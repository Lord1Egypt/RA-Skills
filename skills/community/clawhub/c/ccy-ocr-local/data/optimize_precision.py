#!/usr/bin/env python3
"""
精度优化脚本
用于优化 Tesseract OCR 模型和 OpenCV 图表解析模型的精度
"""

import os
import json
import time
from pathlib import Path
from typing import Dict, List, Any

class PrecisionOptimizer:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.precision_dir = self.data_dir / "precision"

        # 创建目录
        self.precision_dir.mkdir(parents=True, exist_ok=True)

    def optimize_tesseract_precision(self, model_name: str, config_path: str) -> Dict[str, Any]:
        """
        优化 Tesseract 精度
        """
        print(f"📊 优化 Tesseract 精度: {model_name}")

        # 优化参数
        optimization_params = {
            "model_name": model_name,
            "config_path": config_path,
            "optimization": {
                "lstm_model": True,
                "lstm_layers": 3,
                "lstm_hidden_size": 256,
                "lstm_dropout": 0.1,
                "lstm_learning_rate": 0.001,
                "lstm_batch_size": 32,
                "lstm_epochs": 100
            }
        }

        # 保存优化参数
        optimize_path = self.precision_dir / f"{model_name}_precision.json"
        with open(optimize_path, "w", encoding="utf-8") as f:
            json.dump(optimization_params, f, ensure_ascii=False, indent=2)

        print(f"✅ Tesseract 精度优化参数已保存: {optimize_path}")
        return optimization_params

    def optimize_opencv_precision(self, model_name: str, model_path: str) -> Dict[str, Any]:
        """
        优化 OpenCV 精度
        """
        print(f"📊 优化 OpenCV 精度: {model_name}")

        # 优化参数
        optimization_params = {
            "model_name": model_name,
            "model_path": model_path,
            "optimization": {
                "morphology": True,
                "morphology_kernel": 3,
                "morphology_iterations": 2,
                "threshold": True,
                "threshold_method": "adaptive",
                "threshold_block_size": 11,
                "threshold_c": 2
            }
        }

        # 保存优化参数
        optimize_path = self.precision_dir / f"{model_name}_precision.json"
        with open(optimize_path, "w", encoding="utf-8") as f:
            json.dump(optimization_params, f, ensure_ascii=False, indent=2)

        print(f"✅ OpenCV 精度优化参数已保存: {optimize_path}")
        return optimization_params

    def optimize_all_precision(self) -> Dict[str, Any]:
        """
        优化所有精度
        """
        print("🚀 开始优化精度...")

        # 优化 Tesseract 精度
        tesseract_models = {
            "digit": "data/config/digit.config",
            "axis": "data/config/axis.config",
            "legend": "data/config/legend.config",
            "title": "data/config/title.config"
        }

        optimized_tesseract = {}
        for model_name, config_path in tesseract_models.items():
            optimize_params = self.optimize_tesseract_precision(model_name, config_path)
            optimized_tesseract[model_name] = optimize_params

        # 优化 OpenCV 精度
        opencv_models = {
            "chart_detection": "data/models/chart_detection.pb",
            "line_detection": "data/models/line_detection.pb",
            "shape_detection": "data/models/shape_detection.pb"
        }

        optimized_opencv = {}
        for model_name, model_path in opencv_models.items():
            optimize_params = self.optimize_opencv_precision(model_name, model_path)
            optimized_opencv[model_name] = optimize_params

        # 汇总
        all_optimized = {
            "tesseract": optimized_tesseract,
            "opencv": optimized_opencv
        }

        # 保存汇总
        with open(self.precision_dir / "all_precision.json", "w", encoding="utf-8") as f:
            json.dump(all_optimized, f, ensure_ascii=False, indent=2)

        print(f"✅ 所有精度优化参数已保存到 {self.precision_dir / 'all_precision.json'}")

        # 优化信息
        optimize_info = {
            "tesseract_models": list(optimized_tesseract.keys()),
            "opencv_models": list(optimized_opencv.keys()),
            "total_models": len(optimized_tesseract) + len(optimized_opencv)
        }

        return optimize_info

if __name__ == "__main__":
    optimizer = PrecisionOptimizer()
    optimize_info = optimizer.optimize_all_precision()
    print("\n🎉 精度优化完成！")
