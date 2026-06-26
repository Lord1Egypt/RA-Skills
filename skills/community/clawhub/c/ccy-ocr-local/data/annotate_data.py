#!/usr/bin/env python3
"""
数据标注脚本
用于标注图表数据集，包括图表类型、图表元素、文本内容
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any

class DataAnnotator:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.raw_dir = self.data_dir / "raw"
        self.labeled_dir = self.data_dir / "labeled"

        # 创建目录
        self.labeled_dir.mkdir(parents=True, exist_ok=True)

    def annotate_chart_type(self, image_path: str) -> Dict[str, Any]:
        """
        标注图表类型
        """
        print(f"🏷️  标注图表类型: {image_path}")

        # 图表类型
        chart_types = ["饼图", "柱状图", "折线图", "表格", "散点图", "雷达图", "热力图", "其他"]

        # 标注
        annotation = {
            "image_path": image_path,
            "chart_type": "",
            "chart_types": chart_types
        }

        # 保存标注
        with open(self.labeled_dir / f"{Path(image_path).stem}_type.json", "w", encoding="utf-8") as f:
            json.dump(annotation, f, ensure_ascii=False, indent=2)

        print(f"✅ 图表类型标注已保存到 {self.labeled_dir / f'{Path(image_path).stem}_type.json'}")
        return annotation

    def annotate_chart_elements(self, image_path: str) -> Dict[str, Any]:
        """
        标注图表元素
        """
        print(f"🏷️  标注图表元素: {image_path}")

        # 图表元素
        elements = {
            "title": {"x": 0, "y": 0, "w": 0, "h": 0},
            "x_axis": {"x": 0, "y": 0, "w": 0, "h": 0},
            "y_axis": {"x": 0, "y": 0, "w": 0, "h": 0},
            "legend": {"x": 0, "y": 0, "w": 0, "h": 0},
            "plot": {"x": 0, "y": 0, "w": 0, "h": 0}
        }

        # 标注
        annotation = {
            "image_path": image_path,
            "elements": elements
        }

        # 保存标注
        with open(self.labeled_dir / f"{Path(image_path).stem}_elements.json", "w", encoding="utf-8") as f:
            json.dump(annotation, f, ensure_ascii=False, indent=2)

        print(f"✅ 图表元素标注已保存到 {self.labeled_dir / f'{Path(image_path).stem}_elements.json'}")
        return annotation

    def annotate_text_content(self, image_path: str) -> Dict[str, Any]:
        """
        标注文本内容
        """
        print(f"🏷️  标注文本内容: {image_path}")

        # 文本内容
        text_content = {
            "title": "",
            "x_axis_label": "",
            "y_axis_label": "",
            "legend_texts": [],
            "data_values": []
        }

        # 标注
        annotation = {
            "image_path": image_path,
            "text_content": text_content
        }

        # 保存标注
        with open(self.labeled_dir / f"{Path(image_path).stem}_text.json", "w", encoding="utf-8") as f:
            json.dump(annotation, f, ensure_ascii=False, indent=2)

        print(f"✅ 文本内容标注已保存到 {self.labeled_dir / f'{Path(image_path).stem}_text.json'}")
        return annotation

    def annotate_all(self, image_paths: List[str]) -> Dict[str, Any]:
        """
        标注所有数据
        """
        print("🚀 开始数据标注...")

        annotations = {}
        for image_path in image_paths:
            annotations[image_path] = {
                "type": self.annotate_chart_type(image_path),
                "elements": self.annotate_chart_elements(image_path),
                "text": self.annotate_text_content(image_path)
            }

        # 保存汇总
        with open(self.labeled_dir / "all_annotations.json", "w", encoding="utf-8") as f:
            json.dump(annotations, f, ensure_ascii=False, indent=2)

        print(f"✅ 所有标注已保存到 {self.labeled_dir / 'all_annotations.json'}")
        return annotations

if __name__ == "__main__":
    annotator = DataAnnotator()

    # 示例图片路径
    image_paths = [
        "饼图示例.jpg",
        "柱状图示例.jpg",
        "折线图示例.jpg",
        "表格示例.jpg"
    ]

    annotations = annotator.annotate_all(image_paths)
    print("\n🎉 数据标注完成！")
