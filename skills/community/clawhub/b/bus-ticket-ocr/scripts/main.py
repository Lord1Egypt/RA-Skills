#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sugon-Scnet 汽车票 OCR 技能主脚本
接收命令行参数：ocrType filePath
输出：识别结果的 JSON
"""

import os
import sys
import json
import time
import requests
import mimetypes
from pathlib import Path

# 获取技能根目录（脚本所在目录的上一级）
SKILL_ROOT = Path(__file__).parent.parent.absolute()
ENV_FILE = SKILL_ROOT / "config" / ".env"

# --- 新增：重试配置 ---
MAX_RETRIES = 3            # 最大重试次数
RETRY_BACKOFF_FACTOR = 2   # 退避因子，每次重试等待时间翻倍
INITIAL_RETRY_DELAY = 1    # 初始等待时间（秒）
# --------------------

def load_config():
    """从环境变量或 .env 文件加载配置，环境变量优先"""
    config = {}

    # 1. 如果 config/.env 存在，先加载其中的变量
    if ENV_FILE.exists():
        with open(ENV_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    config[key] = value

    # 2. 从系统环境变量读取，覆盖 .env 中的同名变量
    env_api_key = os.environ.get('SCNET_API_KEY')
    if env_api_key:
        config['SCNET_API_KEY'] = env_api_key

    env_api_base = os.environ.get('SCNET_API_BASE')
    if env_api_base:
        config['SCNET_API_BASE'] = env_api_base

    # 3. 设置默认值
    config.setdefault('SCNET_API_BASE', 'https://api.scnet.cn/api/llm/v1')

    # 4. 检查必要配置
    api_key = config.get('SCNET_API_KEY', '')
    if not api_key or api_key == 'your_scnet_api_key_here':
        error_msg = (
            "\n===============================================\n"
            "Scnet API Key 未配置\n"
            "===============================================\n"
            "⚠️ 安全警告：切勿在聊天中粘贴 API Key！\n\n"
            "请通过以下任一方式设置 SCNET_API_KEY：\n\n"
            "1. 环境变量（推荐）：\n"
            "   export SCNET_API_KEY='你的真实密钥'\n\n"
            "2. 配置文件：\n"
            f"   mkdir -p {SKILL_ROOT}/config\n"
            f"   echo 'SCNET_API_KEY=你的真实密钥' > {ENV_FILE}\n"
            f"   chmod 600 {ENV_FILE}\n"
        )
        sys.exit(error_msg)

    return config

def recognize_with_retry(ocr_type, file_path, config, retry_count=0):
    """
    带重试机制的 OCR 识别函数。
    当遇到 429 (Too Many Requests) 时，自动等待后重试。
    """
    api_base = config['SCNET_API_BASE']
    api_key = config['SCNET_API_KEY']
    url = f"{api_base}/ocr/recognize"

    # 检查文件是否存在
    if not os.path.isfile(file_path):
        sys.exit(f"错误: 文件不存在 - {file_path}")

    # 自动检测 MIME 类型
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        mime_type = 'application/octet-stream'

    headers = {
        'Authorization': f'Bearer {api_key}'
    }

    try:
        with open(file_path, 'rb') as f:
            files = {
                'file': (os.path.basename(file_path), f, mime_type)
            }
            data = {
                'ocrType': ocr_type,
                'channelTag': "scnetSkills"
            }
            response = requests.post(url, headers=headers, data=data, files=files, timeout=60)
    except Exception as e:
        sys.exit(f"网络请求失败: {str(e)}")

    # --- 新增：处理 429 速率限制 ---
    if response.status_code == 429:
        if retry_count >= MAX_RETRIES:
            sys.exit(f"错误: 请求被限流 (429)，已达到最大重试次数 {MAX_RETRIES}。请稍后再试。")

        # 尝试从响应中获取重试等待时间（如果有）
        retry_after = INITIAL_RETRY_DELAY * (RETRY_BACKOFF_FACTOR ** retry_count)
        try:
            error_data = response.json()
            # 某些 API 会在响应中返回 retry_after 字段
            if 'retry_after' in error_data:
                retry_after = int(error_data['retry_after'])
        except:
            pass

        # 输出友好提示到 stderr（不影响 JSON 输出）
        sys.stderr.write(f"⚠️ 请求过于频繁，等待 {retry_after} 秒后重试... (第 {retry_count+1}/{MAX_RETRIES} 次重试)\n")
        time.sleep(retry_after)

        # 递归重试
        return recognize_with_retry(ocr_type, file_path, config, retry_count + 1)
    # ---------------------------------

    if response.status_code != 200:
        # 针对 401/403 给出明确提示
        if response.status_code in (401, 403):
            error_msg = (
                "\n===============================================\n"
                "Scnet API Token 无效或已过期\n"
                "===============================================\n"
                f"HTTP 状态码: {response.status_code}\n\n"
                "⚠️ 安全警告：切勿在聊天中粘贴 API Key！\n\n"
                "解决方法：\n"
                "1. 访问 https://www.scnet.cn 重新申请 Token\n"
                "2. 手动更新配置文件：\n"
                f"   编辑 {ENV_FILE}\n"
                "   设置 SCNET_API_KEY=你的新密钥\n"
                "3. 或设置环境变量：export SCNET_API_KEY='你的新密钥'\n"
            )
            sys.exit(error_msg)
        else:
            sys.exit(f"HTTP 错误 {response.status_code}: {response.text}")

    try:
        result = response.json()
    except Exception:
        sys.exit(f"响应不是有效的 JSON: {response.text}")

    # 检查业务状态码
    if result.get('code') != '0':
        sys.exit(f"API 错误 {result.get('code')}: {result.get('msg')}")

    # 输出 data 部分（识别结果）
    data = result.get('data', [])

    # 移除每个识别项中的 confidence 字段（优化点）
    for file_result in data:
        if 'result' in file_result and isinstance(file_result['result'], list):
            for item in file_result['result']:
                item.pop('confidence', None)

    # 输出处理后的数据
    print(json.dumps(data, ensure_ascii=False, indent=2))

def main():
    if len(sys.argv) != 3:
        print("用法: python main.py <ocrType> <filePath>")
        print("ocrType 可选值: BUS_TICKET")
        sys.exit(1)

    ocr_type = sys.argv[1]
    file_path = sys.argv[2]

    config = load_config()
    # 调用带重试的识别函数
    recognize_with_retry(ocr_type, file_path, config)

if __name__ == '__main__':
    main()
