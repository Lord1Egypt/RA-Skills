#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 桌面 Benchmark 样本扫描测试
================================

扫描桌面上的实际安全样本，验证 scanner_v2 的检测能力

样本来源:
- /home/cdy/Desktop/security-benchmark/samples/
- /home/cdy/Desktop/malicious_skills_samples/
- /home/cdy/Desktop/security-samples/samples/

版本：v1.0 (2026-04-07)
"""

import json
import yaml
import sys
from pathlib import Path
from datetime import datetime

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent))
from scanner_v2 import DefenderScanner


class BenchmarkTester:
    """Benchmark 样本测试器"""
    
    def __init__(self):
        self.scanner = DefenderScanner()
        self.results = {
            "total_samples": 0,
            "malicious_samples": 0,
            "benign_samples": 0,
            "detected": 0,
            "missed": 0,
            "false_positives": 0,
            "by_category": {},
            "details": []
        }
    
    def load_sample(self, file_path: Path) -> tuple:
        """加载样本文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                if file_path.suffix in ['.yaml', '.yml']:
                    data = yaml.safe_load(f)
                else:
                    data = json.load(f)
            
            # 提取代码/ payload
            code = None
            is_malicious = True
            category = "unknown"
            
            if isinstance(data, dict):
                code = data.get('payload') or data.get('code') or data.get('content') or data.get('sample')
                is_malicious = data.get('is_malicious', True)
                category = data.get('attack_type') or data.get('category') or data.get('mitre_attack', 'unknown')
            elif isinstance(data, str):
                code = data
            elif isinstance(data, list):
                # 样本列表，取第一个
                if data and isinstance(data[0], dict):
                    code = data[0].get('payload') or data[0].get('code')
                    is_malicious = data[0].get('is_malicious', True)
                    category = data[0].get('attack_type', 'unknown')
            
            return code, is_malicious, category
            
        except Exception as e:
            return None, None, None
    
    def scan_benchmark_dir(self, benchmark_dir: Path):
        """扫描 benchmark 目录"""
        print(f"\n📂 扫描目录：{benchmark_dir}")
        
        # 加载规则
        print("📋 加载检测规则...")
        total_rules = self.scanner.load_rules()
        print(f"✅ 加载 {total_rules} 条规则")
        
        # 查找所有样本文件
        sample_files = []
        for ext in ['*.json', '*.yaml', '*.yml', '*.py', '*.js', '*.sh']:
            sample_files.extend(benchmark_dir.rglob(ext))
        
        # 过滤掉索引文件和无效文件
        sample_files = [f for f in sample_files if 'index' not in f.name.lower() and f.is_file()]
        
        print(f"📊 找到 {len(sample_files)} 个样本文件")
        print()
        
        # 扫描每个样本
        for i, sample_file in enumerate(sample_files):
            code, is_malicious, category = self.load_sample(sample_file)
            
            if not code:
                continue
            
            self.results["total_samples"] += 1
            
            # 检测
            result = self.scanner.detect(code)
            detected = result["is_malicious"]
            
            # 统计
            if is_malicious:
                self.results["malicious_samples"] += 1
                
                if detected:
                    self.results["detected"] += 1
                    
                    # 按类别统计
                    if category not in self.results["by_category"]:
                        self.results["by_category"][category] = {"total": 0, "detected": 0}
                    self.results["by_category"][category]["total"] += 1
                    self.results["by_category"][category]["detected"] += 1
                else:
                    self.results["missed"] += 1
            else:
                self.results["benign_samples"] += 1
                
                if detected:
                    self.results["false_positives"] += 1
            
            # 记录详情 (前 20 个)
            if len(self.results["details"]) < 20:
                self.results["details"].append({
                    "file": str(sample_file),
                    "category": category,
                    "is_malicious": is_malicious,
                    "detected": detected,
                    "risk_level": result.get("risk_level"),
                    "risk_score": result.get("risk_score")
                })
            
            # 进度显示
            if (i + 1) % 50 == 0:
                print(f"  进度：{i+1}/{len(sample_files)} - 已检测：{self.results['detected']}, 漏报：{self.results['missed']}")
        
        print()
    
    def generate_report(self) -> str:
        """生成测试报告"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 计算指标
        total_malicious = self.results["malicious_samples"]
        detection_rate = (self.results["detected"] / total_malicious * 100) if total_malicious > 0 else 0
        
        total_benign = self.results["benign_samples"]
        false_positive_rate = (self.results["false_positives"] / total_benign * 100) if total_benign > 0 else 0
        
        report = f"""# 🧪 桌面 Benchmark 样本扫描测试报告

**测试时间**: {timestamp}  
**测试版本**: scanner_v2  
**样本来源**: /home/cdy/Desktop/security-benchmark/

---

## 📊 核心指标

| 指标 | 结果 | 目标 | 状态 |
|------|------|------|------|
| **检测率** | {detection_rate:.2f}% | ≥95% | {'✅' if detection_rate >= 95 else '⚠️'} |
| **误报率** | {false_positive_rate:.2f}% | ≤15% | {'✅' if false_positive_rate <= 15 else '⚠️'} |
| **精确率** | {(self.results['detected'] / max(self.results['detected'] + self.results['false_positives'], 1) * 100):.2f}% | ≥90% | {'✅' if (self.results['detected'] / max(self.results['detected'] + self.results['false_positives'], 1) * 100) >= 90 else '⚠️'} |

---

## 📋 测试统计

| 项目 | 数量 |
|------|------|
| 总样本数 | {self.results['total_samples']} |
| 恶意样本 | {self.results['malicious_samples']} |
| 良性样本 | {self.results['benign_samples']} |
| 成功检测 | {self.results['detected']} |
| 漏报 | {self.results['missed']} |
| 误报 | {self.results['false_positives']} |

---

## 🎯 按攻击类型检测率

| 攻击类型 | 检测数 | 总数 | 检测率 |
|---------|--------|------|--------|
"""
        
        for attack_type, stats in sorted(self.results['by_category'].items(), key=lambda x: x[1]['total'], reverse=True):
            rate = (stats['detected'] / stats['total'] * 100) if stats['total'] > 0 else 0
            report += f"| {attack_type} | {stats['detected']} | {stats['total']} | {rate:.1f}% |\n"
        
        report += f"""
---

## 📝 详细结果 (前 20 个)

| # | 文件 | 类型 | 预期 | 结果 | 风险等级 |
|---|------|------|------|------|---------|
"""
        
        for i, detail in enumerate(self.results['details'], 1):
            file_name = Path(detail['file']).name[:30]
            expected = "恶意" if detail['is_malicious'] else "安全"
            result = "检出" if detail['detected'] else "未检出"
            status = "✅" if (detail['is_malicious'] == detail['detected']) else "❌"
            
            report += f"| {i} | {file_name} | {detail['category'][:20]} | {expected} | {result} | {detail['risk_level']} |\n"
        
        report += f"""
---

## ✅ 总结

"""
        
        if detection_rate >= 95 and false_positive_rate <= 15:
            report += "**✅ 测试通过！** 检测率和误报率均达到目标。\n\n"
        else:
            report += "**⚠️ 需要优化**\n\n"
            if detection_rate < 95:
                report += f"- 检测率 {detection_rate:.1f}% < 95%，需要增强规则\n"
            if false_positive_rate > 15:
                report += f"- 误报率 {false_positive_rate:.1f}% > 15%，需要优化白名单\n"
        
        # 保存报告
        reports_dir = Path(__file__).parent / "benchmark_reports"
        reports_dir.mkdir(exist_ok=True)
        report_file = reports_dir / f"benchmark_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_file.write_text(report, encoding='utf-8')
        
        return report, str(report_file)
    
    def run_test(self):
        """运行完整测试"""
        print("=" * 70)
        print("🧪 桌面 Benchmark 样本扫描测试")
        print("=" * 70)
        
        # 扫描主要 benchmark 目录
        benchmark_dirs = [
            Path("/home/cdy/Desktop/security-benchmark/samples"),
            Path("/home/cdy/Desktop/malicious_skills_samples"),
            Path("/home/cdy/Desktop/security-samples/samples"),
        ]
        
        for benchmark_dir in benchmark_dirs:
            if benchmark_dir.exists():
                self.scan_benchmark_dir(benchmark_dir)
        
        # 生成报告
        print("📊 生成测试报告...")
        report, report_file = self.generate_report()
        print(f"✅ 报告已保存：{report_file}")
        
        print()
        print("=" * 70)
        print("✅ 测试完成！")
        print("=" * 70)
        
        # 打印摘要
        total_malicious = self.results["malicious_samples"]
        detection_rate = (self.results["detected"] / total_malicious * 100) if total_malicious > 0 else 0
        
        print(f"\n📊 结果摘要:")
        print(f"  总样本：{self.results['total_samples']}")
        print(f"  恶意样本：{total_malicious}")
        print(f"  成功检测：{self.results['detected']}")
        print(f"  漏报：{self.results['missed']}")
        print(f"  检测率：{detection_rate:.2f}%")
        
        if self.results['benign_samples'] > 0:
            false_positive_rate = (self.results['false_positives'] / self.results['benign_samples'] * 100)
            print(f"  良性样本：{self.results['benign_samples']}")
            print(f"  误报：{self.results['false_positives']}")
            print(f"  误报率：{false_positive_rate:.2f}%")


def main():
    tester = BenchmarkTester()
    tester.run_test()


if __name__ == "__main__":
    main()
