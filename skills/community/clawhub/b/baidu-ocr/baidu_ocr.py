#!/usr/bin/env python3
"""
百度 OCR 识别脚本
使用百度 AI 开放平台的通用文字识别 API

API 文档：https://ai.baidu.com/ai-doc/OCR/Ek3h7xypm
"""

import requests
import base64
import json
import sys
from pathlib import Path

# 百度 OCR 配置
API_KEY = "4LceeJ8wBDSqa3SqDHmgXuk1"
SECRET_KEY = "nIulIWxqaUtY5XyfexSvP4OL8ZBk0krR"

# 获取 access_token
def get_access_token():
    """获取百度 API 的 access_token"""
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": SECRET_KEY
    }
    
    response = requests.post(url, params=params)
    result = response.json()
    
    if "access_token" in result:
        return result["access_token"]
    else:
        print(f"错误：获取 access_token 失败 - {result}")
        return None

# 图片转 base64
def image_to_base64(image_path):
    """将图片转换为 base64 编码"""
    with open(image_path, "rb") as f:
        img_data = f.read()
        img_base64 = base64.b64encode(img_data).decode("utf-8")
    return img_base64

# 通用文字识别（高精度版）
def ocr_general_basic(image_base64, access_token):
    """
    通用文字识别（基础版）
    支持中英文混合识别
    API 文档：https://ai.baidu.com/ai-doc/OCR/Ek3h7xypm
    """
    # 使用新版 API 端点
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    url += f"?access_token={access_token}"
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "image": image_base64,
        "detect_direction": "true",
        "detect_language": "true"
    }
    
    response = requests.post(url, headers=headers, data=data)
    return response.json()

# 通用文字识别（含位置信息）
def ocr_general(image_base64, access_token):
    """
    通用文字识别（含位置信息）
    返回文字的位置坐标
    """
    url = f"https://aip.baidubce.com/rest/2.0/ocr/v1/general?access_token={access_token}"
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "image": image_base64,
        "language_type": "CHN_ENG",
        "detect_direction": "true",
        "detect_language": "true",
        "recognize_granularity": "big",  # 返回行级结果
        "probability": "false"
    }
    
    response = requests.post(url, headers=headers, data=data)
    return response.json()

# 表格文字识别
def ocr_table(image_base64, access_token):
    """
    表格文字识别
    识别表格结构和内容
    """
    url = f"https://aip.baidubce.com/rest/2.0/ocr/v1/table?access_token={access_token}"
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "image": image_base64,
        "recognize_granularity": "big"
    }
    
    response = requests.post(url, headers=headers, data=data)
    return response.json()

# 公式识别
def ocr_formula(image_base64, access_token):
    """
    公式识别
    专门识别数学公式
    """
    url = f"https://aip.baidubce.com/rest/2.0/ocr/v1/formula?access_token={access_token}"
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "image": image_base64
    }
    
    response = requests.post(url, headers=headers, data=data)
    return response.json()

# 输出结果
def format_result(result, format_type="text"):
    """格式化输出结果"""
    if "error_code" in result:
        print(f"❌ 错误：{result.get('error_msg', '未知错误')}")
        return None
    
    if "words_result" not in result:
        print("❌ 未识别到文字")
        return None
    
    words_list = result["words_result"]
    
    if format_type == "json":
        return json.dumps(words_list, ensure_ascii=False, indent=2)
    
    # 文本格式
    output_lines = []
    for item in words_list:
        words = item.get("words", "")
        if words.strip():
            output_lines.append(words)
    
    return "\n".join(output_lines)

# 主函数
def main():
    if len(sys.argv) < 2:
        print("用法：python3 baidu_ocr.py <图片路径> [输出格式]")
        print("示例：python3 baidu_ocr.py image.jpg")
        print("输出格式：text(默认), json")
        sys.exit(1)
    
    image_path = sys.argv[1]
    output_format = sys.argv[2] if len(sys.argv) > 2 else "text"
    
    # 检查文件存在
    if not Path(image_path).exists():
        print(f"❌ 文件不存在：{image_path}")
        sys.exit(1)
    
    print(f"📷 读取图片：{image_path}")
    
    # 获取 access_token
    print("🔑 获取 access_token...")
    access_token = get_access_token()
    if not access_token:
        sys.exit(1)
    print("✅ access_token 获取成功")
    
    # 图片转 base64
    image_base64 = image_to_base64(image_path)
    
    # 执行 OCR 识别（使用高精度版）
    print("🔍 执行 OCR 识别（高精度版）...")
    result = ocr_general_basic(image_base64, access_token)
    
    # 输出结果
    print("\n" + "="*60)
    print("识别结果:")
    print("="*60)
    
    formatted = format_result(result, output_format)
    if formatted:
        print(formatted)
        print("="*60)
        print(f"✅ 识别完成！共 {len(result.get('words_result', []))} 行")
    else:
        print("❌ 识别失败")
        sys.exit(1)

if __name__ == "__main__":
    main()
