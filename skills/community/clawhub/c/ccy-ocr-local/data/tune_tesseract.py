#!/usr/bin/env python3
"""
Tesseract 参数调优脚本
用于调优 Tesseract 参数，提高 OCR 精度
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any

class TesseractTuner:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.tuning_dir = self.data_dir / "tuning"

        # 创建目录
        self.tuning_dir.mkdir(parents=True, exist_ok=True)

    def tune_parameters(self) -> Dict[str, Any]:
        """
        调优参数
        """
        print("📊 调优 Tesseract 参数...")

        # 参数列表
        parameters = {
            "digit": {
                "tessedit_char_whitelist": "0123456789.,-%",
                "tessedit_pageseg_mode": "6",
                "tessedit_ocr_engine_mode": "1",
                "tessedit_min_confidence": "60",
                "tessedit_max_variance": "0.3"
            },
            "axis": {
                "tessedit_char_whitelist": "0123456789.,-%abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
                "tessedit_pageseg_mode": "7",
                "tessedit_ocr_engine_mode": "1",
                "tessedit_min_confidence": "60",
                "tessedit_max_variance": "0.3"
            },
            "legend": {
                "tessedit_char_whitelist": "0123456789.,-%abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ:：",
                "tessedit_pageseg_mode": "8",
                "tessedit_ocr_engine_mode": "1",
                "tessedit_min_confidence": "60",
                "tessedit_max_variance": "0.3"
            },
            "title": {
                "tessedit_char_whitelist": "0123456789.,-%abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ:：",
                "tessedit_pageseg_mode": "6",
                "tessedit_ocr_engine_mode": "1",
                "tessedit_min_confidence": "60",
                "tessedit_max_variance": "0.3"
            }
        }

        # 保存参数
        for param_name, param_values in parameters.items():
            param_path = self.tuning_dir / f"{param_name}_params.json"
            with open(param_path, "w", encoding="utf-8") as f:
                json.dump(param_values, f, ensure_ascii=False, indent=2)
            print(f"✅ {param_name} 参数已保存到 {param_path}")

        # 保存汇总
        with open(self.tuning_dir / "all_params.json", "w", encoding="utf-8") as f:
            json.dump(parameters, f, ensure_ascii=False, indent=2)

        print(f"✅ 所有参数已保存到 {self.tuning_dir / 'all_params.json'}")
        return parameters

    def generate_config_strings(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成配置字符串
        """
        print("📊 生成配置字符串...")

        config_strings = {}
        for param_name, param_values in parameters.items():
            config_parts = []
            for key, value in param_values.items():
                config_parts.append(f"-c {key}={value}")
            config_strings[param_name] = " ".join(config_parts)

        # 保存配置字符串
        with open(self.tuning_dir / "config_strings.json", "w", encoding="utf-8") as f:
            json.dump(config_strings, f, ensure_ascii=False, indent=2)

        print(f"✅ 配置字符串已保存到 {self.tuning_dir / 'config_strings.json'}")
        return config_strings

    def tune_all(self) -> Dict[str, Any]:
        """
        调优所有参数
        """
        print("🚀 开始调优 Tesseract 参数...")

        # 调优参数
        parameters = self.tune_parameters()

        # 生成配置字符串
        config_strings = self.generate_config_strings(parameters)

        # 汇总
        tuning_results = {
            "parameters": parameters,
            "config_strings": config_strings
        }

        # 保存汇总
        with open(self.tuning_dir / "tuning_results.json", "w", encoding="utf-8") as f:
            json.dump(tuning_results, f, ensure_ascii=False, indent=2)

        print(f"✅ 调优结果已保存到 {self.tuning_dir / 'tuning_results.json'}")
        return tuning_results

if __name__ == "__main__":
    tuner = TesseractTuner()
    tuning_results = tuner.tune_all()
    print("\n🎉 Tesseract 参数调优完成！")
