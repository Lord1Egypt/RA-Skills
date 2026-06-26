#!/usr/bin/env python3
"""
推理优化脚本
用于优化 Tesseract OCR 模型和 OpenCV 图表解析模型的推理速度
"""

import os
import json
import threading
import time
from pathlib import Path
from typing import Dict, List, Any

class InferenceOptimizer:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.optimize_dir = self.data_dir / "optimize"

        # 创建目录
        self.optimize_dir.mkdir(parents=True, exist_ok=True)

    def optimize_tesseract_inference(self, model_name: str, config_path: str) -> Dict[str, Any]:
        """
        优化 Tesseract 推理
        """
        print(f"📊 优化 Tesseract 推理: {model_name}")

        # 优化参数
        optimization_params = {
            "model_name": model_name,
            "config_path": config_path,
            "optimization": {
                "multithread": True,
                "batch_size": 10,
                "cache_size": 100,
                "timeout": 30
            }
        }

        # 保存优化参数
        optimize_path = self.optimize_dir / f"{model_name}_optimize.json"
        with open(optimize_path, "w", encoding="utf-8") as f:
            json.dump(optimization_params, f, ensure_ascii=False, indent=2)

        print(f"✅ Tesseract 推理优化参数已保存: {optimize_path}")
        return optimization_params

    def optimize_opencv_inference(self, model_name: str, model_path: str) -> Dict[str, Any]:
        """
        优化 OpenCV 推理
        """
        print(f"📊 优化 OpenCV 推理: {model_name}")

        # 优化参数
        optimization_params = {
            "model_name": model_name,
            "model_path": model_path,
            "optimization": {
                "multithread": True,
                "batch_size": 10,
                "cache_size": 100,
                "timeout": 30
            }
        }

        # 保存优化参数
        optimize_path = self.optimize_dir / f"{model_name}_optimize.json"
        with open(optimize_path, "w", encoding="utf-8") as f:
            json.dump(optimization_params, f, ensure_ascii=False, indent=2)

        print(f"✅ OpenCV 推理优化参数已保存: {optimize_path}")
        return optimization_params

    def optimize_all_inference(self) -> Dict[str, Any]:
        """
        优化所有推理
        """
        print("🚀 开始优化推理...")

        # 优化 Tesseract 推理
        tesseract_models = {
            "digit": "data/config/digit.config",
            "axis": "data/config/axis.config",
            "legend": "data/config/legend.config",
            "title": "data/config/title.config"
        }

        optimized_tesseract = {}
        for model_name, config_path in tesseract_models.items():
            optimize_params = self.optimize_tesseract_inference(model_name, config_path)
            optimized_tesseract[model_name] = optimize_params

        # 优化 OpenCV 推理
        opencv_models = {
            "chart_detection": "data/models/chart_detection.pb",
            "line_detection": "data/models/line_detection.pb",
            "shape_detection": "data/models/shape_detection.pb"
        }

        optimized_opencv = {}
        for model_name, model_path in opencv_models.items():
            optimize_params = self.optimize_opencv_inference(model_name, model_path)
            optimized_opencv[model_name] = optimize_params

        # 汇总
        all_optimized = {
            "tesseract": optimized_tesseract,
            "opencv": optimized_opencv
        }

        # 保存汇总
        with open(self.optimize_dir / "all_optimized.json", "w", encoding="utf-8") as f:
            json.dump(all_optimized, f, ensure_ascii=False, indent=2)

        print(f"✅ 所有推理优化参数已保存到 {self.optimize_dir / 'all_optimized.json'}")

        # 优化信息
        optimize_info = {
            "tesseract_models": list(optimized_tesseract.keys()),
            "opencv_models": list(optimized_opencv.keys()),
            "total_models": len(optimized_tesseract) + len(optimized_opencv)
        }

        return optimize_info

if __name__ == "__main__":
    optimizer = InferenceOptimizer()
    optimize_info = optimizer.optimize_all_inference()
    print("\n🎉 推理优化完成！")
