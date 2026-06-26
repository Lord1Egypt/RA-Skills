#!/usr/bin/env python3
"""
并发扫描所有样本 - Benchmark 测试
使用 scanner_distributed_v4_1 扫描所有 malicious 样本
"""

import os
import sys
import json
import time
import statistics
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import yara
except ImportError:
    print("❌ 需要安装 yara-python: pip3 install yara-python")
    sys.exit(1)

SAMPLES_DIR = "samples/malicious"
RULES_DIR = "rules/yara"
REPORT_DIR = "reports"

def load_rules():
    """加载所有 YARA 规则"""
    print("📋 加载 YARA 规则...")
    # 使用合并规则文件
    merged_rules = Path("rules/scanner_v3/yara/merged_rules.yar")
    
    if not merged_rules.exists():
        print(f"❌ 合并规则文件不存在：{merged_rules}")
        return None
    
    try:
        rules_content = merged_rules.read_text(errors='ignore')
        rules = yara.compile(source=rules_content)
        print(f"   ✅ 加载 merged_rules.yar ({len(rules_content):,} 字节)")
        return rules
    except Exception as e:
        print(f"❌ 规则编译失败：{e}")
        return None

def collect_samples():
    """收集所有样本文件"""
    print("\n📂 收集样本文件...")
    samples = []
    sample_path = Path(SAMPLES_DIR)
    
    for txt_file in sample_path.rglob("*.txt"):
        samples.append(txt_file)
    
    print(f"   ✅ 收集 {len(samples):,} 个样本文件")
    return samples

def scan_sample(rules, sample_file):
    """扫描单个样本"""
    try:
        content = sample_file.read_text(errors='ignore')
        
        start = time.perf_counter()
        matches = rules.match(data=content)
        elapsed = (time.perf_counter() - start) * 1000  # ms
        
        detected = len(matches) > 0
        matched_rules = [m.rule for m in matches]
        
        return {
            'file': str(sample_file),
            'detected': detected,
            'rules': matched_rules,
            'time_ms': elapsed
        }
    except Exception as e:
        return {
            'file': str(sample_file),
            'detected': False,
            'rules': [],
            'time_ms': 0,
            'error': str(e)
        }

def scan_batch(args):
    """批量扫描（用于并发）"""
    rules, samples = args
    results = []
    for sample in samples:
        result = scan_sample(rules, sample)
        results.append(result)
    return results

def main():
    print("=" * 70)
    print("🚀 并发扫描所有样本 - Benchmark 测试")
    print("=" * 70)
    
    # 加载规则
    rules = load_rules()
    if not rules:
        sys.exit(1)
    
    # 收集样本
    samples = collect_samples()
    if not samples:
        sys.exit(1)
    
    # 并发扫描
    print("\n⚡ 启动并发扫描 (16 线程)...")
    start_time = time.time()
    
    # 分块处理
    chunk_size = 50
    chunks = [samples[i:i+chunk_size] for i in range(0, len(samples), chunk_size)]
    
    all_results = []
    with ThreadPoolExecutor(max_workers=16) as executor:
        futures = [executor.submit(scan_batch, (rules, chunk)) for chunk in chunks]
        for future in as_completed(futures):
            results = future.result()
            all_results.extend(results)
    
    total_time = time.time() - start_time
    
    # 统计结果
    detected_count = sum(1 for r in all_results if r['detected'])
    missed_count = len(all_results) - detected_count
    detection_rate = (detected_count / len(all_results)) * 100 if all_results else 0
    
    scan_times = [r['time_ms'] for r in all_results if 'time_ms' in r and r['time_ms'] > 0]
    avg_time = statistics.mean(scan_times) if scan_times else 0
    p99_time = sorted(scan_times)[int(len(scan_times) * 0.99)] if len(scan_times) > 1 else avg_time
    p95_time = sorted(scan_times)[int(len(scan_times) * 0.95)] if len(scan_times) > 1 else avg_time
    
    # 打印结果
    print("\n" + "=" * 70)
    print("📊 Benchmark 结果")
    print("=" * 70)
    
    print(f"\n✅ 扫描样本：{len(all_results):,} 个")
    print(f"✅ 检测成功：{detected_count:,} ({detection_rate:.1f}%)")
    print(f"❌ 漏报：{missed_count:,} ({100-detection_rate:.1f}%)")
    
    print(f"\n⚡ 性能指标")
    print(f"   总耗时：{total_time:.2f} 秒")
    print(f"   平均耗时：{avg_time:.3f} ms/样本")
    print(f"   P95 耗时：{p95_time:.3f} ms")
    print(f"   P99 耗时：{p99_time:.3f} ms")
    print(f"   吞吐量：{len(all_results)/total_time:.1f} 样本/秒")
    
    # 规则匹配统计
    print(f"\n📋 规则匹配统计 (Top 10):")
    rule_stats = {}
    for r in all_results:
        for rule in r['rules']:
            rule_stats[rule] = rule_stats.get(rule, 0) + 1
    
    for rule, count in sorted(rule_stats.items(), key=lambda x: -x[1])[:10]:
        print(f"   {rule}: {count} 次")
    
    # 生成报告
    report = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'total_samples': len(all_results),
        'detected': detected_count,
        'missed': missed_count,
        'detection_rate': detection_rate,
        'total_time_seconds': total_time,
        'avg_time_ms': avg_time,
        'p95_time_ms': p95_time,
        'p99_time_ms': p99_time,
        'throughput_samples_per_sec': len(all_results)/total_time,
        'rule_stats': rule_stats,
        'status': 'PASS' if detection_rate >= 95 else 'NEEDS_IMPROVEMENT'
    }
    
    # 保存报告
    Path(REPORT_DIR).mkdir(exist_ok=True)
    report_file = f"{REPORT_DIR}/benchmark_full_scan_{time.strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n💾 报告已保存：{report_file}")
    
    # 保存 Markdown 摘要
    md_file = report_file.replace('.json', '.md')
    with open(md_file, 'w') as f:
        f.write(f"# Benchmark 全量扫描报告\n\n")
        f.write(f"**时间**: {report['timestamp']}\n\n")
        f.write(f"## 检测结果\n\n")
        f.write(f"- 总样本：{report['total_samples']:,}\n")
        f.write(f"- 检测成功：{report['detected']:,} ({report['detection_rate']:.1f}%)\n")
        f.write(f"- 漏报：{report['missed']:,}\n\n")
        f.write(f"## 性能指标\n\n")
        f.write(f"- 总耗时：{report['total_time_seconds']:.2f} 秒\n")
        f.write(f"- 平均耗时：{report['avg_time_ms']:.3f} ms\n")
        f.write(f"- P95 耗时：{report['p95_time_ms']:.3f} ms\n")
        f.write(f"- P99 耗时：{report['p99_time_ms']:.3f} ms\n")
        f.write(f"- 吞吐量：{report['throughput_samples_per_sec']:.1f} 样本/秒\n\n")
        f.write(f"## 状态\n\n")
        f.write(f"{'✅ PASS' if report['status'] == 'PASS' else '⚠️ NEEDS_IMPROVEMENT'}\n")
    
    print(f"📄 Markdown 报告：{md_file}")
    
    print("\n" + "=" * 70)
    if detection_rate >= 98:
        print("✅ 检测能力：优秀 (≥98%)")
    elif detection_rate >= 95:
        print("✅ 检测能力：良好 (≥95%)")
    elif detection_rate >= 90:
        print("⚠️  检测能力：需要改进 (≥90%)")
    else:
        print("❌ 检测能力：不足 (<90%)")
    print("=" * 70)
    
    return report

if __name__ == "__main__":
    main()
