#!/usr/bin/env python3
"""
合成数据生成脚本
用于生成基于模板的图表数据集
"""

import os
import json
import random
from pathlib import Path
from typing import Dict, List, Any

class SyntheticDataGenerator:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.synthetic_dir = self.data_dir / "synthetic"

        # 创建目录
        self.synthetic_dir.mkdir(parents=True, exist_ok=True)

    def generate_pie_chart(self, index: int) -> Dict[str, Any]:
        """
        生成饼图
        """
        print(f"🎨 生成饼图 {index}...")

        # 随机数据
        labels = ["类别A", "类别B", "类别C", "类别D", "类别E"]
        values = [random.randint(10, 100) for _ in range(5)]

        # 生成图表
        chart = {
            "type": "饼图",
            "title": f"饼图示例 {index}",
            "labels": labels,
            "values": values,
            "total": sum(values)
        }

        # 保存图表
        with open(self.synthetic_dir / f"pie_chart_{index:03d}.json", "w", encoding="utf-8") as f:
            json.dump(chart, f, ensure_ascii=False, indent=2)

        print(f"✅ 饼图 {index} 已保存到 {self.synthetic_dir / f'pie_chart_{index:03d}.json'}")
        return chart

    def generate_bar_chart(self, index: int) -> Dict[str, Any]:
        """
        生成柱状图
        """
        print(f"🎨 生成柱状图 {index}...")

        # 随机数据
        categories = ["一月", "二月", "三月", "四月", "五月", "六月"]
        values = [random.randint(50, 200) for _ in range(6)]

        # 生成图表
        chart = {
            "type": "柱状图",
            "title": f"柱状图示例 {index}",
            "categories": categories,
            "values": values,
            "x_label": "月份",
            "y_label": "数值"
        }

        # 保存图表
        with open(self.synthetic_dir / f"bar_chart_{index:03d}.json", "w", encoding="utf-8") as f:
            json.dump(chart, f, ensure_ascii=False, indent=2)

        print(f"✅ 柱状图 {index} 已保存到 {self.synthetic_dir / f'bar_chart_{index:03d}.json'}")
        return chart

    def generate_line_chart(self, index: int) -> Dict[str, Any]:
        """
        生成折线图
        """
        print(f"🎨 生成折线图 {index}...")

        # 随机数据
        x_values = list(range(1, 11))
        y_values = [random.randint(10, 100) for _ in range(10)]

        # 生成图表
        chart = {
            "type": "折线图",
            "title": f"折线图示例 {index}",
            "x_values": x_values,
            "y_values": y_values,
            "x_label": "X轴",
            "y_label": "Y轴"
        }

        # 保存图表
        with open(self.synthetic_dir / f"line_chart_{index:03d}.json", "w", encoding="utf-8") as f:
            json.dump(chart, f, ensure_ascii=False, indent=2)

        print(f"✅ 折线图 {index} 已保存到 {self.synthetic_dir / f'line_chart_{index:03d}.json'}")
        return chart

    def generate_table(self, index: int) -> Dict[str, Any]:
        """
        生成表格
        """
        print(f"🎨 生成表格 {index}...")

        # 随机数据
        headers = ["姓名", "年龄", "城市", "职业"]
        rows = [
            ["张三", "25", "北京", "工程师"],
            ["李四", "30", "上海", "设计师"],
            ["王五", "28", "广州", "产品经理"],
            ["赵六", "35", "深圳", "数据分析师"]
        ]

        # 生成表格
        table = {
            "type": "表格",
            "title": f"表格示例 {index}",
            "headers": headers,
            "rows": rows,
            "row_count": len(rows),
            "col_count": len(headers)
        }

        # 保存表格
        with open(self.synthetic_dir / f"table_{index:03d}.json", "w", encoding="utf-8") as f:
            json.dump(table, f, ensure_ascii=False, indent=2)

        print(f"✅ 表格 {index} 已保存到 {self.synthetic_dir / f'table_{index:03d}.json'}")
        return table

    def generate_all(self, count: int = 100) -> Dict[str, Any]:
        """
        生成所有合成数据
        """
        print(f"🚀 开始生成合成数据 ({count} 张图表)...")

        charts = []
        for i in range(count):
            chart_type = random.choice(["饼图", "柱状图", "折线图", "表格"])

            if chart_type == "饼图":
                chart = self.generate_pie_chart(i)
            elif chart_type == "柱状图":
                chart = self.generate_bar_chart(i)
            elif chart_type == "折线图":
                chart = self.generate_line_chart(i)
            elif chart_type == "表格":
                chart = self.generate_table(i)

            charts.append(chart)

        # 保存汇总
        with open(self.synthetic_dir / "all_synthetic_data.json", "w", encoding="utf-8") as f:
            json.dump(charts, f, ensure_ascii=False, indent=2)

        print(f"✅ 所有合成数据已保存到 {self.synthetic_dir / 'all_synthetic_data.json'}")
        return charts

if __name__ == "__main__":
    generator = SyntheticDataGenerator()
    charts = generator.generate_all(100)
    print("\n🎉 合成数据生成完成！")
