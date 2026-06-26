#!/usr/bin/env python3
"""
模型部署脚本
用于部署 Tesseract OCR 模型和 OpenCV 图表解析模型
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Any

class ModelDeployer:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.deploy_dir = self.data_dir / "deploy"
        self.models_dir = self.data_dir / "models"

        # 创建目录
        self.deploy_dir.mkdir(parents=True, exist_ok=True)

    def deploy_tesseract_model(self, model_name: str, config_path: str) -> Dict[str, Any]:
        """
        部署 Tesseract 模型
        """
        print(f"📊 部署 Tesseract 模型: {model_name}")

        # 模型信息
        model_info = {
            "name": model_name,
            "type": "tesseract",
            "config_path": config_path,
            "deployed": True
        }

        # 保存模型信息
        model_info_path = self.deploy_dir / f"{model_name}_info.json"
        with open(model_info_path, "w", encoding="utf-8") as f:
            json.dump(model_info, f, ensure_ascii=False, indent=2)

        print(f"✅ Tesseract 模型已部署: {model_info_path}")
        return model_info

    def deploy_opencv_model(self, model_name: str, model_path: str) -> Dict[str, Any]:
        """
        部署 OpenCV 模型
        """
        print(f"📊 部署 OpenCV 模型: {model_name}")

        # 模型信息
        model_info = {
            "name": model_name,
            "type": "opencv",
            "model_path": model_path,
            "deployed": True
        }

        # 保存模型信息
        model_info_path = self.deploy_dir / f"{model_name}_info.json"
        with open(model_info_path, "w", encoding="utf-8") as f:
            json.dump(model_info, f, ensure_ascii=False, indent=2)

        print(f"✅ OpenCV 模型已部署: {model_info_path}")
        return model_info

    def deploy_all_models(self) -> Dict[str, Any]:
        """
        部署所有模型
        """
        print("🚀 开始部署模型...")

        # 部署 Tesseract 模型
        tesseract_models = {
            "digit": "data/config/digit.config",
            "axis": "data/config/axis.config",
            "legend": "data/config/legend.config",
            "title": "data/config/title.config"
        }

        deployed_tesseract = {}
        for model_name, config_path in tesseract_models.items():
            model_info = self.deploy_tesseract_model(model_name, config_path)
            deployed_tesseract[model_name] = model_info

        # 部署 OpenCV 模型
        opencv_models = {
            "chart_detection": "data/models/chart_detection.pb",
            "line_detection": "data/models/line_detection.pb",
            "shape_detection": "data/models/shape_detection.pb"
        }

        deployed_opencv = {}
        for model_name, model_path in opencv_models.items():
            model_info = self.deploy_opencv_model(model_name, model_path)
            deployed_opencv[model_name] = model_info

        # 汇总
        all_models = {
            "tesseract": deployed_tesseract,
            "opencv": deployed_opencv
        }

        # 保存汇总
        with open(self.deploy_dir / "all_models.json", "w", encoding="utf-8") as f:
            json.dump(all_models, f, ensure_ascii=False, indent=2)

        print(f"✅ 所有模型已保存到 {self.deploy_dir / 'all_models.json'}")

        # 部署信息
        deploy_info = {
            "tesseract_models": list(deployed_tesseract.keys()),
            "opencv_models": list(deployed_opencv.keys()),
            "total_models": len(deployed_tesseract) + len(deployed_opencv)
        }

        return deploy_info

if __name__ == "__main__":
    deployer = ModelDeployer()
    deploy_info = deployer.deploy_all_models()
    print("\n🎉 模型部署完成！")
