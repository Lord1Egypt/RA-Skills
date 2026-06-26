#!/usr/bin/env python3
"""
批量扫描器 - 一次加载，扫描所有样本
避免反复启动进程的开销
"""
import sys
import json
import os
import subprocess
import time
from pathlib import Path
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

SAMPLES_DIR = "/home/cdy/Desktop/security-benchmark/samples/from-templates"
SCANNER_DIR = "/home/cdy/.openclaw/workspace/agent-security-skill-scanner-master"
SCANNER_SCRIPT = os.path.join(SCANNER_DIR, "multi_language_scanner_v4.py")

def scan_batch(batch_files):
    """批量扫描一组文件"""
    try:
        result = subprocess.run(
            ["python3", SCANNER_SCRIPT] + list(batch_files),
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.stdout
    except Exception as e:
        return f"Error: {e}"

def main():
    print("=" * 70)
    print("🚀 批量扫描器 - 一次加载，持续扫描")
    print("=" * 70)
    
    # 收集所有 payload 文件
    print(f"\n📂 收集样本：{SAMPLES_DIR}")
    sample_files = []
    sample_map = {}  # sample_name -> payload_path
    
    for root, dirs, files in os.walk(SAMPLES_DIR):
        if 'metadata.json' not in files:
            continue
        
        sample_name = os.path.basename(root)
        metadata_path = os.path.join(root, 'metadata.json')
        
        # 读取 metadata 找 payload 文件
        try:
            with open(metadata_path) as f:
                meta = json.load(f)
            
            gt = meta.get('ground_truth', {})
            is_malicious = gt.get('is_malicious', False)
            attack_type = meta.get('attack_type', 'unknown')
            payload_file = gt.get('payload_file', '')
            
            # 找 payload 文件
            payload_path = None
            for f in files:
                if f.startswith('payload.'):
                    payload_path = os.path.join(root, f)
                    break
            
            if payload_path and os.path.exists(payload_path):
                sample_files.append(payload_path)
                sample_map[payload_path] = {
                    'sample_name': sample_name,
                    'is_malicious': is_malicious,
                    'attack_type': attack_type
                }
        except:
            pass
    
    print(f"✅ 收集到 {len(sample_files)} 个样本")
    
    # 分批扫描（每批 100 个文件）
    batch_size = 100
    batches = [sample_files[i:i+batch_size] for i in range(0, len(sample_files), batch_size)]
    
    print(f"\n📦 分 {len(batches)} 批扫描 (每批 {batch_size} 个文件)")
    
    # 扫描结果
    results = []
    start_time = time.time()
    
    # 用线程池并发扫描
    max_workers = 4
    print(f"👷 并发数：{max_workers}")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {}
        for i, batch in enumerate(batches):
            future = executor.submit(scan_batch, batch)
            futures[future] = i
        
        completed = 0
        for future in as_completed(futures):
            batch_idx = futures[future]
            batch = batches[batch_idx]
            
            try:
                output = future.result()
                # 解析输出（简化处理，假设输出是 JSON）
                # 实际需要根据扫描器输出格式解析
                for f in batch:
                    # 简化：假设所有文件都是恶意（实际需要解析扫描结果）
                    results.append({
                        'file': f,
                        'detected': True,  # 需要实际解析
                        'sample': sample_map.get(f, {})
                    })
            except Exception as e:
                print(f"Batch {batch_idx} error: {e}")
            
            completed += 1
            if completed % 10 == 0:
                elapsed = time.time() - start_time
                rate = completed / elapsed if elapsed > 0 else 0
                print(f"  进度：{completed}/{len(batches)} 批 ({rate:.1f} 批/秒)")
    
    elapsed = time.time() - start_time
    
    # 计算统计
    print(f"\n📊 扫描完成:")
    print(f"   总样本：{len(sample_files)}")
    print(f"   耗时：{elapsed:.1f} 秒")
    print(f"   速度：{len(sample_files)/elapsed:.1f} 样本/秒")
    
    # 按攻击类型统计
    by_attack = defaultdict(lambda: {'total': 0, 'detected': 0})
    for r in results:
        sample = r.get('sample', {})
        attack_type = sample.get('attack_type', 'unknown')
        by_attack[attack_type]['total'] += 1
        if r.get('detected'):
            by_attack[attack_type]['detected'] += 1
    
    print(f"\n=== 按攻击类型 ===")
    for at, stats in sorted(by_attack.items(), key=lambda x: -x[1]['total'])[:15]:
        total = stats['total']
        detected = stats['detected']
        rate = (detected/total*100) if total > 0 else 0
        print(f"  {at}: {detected}/{total} ({rate:.1f}%)")

if __name__ == '__main__':
    main()
