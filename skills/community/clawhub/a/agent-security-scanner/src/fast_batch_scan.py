#!/usr/bin/env python3
"""
直接调用扫描器 API - 批量扫描所有样本 (并发优化版)
加载一次，扫描全部，输出详细结果

优化:
- ThreadPoolExecutor 并发扫描
- 批量结果写入
- 进度实时显示
"""
import sys
import json
import os
import time
from pathlib import Path
from collections import defaultdict
# 并发在 CPU 密集型任务中受 GIL 限制，使用单线程 + 规则优化
from dataclasses import asdict

# 添加扫描器路径
SCANNER_DIR = "/home/cdy/.openclaw/workspace/agent-security-skill-scanner-master"
sys.path.insert(0, SCANNER_DIR)

from multi_language_scanner_v4 import MultiLanguageScanner, ScanResult

SAMPLES_DIR = "/home/cdy/Desktop/security-benchmark/samples/from-templates"
OUTPUT_FILE = "/home/cdy/.openclaw/workspace/agent-security-skill-scanner-master/reports/batch_scan_result.json"
MAX_WORKERS = 8  # 并发数

def main():
    print("=" * 70)
    print("🚀 批量扫描器 - 加载一次，扫描全部")
    print("=" * 70)
    
    # 初始化扫描器（只加载一次规则）
    print("\n📥 加载扫描器...")
    scanner = MultiLanguageScanner(use_smart_scoring=True)
    print("✅ 扫描器已加载")
    
    # 收集所有 payload 文件及其 metadata
    print(f"\n📂 收集样本：{SAMPLES_DIR}")
    samples = []
    
    for root, dirs, files in os.walk(SAMPLES_DIR):
        if 'metadata.json' not in files:
            continue
        
        sample_name = os.path.basename(root)
        metadata_path = os.path.join(root, 'metadata.json')
        
        try:
            with open(metadata_path) as f:
                meta = json.load(f)
            
            gt = meta.get('ground_truth', {})
            is_malicious_gt = gt.get('is_malicious', False)
            attack_type = meta.get('attack_type', 'unknown')
            
            # 找 payload 文件
            payload_path = None
            for f in files:
                if f.startswith('payload.'):
                    payload_path = os.path.join(root, f)
                    break
            
            if payload_path and os.path.exists(payload_path):
                samples.append({
                    'path': payload_path,
                    'sample_name': sample_name,
                    'is_malicious_gt': is_malicious_gt,
                    'attack_type': attack_type
                })
        except Exception as e:
            pass
    
    print(f"✅ 收集到 {len(samples)} 个样本")
    
    # 批量扫描 (单线程优化版)
    print(f"\n🔍 开始扫描...")
    start_time = time.time()
    
    results = []
    tp = fn = tn = fp = 0
    by_attack = defaultdict(lambda: {'tp': 0, 'fn': 0, 'total': 0})
    
    for i, sample in enumerate(samples):
        # 扫描单个文件
        scan_result = scanner.scan_file(Path(sample['path']))
        
        is_malicious_detected = scan_result.is_malicious
        is_malicious_gt = sample['is_malicious_gt']
        attack_type = sample['attack_type']
        
        # 计算混淆矩阵
        if is_malicious_gt and is_malicious_detected:
            tp += 1
            by_attack[attack_type]['tp'] += 1
        elif is_malicious_gt and not is_malicious_detected:
            fn += 1
        elif not is_malicious_gt and is_malicious_detected:
            fp += 1
        else:
            tn += 1
        
        by_attack[attack_type]['total'] += 1
        
        # 保存结果
        results.append({
            'sample_name': sample['sample_name'],
            'path': sample['path'],
            'language': scan_result.language,
            'attack_type': attack_type,
            'is_malicious_gt': is_malicious_gt,
            'is_malicious_detected': is_malicious_detected,
            'risk_score': scan_result.risk_score,
            'risk_level': scan_result.risk_level,
            'detection_method': scan_result.detection_method,
            'behaviors': scan_result.behaviors[:5] if scan_result.behaviors else []
        })
        
        # 进度
        if (i + 1) % 5000 == 0:
            elapsed = time.time() - start_time
            rate = (i + 1) / elapsed if elapsed > 0 else 0
            print(f"  进度：{i+1}/{len(samples)} ({rate:.1f} 样本/秒)")
    
    elapsed = time.time() - start_time
    
    # 输出统计
    total_malicious = tp + fn
    total_benign = tn + fp
    detection_rate = (tp / total_malicious * 100) if total_malicious > 0 else 0
    fpr = (fp / total_benign * 100) if total_benign > 0 else 0
    precision = (tp / (tp + fp) * 100) if (tp + fp) > 0 else 0
    
    print(f"\n📊 扫描完成:")
    print(f"   总样本：{len(samples)}")
    print(f"   耗时：{elapsed:.1f} 秒")
    print(f"   速度：{len(samples)/elapsed:.1f} 样本/秒")
    print(f"\n=== 检测结果 ===")
    print(f"   TP={tp}, FN={fn}, TN={tn}, FP={fp}")
    print(f"   检测率 (DR): {detection_rate:.2f}%")
    print(f"   误报率 (FPR): {fpr:.2f}%")
    print(f"   精确率 (Precision): {precision:.2f}%")
    
    print(f"\n=== 按攻击类型 ===")
    for at, stats in sorted(by_attack.items(), key=lambda x: -x[1]['total'])[:20]:
        total = stats['total']
        tp_at = stats['tp']
        fn_at = total - tp_at
        dr_at = (tp_at / total * 100) if total > 0 else 0
        print(f"  {at}: {tp_at}/{total} ({dr_at:.1f}%)")
    
    # 保存结果
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        json.dump({
            'summary': {
                'total': len(samples),
                'tp': tp, 'fn': fn, 'tn': tn, 'fp': fp,
                'detection_rate': detection_rate,
                'false_positive_rate': fpr,
                'precision': precision,
                'elapsed_seconds': elapsed,
                'samples_per_second': len(samples)/elapsed
            },
            'by_attack_type': {at: dict(stats) for at, stats in by_attack.items()},
            'results': results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ 结果已保存：{OUTPUT_FILE}")

if __name__ == '__main__':
    main()
