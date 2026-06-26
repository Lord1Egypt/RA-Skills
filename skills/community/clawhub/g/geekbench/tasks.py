#!/usr/bin/env python3
"""
Geekbench 任务处理器
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List
from geekbench_crawler import GeekbenchCrawler

class GeekbenchTasks:
    def __init__(self):
        self.crawler = GeekbenchCrawler()
        self.data_dir = '/Users/ding/.openclaw/workspace/geekbench/data'
        self.ensure_data_dir()

    def ensure_data_dir(self):
        """确保数据目录存在"""
        os.makedirs(self.data_dir, exist_ok=True)

    def task_analyze_device(self, device_name: str) -> str:
        """
        任务 4.1: 分析特定设备的跑分分布
        技巧: 先搜索 "设备名 + geekbench" 获取内部型号
        """
        print(f"\n🚀 开始分析设备: {device_name}")

        # Step 1: 搜索内部型号
        print("🔍 Step 1: 查找内部型号...")
        
        # 方法1: 搜索 "设备名 + geekbench"
        search_term = f"{device_name} geekbench"
        internal_results = self.crawler.search_device(search_term)
        
        # 提取内部型号
        internal_model = None
        if internal_results:
            for r in internal_results[:5]:
                text = r.get('text', '')
                # 内部型号通常是 10-15 位的字母数字组合，且包含设备品牌名
                import re
                models = re.findall(r'\b[A-Z0-9]{8,15}\b', text)
                for m in models:
                    # 检查型号是否与搜索结果匹配（包含品牌名）
                    if device_name.split()[0].lower() in text.lower():  # 荣耀
                        if m not in ['Linux', 'Android', 'Windows', 'GHz', 'ARM', 'Intel', 'AMD', 'Apple', 'Qualcomm']:
                            internal_model = m
                            print(f"  ✅ 发现内部型号: {internal_model}")
                            break
                if internal_model:
                    break
        
        # 如果方法1失败，尝试直接搜索 "geekbench" 获取最新记录
        if not internal_model:
            print("  ⚠️ 方法1未找到，尝试方法2...")
            latest = self.crawler.get_latest_benchmarks(20)
            for l in latest:
                title = l.get('title', '')
                if device_name.split()[0] in title:  # 检查品牌名
                    # 获取详情来确认
                    detail = self.crawler.get_benchmark_detail(l['id'])
                    if detail and device_name in str(detail.get('model', '')):
                        internal_model = detail.get('model', '').split()[-1] if detail.get('model') else None
                        if internal_model and len(internal_model) > 5:
                            print(f"  ✅ 从最新记录发现: {internal_model}")
                            break
        
        # Step 2: 使用内部型号搜索
        print("🔍 Step 2: 使用内部型号搜索跑分...")
        if internal_model:
            search_results = self.crawler.search_device(internal_model)
            print(f"  使用内部型号 '{internal_model}' 搜索")
        else:
            search_results = self.crawler.search_device(device_name)
            print(f"  使用原始名称 '{device_name}' 搜索")

        if not search_results:
            return f"❌ 未找到设备: {device_name}"

        print(f"✅ 找到 {len(search_results)} 条跑分记录")

        # 获取详细信息
        all_benchmarks = []
        for result in search_results[:30]:  # 获取最多30条
            print(f"  📥 获取 #{result['id']}...")
            detail = self.crawler.get_benchmark_detail(result['id'])
            if detail:
                all_benchmarks.append(detail)

        if not all_benchmarks:
            return "❌ 无法获取跑分详情"

        # 按版本分组统计
        version_stats = {}
        for bench in all_benchmarks:
            version = bench.get('version', 'Unknown')
            if version not in version_stats:
                version_stats[version] = {
                    'count': 0,
                    'single_scores': [],
                    'multi_scores': [],
                    'benchmarks': []
                }
            version_stats[version]['count'] += 1
            version_stats[version]['single_scores'].append(bench['single_core_score'])
            version_stats[version]['multi_scores'].append(bench['multi_core_score'])
            version_stats[version]['benchmarks'].append(bench)

        # 生成报告
        report = [
            f"📱 **设备: {device_name}**",
            f"📊 **总跑分数: {len(all_benchmarks)}**",
            "=" * 60
        ]

        # 保存原始数据
        raw_data = {
            'device': device_name,
            'analyzed_at': datetime.now().isoformat(),
            'total_count': len(all_benchmarks),
            'versions': version_stats
        }
        self.save_data(f"{device_name}_raw.json", raw_data)

        for version, stats in sorted(version_stats.items()):
            avg_single = sum(stats['single_scores']) / len(stats['single_scores'])
            avg_multi = sum(stats['multi_scores']) / len(stats['multi_scores'])
            median_single = self._median(stats['single_scores'])
            median_multi = self._median(stats['multi_scores'])

            report.extend([
                f"\n🔹 **Geekbench {version}**",
                f"  - 跑分数量: {stats['count']}",
                f"  - Single-Core 平均分: **{avg_single:.0f}** (中位数: {median_single:.0f})",
                f"  - Multi-Core 平均分: **{avg_multi:.0f}** (中位数: {median_multi:.0f})"
            ])

            # 找出典型值（最接近中位数）
            if stats['benchmarks']:
                typical = min(stats['benchmarks'],
                             key=lambda x: abs(x['single_core_score'] - median_single))
                report.append(
                    f"\n  📌 **典型跑分示例** #{typical['id']}:\n"
                    f"     🔗 链接: https://browser.geekbench.com/v6/cpu/{typical['id']}\n"
                    f"     - 型号: {typical['model']}\n"
                    f"     - 系统: {typical['operating_system']}\n"
                    f"     - CPU: {typical['cpu']['name']}\n"
                    f"     - Single-Core: **{typical['single_core_score']}**\n"
                    f"     - Multi-Core: **{typical['multi_core_score']}**"
                )

        report.append("\n" + "=" * 60)

        result = '\n'.join(report)
        self.save_data(f"{device_name}_report.txt", {'report': result})

        return result

    def _median(self, values: List[int]) -> float:
        """计算中位数"""
        sorted_vals = sorted(values)
        n = len(sorted_vals)
        if n % 2 == 0:
            return (sorted_vals[n//2 - 1] + sorted_vals[n//2]) / 2
        return sorted_vals[n//2]

    def task_monitor_latest(self, save_path: str = None) -> Dict:
        """
        任务 4.2: 监控最新上传的跑分
        """
        print("\n🔔 监控最新跑分...")

        latest = self.crawler.get_latest_benchmarks(50)

        # 加载上次记录
        last_file = os.path.join(self.data_dir, 'last_check.json')
        last_data = {}
        if os.path.exists(last_file):
            with open(last_file, 'r') as f:
                last_data = json.load(f)

        last_benchmarks = set(last_data.get('benchmarks', []))
        current_benchmarks = set(b['id'] for b in latest)

        # 找出新的
        new_ids = current_benchmarks - last_benchmarks
        new_benchmarks = [b for b in latest if b['id'] in new_ids]

        # 检查高分
        high_scores = {
            'single_core': [],
            'multi_core': []
        }

        if latest:
            # 找出最高分
            max_single = max(latest, key=lambda x: x['single_core'])
            max_multi = max(latest, key=lambda x: x['multi_core'])

            high_scores['single_core'] = max_single
            high_scores['multi_core'] = max_multi

        # 保存当前状态
        current_state = {
            'checked_at': datetime.now().isoformat(),
            'benchmarks': list(current_benchmarks)
        }
        self.save_data('last_check.json', current_state)

        result = {
            'timestamp': datetime.now().isoformat(),
            'new_count': len(new_benchmarks),
            'new_benchmarks': new_benchmarks,
            'high_scores': high_scores
        }

        return result

    def save_data(self, filename: str, data: Dict):
        """保存数据"""
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"💾 已保存: {filepath}")

    def generate_monitor_report(self, monitor_result: Dict) -> str:
        """生成监控报告"""
        if not monitor_result:
            return "❌ 无监控数据"

        lines = [
            f"🔔 **Geekbench 监控报告**",
            f"⏰ 检测时间: {monitor_result['timestamp']}",
            "-" * 60
        ]

        if monitor_result['new_count'] > 0:
            lines.append(f"\n🆕 **新增跑分 ({monitor_result['new_count']} 条)**:")
            for b in monitor_result['new_benchmarks'][:10]:  # 只显示前10条
                lines.append(
                    f"  • #{b['id']}: {b['title']}\n"
                    f"    Single: {b['single_core']} | Multi: {b['multi_core']}"
                )
        else:
            lines.append("\n✅ 无新增跑分")

        if monitor_result['high_scores']:
            lines.extend([
                "\n🏆 **本次最高分**",
                f"  Single-Core: #{monitor_result['high_scores']['single_core']['id']} "
                f"({monitor_result['high_scores']['single_core']['single_core']}分)",
                f"  Multi-Core: #{monitor_result['high_scores']['multi_core']['id']} "
                f"({monitor_result['high_scores']['multi_core']['multi_core']}分)"
            ])

        return '\n'.join(lines)


def main():
    """主函数"""
    tasks = GeekbenchTasks()

    if len(sys.argv) < 2:
        print("用法:")
        print("  python tasks.py analyze <设备名>")
        print("  python tasks.py monitor")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'analyze':
        if len(sys.argv) < 3:
            print("请指定设备名，例如: python tasks.py analyze 小米17")
            sys.exit(1)
        device_name = ' '.join(sys.argv[2:])
        result = tasks.task_analyze_device(device_name)
        print("\n" + result)

    elif command == 'monitor':
        result = tasks.task_monitor_latest()
        report = tasks.generate_monitor_report(result)
        print("\n" + report)

    else:
        print(f"未知命令: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
