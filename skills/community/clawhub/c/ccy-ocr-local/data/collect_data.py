#!/usr/bin/env python3
"""
数据收集脚本
用于收集图表数据集，包括公开数据集、内部数据集和合成数据集
"""

import os
import json
import shutil
from pathlib import Path
from typing import Dict, List, Any

class DataCollector:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.raw_dir = self.data_dir / "raw"
        self.labeled_dir = self.data_dir / "labeled"
        self.synthetic_dir = self.data_dir / "synthetic"

        # 创建目录
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.labeled_dir.mkdir(parents=True, exist_ok=True)
        self.synthetic_dir.mkdir(parents=True, exist_ok=True)

    def collect_public_data(self) -> Dict[str, Any]:
        """
        收集公开数据集
        """
        print("📊 收集公开数据集...")

        # ICDAR 2019
        icdar_2019 = {
            "name": "ICDAR 2019",
            "url": "https://rrc.cvc.uab.es/?ch=14&com=downloads",
            "description": "ICDAR 2019 图表识别挑战赛数据集",
            "size": "约 1000 张图表",
            "types": ["饼图", "柱状图", "折线图", "表格"],
            "format": "PNG",
            "license": "CC BY 4.0"
        }

        # ICDAR 2021
        icdar_2021 = {
            "name": "ICDAR 2021",
            "url": "https://rrc.cvc.uab.es/?ch=15&com=downloads",
            "description": "ICDAR 2021 图表识别挑战赛数据集",
            "size": "约 1500 张图表",
            "types": ["饼图", "柱状图", "折线图", "表格", "散点图"],
            "format": "PNG",
            "license": "CC BY 4.0"
        }

        public_data = {
            "icdar_2019": icdar_2019,
            "icdar_2021": icdar_2021
        }

        # 保存元数据
        with open(self.raw_dir / "public_data.json", "w", encoding="utf-8") as f:
            json.dump(public_data, f, ensure_ascii=False, indent=2)

        print(f"✅ 公开数据集元数据已保存到 {self.raw_dir / 'public_data.json'}")
        return public_data

    def collect_internal_data(self) -> Dict[str, Any]:
        """
        收集内部数据集
        """
        print("📊 收集内部数据集...")

        # 用户提供的图表截图
        internal_data = {
            "name": "内部数据集",
            "description": "用户提供的图表截图",
            "size": "未知",
            "types": ["饼图", "柱状图", "折线图", "表格"],
            "format": "PNG/JPG",
            "license": "私有"
        }

        # 保存元数据
        with open(self.raw_dir / "internal_data.json", "w", encoding="utf-8") as f:
            json.dump(internal_data, f, ensure_ascii=False, indent=2)

        print(f"✅ 内部数据集元数据已保存到 {self.raw_dir / 'internal_data.json'}")
        return internal_data

    def generate_synthetic_data(self, count: int = 100) -> Dict[str, Any]:
        """
        生成合成数据集
        """
        print(f"📊 生成合成数据集 ({count} 张图表)...")

        synthetic_data = {
            "name": "合成数据集",
            "description": "基于模板生成的图表",
            "size": f"{count} 张图表",
            "types": ["饼图", "柱状图", "折线图", "表格"],
            "format": "PNG",
            "license": "MIT"
        }

        # 保存元数据
        with open(self.synthetic_dir / "synthetic_data.json", "w", encoding="utf-8") as f:
            json.dump(synthetic_data, f, ensure_ascii=False, indent=2)

        print(f"✅ 合成数据集元数据已保存到 {self.synthetic_dir / 'synthetic_data.json'}")
        return synthetic_data

    def collect_all_data(self) -> Dict[str, Any]:
        """
        收集所有数据集
        """
        print("🚀 开始数据收集...")

        public_data = self.collect_public_data()
        internal_data = self.collect_internal_data()
        synthetic_data = self.generate_synthetic_data()

        # 汇总
        all_data = {
            "public": public_data,
            "internal": internal_data,
            "synthetic": synthetic_data
        }

        # 保存汇总
        with open(self.data_dir / "all_data.json", "w", encoding="utf-8") as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)

        print(f"✅ 所有数据集元数据已保存到 {self.data_dir / 'all_data.json'}")
        return all_data

if __name__ == "__main__":
    collector = DataCollector()
    all_data = collector.collect_all_data()
    print("\n🎉 数据收集完成！")
