#!/usr/bin/env python3
"""
Tesseract 配置优化脚本
用于优化 Tesseract 配置，提高 OCR 精度
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Any

class TesseractOptimizer:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.config_dir = self.data_dir / "config"
        self.results_dir = self.data_dir / "results"

        # 创建目录
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.results_dir.mkdir(parents=True, exist_ok=True)

    def optimize_config(self, config_name: str, config_content: str) -> Dict[str, Any]:
        """
        优化配置
        """
        print(f"📊 优化配置: {config_name}")

        # 保存配置
        config_path = self.config_dir / f"{config_name}.config"
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(config_content)

        # 配置信息
        config_info = {
            "name": config_name,
            "path": str(config_path),
            "content": config_content
        }

        print(f"✅ 配置已保存到 {config_path}")
        return config_info

    def test_config(self, config_name: str, config_path: str, test_text: str) -> Dict[str, Any]:
        """
        测试配置
        """
        print(f"📊 测试配置: {config_name}")

        # 测试命令
        cmd = [
            "tesseract",
            "--psm", "6",
            "--oem", "1",
            "--tessdata-dir", "/usr/share/tesseract-ocr/4.00/tessdata",
            "--user-words", config_path,
            "--user-patterns", config_path,
            "stdin",
            "stdout"
        ]

        try:
            # 运行测试命令
            result = subprocess.run(cmd, input=test_text, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                print(f"✅ 配置测试成功: {result.stdout.strip()}")
                return {
                    "name": config_name,
                    "success": True,
                    "output": result.stdout.strip(),
                    "error": ""
                }
            else:
                print(f"❌ 配置测试失败: {result.stderr}")
                return {
                    "name": config_name,
                    "success": False,
                    "output": "",
                    "error": result.stderr
                }

        except subprocess.TimeoutExpired:
            print(f"❌ 配置测试超时")
            return {
                "name": config_name,
                "success": False,
                "output": "",
                "error": "Timeout"
            }
        except Exception as e:
            print(f"❌ 配置测试出错: {e}")
            return {
                "name": config_name,
                "success": False,
                "output": "",
                "error": str(e)
            }

    def optimize_all_configs(self) -> Dict[str, Any]:
        """
        优化所有配置
        """
        print("🚀 开始优化 Tesseract 配置...")

        # 配置列表
        configs = {
            "digit": {
                "content": """tessedit_char_whitelist=0123456789.,-%
tessedit_pageseg_mode=6
""",
                "test_text": "123.45%"
            },
            "axis": {
                "content": """tessedit_char_whitelist=0123456789.,-%abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
tessedit_pageseg_mode=7
""",
                "test_text": "X轴 Y轴"
            },
            "legend": {
                "content": """tessedit_char_whitelist=0123456789.,-%abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ:：
tessedit_pageseg_mode=8
""",
                "test_text": "类别A: 100"
            },
            "title": {
                "content": """tessedit_char_whitelist=0123456789.,-%abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ:：
tessedit_pageseg_mode=6
""",
                "test_text": "图表标题"
            }
        }

        # 优化配置
        optimized_configs = {}
        for config_name, config_data in configs.items():
            config_info = self.optimize_config(config_name, config_data["content"])
            test_result = self.test_config(config_name, config_info["path"], config_data["test_text"])
            optimized_configs[config_name] = {
                "config": config_info,
                "test": test_result
            }

        # 保存结果
        with open(self.results_dir / "optimized_configs.json", "w", encoding="utf-8") as f:
            json.dump(optimized_configs, f, ensure_ascii=False, indent=2)

        print(f"✅ 所有配置已保存到 {self.results_dir / 'optimized_configs.json'}")
        return optimized_configs

if __name__ == "__main__":
    optimizer = TesseractOptimizer()
    optimized_configs = optimizer.optimize_all_configs()
    print("\n🎉 Tesseract 配置优化完成！")
