#!/usr/bin/env python3
"""
汉字书法字体识别脚本
调用书法识别API进行书法字体识别
支持多个API源：
1. 镜像站: https://xjf123.dy.takin.cc (推荐，无需Token)
2. HuggingFace Space: https://jfxia-shufa.hf.space
"""

import os
import sys
import argparse
import requests
from typing import Dict, List, Optional
import json
import base64


class CalligraphyRecognizer:
    """书法字体识别器"""
    
    # 支持的字体类型
    FONT_TYPES = [
        "楷书", "行书", "草书", 
        "篆书", "隶书"
    ]
    
    def __init__(self, api_token: Optional[str] = None):
        """
        初始化识别器
        
        Args:
            api_token: HuggingFace API Token (可选)
        """
        self.api_token = api_token or os.environ.get("HF_TOKEN")
        
        # API 地址列表（按优先级排序）
        self.api_endpoints = [
            # 镜像站 (推荐，无速率限制)
            "https://xjf123.dy.takin.cc/upload",
            # HuggingFace Space
            "https://jfxia-shufa.hf.space/run/predict",
        ]
    
    def recognize_from_file(self, image_path: str) -> Dict:
        """
        从图片文件识别书法字体
        
        Args:
            image_path: 图片文件路径
            
        Returns:
            识别结果字典
        """
        if not os.path.exists(image_path):
            return {
                "success": False,
                "error": f"图片文件不存在: {image_path}"
            }
        
        try:
            with open(image_path, "rb") as f:
                image_data = f.read()
            
            return self._call_api(image_data)
            
        except Exception as e:
            return {
                "success": False,
                "error": f"读取图片失败: {str(e)}"
            }
    
    def recognize_from_url(self, image_url: str) -> Dict:
        """
        从 URL 识别书法字体
        
        Args:
            image_url: 图片 URL
            
        Returns:
            识别结果字典
        """
        try:
            # 下载图片
            response = requests.get(image_url, timeout=30)
            if response.status_code != 200:
                return {
                    "success": False,
                    "error": f"下载图片失败: HTTP {response.status_code}"
                }
            
            image_data = response.content
            return self._call_api(image_data)
            
        except Exception as e:
            return {
                "success": False,
                "error": f"下载图片失败: {str(e)}"
            }
    
    def _call_api(self, image_data: bytes) -> Dict:
        """调用 API 进行识别"""
        
        # 尝试镜像站 (推荐)
        try:
            result = self._call_mirror_api(image_data)
            if result.get("success"):
                return result
        except Exception as e:
            print(f"镜像站调用失败: {e}", file=sys.stderr)
        
        # 尝试 HuggingFace Space
        try:
            result = self._call_hf_space_api(image_data)
            if result.get("success"):
                return result
        except Exception as e:
            print(f"HuggingFace Space 调用失败: {e}", file=sys.stderr)
        
        return {
            "success": False,
            "error": "所有 API 调用均失败"
        }
    
    def _call_mirror_api(self, image_data: bytes) -> Dict:
        """调用镜像站 API"""
        
        url = "https://xjf123.dy.takin.cc/upload"
        
        files = {"file": image_data}
        
        response = requests.post(url, files=files, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            return self._parse_mirror_result(data)
        else:
            raise Exception(f"HTTP {response.status_code}")
    
    def _call_hf_space_api(self, image_data: bytes) -> Dict:
        """调用 HuggingFace Space API"""
        
        # 将图片转换为 base64
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        # 构建请求
        url = "https://jfxia-shufa.hf.space/run/predict"
        payload = {
            "data": [f"data:image/png;base64,{image_base64}"]
        }
        
        headers = {"Content-Type": "application/json"}
        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"
        
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            return self._parse_hf_result(result)
        else:
            raise Exception(f"HTTP {response.status_code}")
    
    def _parse_mirror_result(self, result: List) -> Dict:
        """解析镜像站返回结果"""
        
        try:
            if not result or len(result) == 0:
                return {
                    "success": False,
                    "error": "返回结果为空"
                }
            
            # 解析结果列表
            all_results = []
            for item in result:
                char = item.get("char", "")
                prob_str = item.get("prob", "0%").replace("%", "")
                try:
                    prob = float(prob_str) / 100
                except:
                    prob = 0.0
                all_results.append({
                    "char": char,
                    "confidence": prob
                })
            
            return {
                "success": True,
                "char": all_results[0]["char"],
                "confidence": all_results[0]["confidence"],
                "all_results": all_results,
                "raw_result": result
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"解析结果失败: {str(e)}"
            }
    
    def _parse_hf_result(self, result: Dict) -> Dict:
        """解析 HuggingFace 返回结果"""
        
        try:
            # Gradio 返回格式: {"data": [...]}
            if "data" in result and len(result["data"]) > 0:
                first_result = result["data"][0]
                
                if isinstance(first_result, dict):
                    label = first_result.get("label", "")
                    confidences = first_result.get("confidences", [])
                    
                    confidence = 0.0
                    if confidences and len(confidences) > 0:
                        confidence = confidences[0].get("confidence", confidences[0].get("score", 0))
                    
                    return {
                        "success": True,
                        "font_type": label,
                        "confidence": confidence,
                        "all_results": confidences,
                        "raw_result": result
                    }
            
            return {
                "success": False,
                "error": "无法解析识别结果"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"解析结果失败: {str(e)}"
            }
    
    def print_result(self, result: Dict) -> None:
        """打印识别结果"""
        if result.get("success"):
            print(f"✓ 识别成功")
            print(f"  汉字: {result.get('char', result.get('font_type', 'N/A'))}")
            print(f"  置信度: {result['confidence']:.2%}")
            if "all_results" in result and result["all_results"]:
                print(f"\n  备选结果:")
                for r in result["all_results"][:5]:
                    label = r.get("char", r.get("label", r.get("class", "")))
                    score = r.get("confidence", r.get("score", 0))
                    print(f"    - {label}: {score:.2%}")
        else:
            print(f"✗ 识别失败")
            print(f"  错误信息: {result.get('error', '未知错误')}")
        
        # 打印原始结果（调试用）
        if "--verbose" in sys.argv or "-v" in sys.argv:
            print(f"\n原始结果:")
            print(json.dumps(result.get("raw_result", {}), indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="汉字书法字体识别")
    parser.add_argument("image", help="图片文件路径或图片URL")
    parser.add_argument("-t", "--token", help="HuggingFace API Token")
    parser.add_argument("-v", "--verbose", action="store_true", help="显示详细信息")
    
    args = parser.parse_args()
    
    recognizer = CalligraphyRecognizer(args.token)
    
    # 判断是文件还是 URL
    if args.image.startswith("http://") or args.image.startswith("https://"):
        result = recognizer.recognize_from_url(args.image)
    else:
        result = recognizer.recognize_from_file(args.image)
    
    recognizer.print_result(result)
    
    # 返回状态码
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
