#!/usr/bin/env python3
"""
Tesseract 专用 OCR 模型训练脚本
用于训练数字、坐标轴、图例、标题专用 OCR 模型
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Any

class TesseractTrainer:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.training_dir = self.data_dir / "training"
        self.models_dir = self.data_dir / "models"

        # 创建目录
        self.training_dir.mkdir(parents=True, exist_ok=True)
        self.models_dir.mkdir(parents=True, exist_ok=True)

    def prepare_training_data(self) -> Dict[str, Any]:
        """
        准备训练数据
        """
        print("📊 准备训练数据...")

        # 读取合成数据
        synthetic_data_path = self.data_dir / "synthetic" / "all_synthetic_data.json"
        with open(synthetic_data_path, "r", encoding="utf-8") as f:
            synthetic_data = json.load(f)

        # 准备训练数据
        training_data = {
            "digit": [],
            "axis": [],
            "legend": [],
            "title": []
        }

        for chart in synthetic_data:
            chart_type = chart["type"]

            if chart_type == "饼图":
                # 数字数据
                for value in chart["values"]:
                    training_data["digit"].append(str(value))
                # 标题数据
                training_data["title"].append(chart["title"])
                # 图例数据
                for label in chart["labels"]:
                    training_data["legend"].append(label)

            elif chart_type == "柱状图":
                # 数字数据
                for value in chart["values"]:
                    training_data["digit"].append(str(value))
                # 标题数据
                training_data["title"].append(chart["title"])
                # 坐标轴数据
                training_data["axis"].append(chart["x_label"])
                training_data["axis"].append(chart["y_label"])
                # 类目数据
                for category in chart["categories"]:
                    training_data["legend"].append(category)

            elif chart_type == "折线图":
                # 数字数据
                for value in chart["y_values"]:
                    training_data["digit"].append(str(value))
                # 标题数据
                training_data["title"].append(chart["title"])
                # 坐标轴数据
                training_data["axis"].append(chart["x_label"])
                training_data["axis"].append(chart["y_label"])

            elif chart_type == "表格":
                # 标题数据
                training_data["title"].append(chart["title"])
                # 表头数据
                for header in chart["headers"]:
                    training_data["legend"].append(header)
                # 表格数据
                for row in chart["rows"]:
                    for cell in row:
                        training_data["digit"].append(str(cell))

        # 去重
        for key in training_data:
            training_data[key] = list(set(training_data[key]))

        # 保存训练数据
        with open(self.training_dir / "training_data.json", "w", encoding="utf-8") as f:
            json.dump(training_data, f, ensure_ascii=False, indent=2)

        print(f"✅ 训练数据已保存到 {self.training_dir / 'training_data.json'}")
        return training_data

    def generate_box_files(self, training_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成 box 文件
        """
        print("📊 生成 box 文件...")

        box_files = {}

        for data_type, texts in training_data.items():
            if not texts:
                continue

            box_file_path = self.training_dir / f"{data_type}.box"
            with open(box_file_path, "w", encoding="utf-8") as f:
                for i, text in enumerate(texts):
                    # 生成 box 文件内容
                    # 格式: char x y w h page
                    for j, char in enumerate(text):
                        x = j * 20
                        y = 0
                        w = 20
                        h = 30
                        page = 0
                        f.write(f"{char} {x} {y} {w} {h} {page}\n")

            box_files[data_type] = str(box_file_path)
            print(f"✅ {data_type} box 文件已生成: {box_file_path}")

        return box_files

    def train_tesseract_model(self, data_type: str, box_file: str) -> str:
        """
        训练 Tesseract 模型
        """
        print(f"📊 训练 {data_type} 模型...")

        # 模型名称
        model_name = f"chart_{data_type}"
        model_dir = self.models_dir / model_name
        model_dir.mkdir(parents=True, exist_ok=True)

        # 训练命令
        cmd = [
            "tesseract",
            "--psm", "6",
            "--oem", "1",
            "--tessdata-dir", "/usr/share/tesseract-ocr/4.00/tessdata",
            "--user-words", box_file,
            "--user-patterns", box_file,
            "--train", model_name,
            str(model_dir)
        ]

        try:
            # 运行训练命令
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            if result.returncode == 0:
                print(f"✅ {data_type} 模型训练成功: {model_dir}")
                return str(model_dir)
            else:
                print(f"❌ {data_type} 模型训练失败: {result.stderr}")
                return ""

        except subprocess.TimeoutExpired:
            print(f"❌ {data_type} 模型训练超时")
            return ""
        except Exception as e:
            print(f"❌ {data_type} 模型训练出错: {e}")
            return ""

    def train_all_models(self) -> Dict[str, Any]:
        """
        训练所有模型
        """
        print("🚀 开始训练 Tesseract 模型...")

        # 准备训练数据
        training_data = self.prepare_training_data()

        # 生成 box 文件
        box_files = self.generate_box_files(training_data)

        # 训练模型
        models = {}
        for data_type, box_file in box_files.items():
            model_dir = self.train_tesseract_model(data_type, box_file)
            if model_dir:
                models[data_type] = model_dir

        # 保存模型信息
        with open(self.models_dir / "models.json", "w", encoding="utf-8") as f:
            json.dump(models, f, ensure_ascii=False, indent=2)

        print(f"✅ 所有模型已保存到 {self.models_dir / 'models.json'}")
        return models

if __name__ == "__main__":
    trainer = TesseractTrainer()
    models = trainer.train_all_models()
    print("\n🎉 Tesseract 模型训练完成！")
