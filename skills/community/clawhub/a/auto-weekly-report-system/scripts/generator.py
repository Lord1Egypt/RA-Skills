#!/usr/bin/env python3
"""
报告生成器 - 将数据转换为 Markdown 周报
"""

import json
from datetime import datetime
from pathlib import Path

class ReportGenerator:
    def __init__(self, data_file="/tmp/weekly_data.json"):
        self.data_file = data_file
        self.data = self._load_data()
    
    def _load_data(self):
        """加载数据"""
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def generate(self):
        """生成完整周报"""
        lines = []
        
        # 标题
        lines.extend(self._generate_header())
        lines.append("")
        
        # v3.5 章节
        lines.extend(self._generate_v35_section())
        lines.append("")
        
        # InStreet 章节
        lines.extend(self._generate_instreet_section())
        lines.append("")
        
        # 价格监控章节
        lines.extend(self._generate_price_section())
        lines.append("")
        
        # 系统健康
        lines.extend(self._generate_health_section())
        lines.append("")
        
        # 下周计划
        lines.extend(self._generate_next_week())
        lines.append("")
        
        # 页脚
        lines.append("---")
        lines.append(f"\n*本报告由 Auto Weekly System 自动生成*")
        lines.append(f"*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        
        return "\n".join(lines)
    
    def _generate_header(self):
        """生成标题"""
        period = self.data.get("period", "本周")
        return [
            f"# 🤖 MoltbookAgent 项目周报",
            f"",
            f"**报告周期**: {period}",
            f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"",
            "---",
        ]
    
    def _generate_v35_section(self):
        """生成 v3.5 章节"""
        v35 = self.data.get("v35", {})
        lines = [
            "## 🧠 v3.5 因果推理系统",
            "",
            f"**当前状态**: {v35.get('status', '未知')}",
            "",
            "### 本周表现",
            "",
            f"| 指标 | 数值 |",
            f"|------|------|",
            f"| 运行次数 | {v35.get('week_runs', 0)} |",
            f"| 平均赞数 | {v35.get('week_avg', 0):.1f} |",
            f"| 累计赞数 | {sum(v35.get('week_votes', [])):.0f} |",
            f"| 预测准确度 | {v35.get('accuracy', 0)*100:.0f}% |",
            "",
        ]
        
        # 策略分析
        if v35.get('week_avg', 0) > 20:
            lines.append("✅ **表现优异**: 平均赞数超过20，因果推理策略有效")
        elif v35.get('week_avg', 0) > 15:
            lines.append("⚠️ **表现良好**: 平均赞数在15-20之间，持续优化中")
        else:
            lines.append("📉 **需要关注**: 平均赞数偏低，建议检查策略")
        
        return lines
    
    def _generate_instreet_section(self):
        """生成 InStreet 章节"""
        instreet = self.data.get("instreet", {})
        lines = [
            "## 📱 InStreet 自动回复",
            "",
            f"**运行状态**: {instreet.get('status', '未知')}",
            "",
        ]
        
        if "total_replies" in instreet:
            lines.extend([
                "### 本周统计",
                "",
                f"| 指标 | 数值 |",
                f"|------|------|",
                f"| 总回复数 | {instreet.get('total_replies', 0)} |",
                f"| 成功回复 | {instreet.get('successful', 0)} |",
                f"| 失败数 | {instreet.get('failed', 0)} |",
                f"| 成功率 | {instreet.get('success_rate', 'N/A')} |",
                f"| 早高峰运行 | {instreet.get('morning_rush_runs', 0)} 次 |",
                "",
            ])
        
        if "hint" in instreet:
            lines.append(f"💡 **提示**: {instreet['hint']}")
        
        return lines
    
    def _generate_price_section(self):
        """生成价格监控章节"""
        price = self.data.get("price_monitor", {})
        lines = [
            "## 💰 竞品价格监控",
            "",
            f"**监控状态**: {price.get('status', '未知')}",
            "",
        ]
        
        products = price.get("products", [])
        if products:
            lines.extend([
                "| 产品 | 当前价格 | 最后检查 |",
                "|------|----------|----------|",
            ])
            for p in products:
                lines.append(f"| {p['name']} | {p['price']} | {p['last_check']} |")
            lines.append("")
        
        return lines
    
    def _generate_health_section(self):
        """生成系统健康章节"""
        health = self.data.get("system_health", {})
        lines = [
            "## 🔧 系统健康检查",
            "",
            f"**总体状态**: {health.get('overall', '未知')}",
            f"**磁盘使用**: {health.get('disk_usage', '未知')}",
            "",
            "### 日志文件状态",
            "",
        ]
        
        logs = health.get("logs_status", {})
        for name, exists in logs.items():
            status = "✅" if exists else "❌"
            lines.append(f"- {status} {name}")
        
        return lines
    
    def _generate_next_week(self):
        """生成下周计划"""
        return [
            "## 📋 下周计划",
            "",
            "- [ ] 持续监控 v3.5 生产表现",
            "- [ ] 分析 InStreet 回复数据（日志启用后）",
            "- [ ] 跟踪竞品价格变动",
            "- [ ] 优化周报自动化流程",
            "",
        ]

if __name__ == "__main__":
    # 先生成数据
    import subprocess
    subprocess.run(["python3", str(Path(__file__).parent / "collector.py")])
    
    # 生成报告
    generator = ReportGenerator()
    report = generator.generate()
    
    # 保存
    output_file = "/tmp/weekly_report_auto.md"
    with open(output_file, 'w') as f:
        f.write(report)
    
    print(report)
    print(f"\n💾 报告已保存: {output_file}")
