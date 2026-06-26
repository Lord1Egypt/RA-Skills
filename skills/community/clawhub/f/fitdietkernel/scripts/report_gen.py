#!/usr/bin/env python3
"""
BioContext-Kernel Report Generator
自动将日志转换为结构化周报
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path


class ReportGenerator:
    def __init__(self, base_path="."):
        self.base_path = Path(base_path)
        self.logs_path = self.base_path / "logs"

    def get_recent_logs(self, days=7):
        """获取最近N天的日志"""
        logs = []
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            log_file = self.logs_path / f"{date.strftime('%Y-%m-%d')}.md"
            if log_file.exists():
                logs.append(self._parse_log(log_file))
        return logs

    def _parse_log(self, log_file):
        """解析单日日志"""
        with open(log_file, "r", encoding="utf-8") as f:
            content = f.read()

        data = {
            "date": log_file.stem,
            "content": content,
            "meals": [],
            "carbon_actual": 0,
            "sleep_time": None,
        }

        # 简单解析 - 提取碳水数值
        import re

        carbon_matches = re.findall(r"碳水.*?(\d+)g", content)
        if carbon_matches:
            data["carbon_actual"] = sum(int(c) for c in carbon_matches)

        # 提取睡眠时间
        sleep_match = re.search(r"关机时间.*?(\d+:\d+)", content)
        if sleep_match:
            data["sleep_time"] = sleep_match.group(1)

        return data

    def generate_weekly_report(self):
        """生成周报"""
        logs = self.get_recent_logs(7)

        if not logs:
            return "暂无日志数据"

        # 加载 profile 获取目标
        profile_path = self.base_path / "profile.json"
        target_carbon = 147  # 默认MC

        if profile_path.exists():
            with open(profile_path, "r", encoding="utf-8") as f:
                profile = json.load(f)
                target_carbon = (
                    profile.get("carbonCycle", {}).get("medium", {}).get("c", 147)
                )

        # 计算统计数据
        total_carbon = sum(log["carbon_actual"] for log in logs)
        avg_carbon = total_carbon / len(logs) if logs else 0
        carbon_error = avg_carbon - target_carbon

        # 生成报告
        report = f"""# 📊 周报 - {datetime.now().strftime("%Y年%W周")}

## 📈 核心数据

| 维度 | 本周表现 | 状态 |
|------|----------|------|
| 平均碳水 | {avg_carbon:.1f}g | {"🟢" if abs(carbon_error) < 10 else "🟡"} |
| 目标碳水 | {target_carbon}g | - |
| 误差 | {carbon_error:+.1f}g | {"🟢 安全" if abs(carbon_error) < 10 else "🟡 需优化"} |
| 记录天数 | {len(logs)}天 | - |

## 📅 每日详情

"""
        for log in logs:
            status = "✅" if log["carbon_actual"] <= target_carbon + 20 else "⚠️"
            report += f"- {log['date']}: {log['carbon_actual']}g碳水 {status}\n"

        report += f"""
## 💡 建议

{"碳水控制良好，继续保持" if abs(carbon_error) < 10 else "碳水摄入偏高，建议增加低碳日比例"}

---
*由 BioContext-Kernel 自动生成 | {datetime.now().strftime("%Y-%m-%d %H:%M")}*
"""

        return report

    def save_report(self, output_path=None):
        """保存报告"""
        report = self.generate_weekly_report()

        if output_path is None:
            output_path = (
                self.logs_path
                / "weekly_report"
                / f"report_{datetime.now().strftime('%Y-%m-%d')}.md"
            )
        else:
            output_path = Path(output_path)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report)

        print(f"✅ 报告已生成: {output_path}")
        return output_path


if __name__ == "__main__":
    import sys

    path = sys.argv[1] if len(sys.argv) > 1 else "."
    gen = ReportGenerator(path)
    gen.save_report()
