#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sugon-Scnet 文档智能 OCR 技能主脚本
接收命令行参数：[ocrType] fileUrl
ocrType 可选，默认为 DOC_PARSING
输出：识别结果的 JSON（内容与结果文件中的 JSON 结构完全一致）
"""

import os
import sys
import json
import time
import requests
from pathlib import Path

# 获取技能根目录（脚本所在目录的上一级）
SKILL_ROOT = Path(__file__).parent.parent.absolute()
ENV_FILE = SKILL_ROOT / "config" / ".env"

# --- 配置参数 ---
MAX_RETRIES = 3                     # 提交失败最大重试次数
RETRY_BACKOFF_FACTOR = 2            # 退避因子
INITIAL_RETRY_DELAY = 1             # 初始等待时间（秒）
POLL_INTERVAL = 2                   # 状态查询间隔（秒）
POLL_TIMEOUT = 600                  # 总轮询超时时间（秒）
# -----------------

def load_config():
    """从 .env 文件加载配置，若文件不存在则抛出友好错误"""
    if not ENV_FILE.exists():
        error_msg = (
            "\n===============================================\n"
            "Scnet OCR 配置文件不存在\n"
            "===============================================\n"
            "⚠️ 安全警告：切勿在聊天中直接粘贴 API Key！\n\n"
            "请按以下步骤安全配置：\n\n"
            "1. 申请 Scnet API Token：\n"
            "   访问 https://www.scnet.cn 注册并获取密钥\n\n"
            "2. 配置 Token（选择一种方式）：\n"
            "   a) 环境变量（推荐）：\n"
            "      export SCNET_API_KEY='你的密钥'\n"
            "   b) 配置文件：\n"
            f"      mkdir -p {SKILL_ROOT}/config\n"
            f"      echo 'SCNET_API_KEY=你的密钥' > {ENV_FILE}\n"
            f"      chmod 600 {ENV_FILE}\n"
            "\n配置完成后重新运行。"
        )
        sys.exit(error_msg)

    config = {}
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

    api_key = config.get('SCNET_API_KEY', '')
    if not api_key or api_key == 'your_scnet_api_key_here':
        error_msg = (
            "\n===============================================\n"
            "Scnet API Key 未配置\n"
            "===============================================\n"
            "请按以下步骤配置：\n\n"
            "1. 申请 Scnet API Token：\n"
            "   访问 https://www.scnet.cn 注册并获取密钥\n\n"
            "2. 配置 Token：\n"
            f"   编辑 {ENV_FILE}\n"
            "   设置 SCNET_API_KEY=你的密钥\n"
        )
        sys.exit(error_msg)

    config.setdefault('SCNET_API_BASE', 'https://api.scnet.cn/api/llm/v1')
    return config

def submit_task(api_base, api_key, file_url, ocr_type, retry_count=0):
    """提交异步 OCR 任务，返回 task_id"""
    url = f"{api_base}/ocrdoc/submit"
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    payload = {
        'file_url': file_url
    }
    if ocr_type:
        payload['ocr_type'] = ocr_type

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
    except Exception as e:
        sys.exit(f"网络请求失败: {str(e)}")

    # 处理限流
    if response.status_code == 429:
        if retry_count >= MAX_RETRIES:
            sys.exit(f"错误: 请求被限流 (429)，已达到最大重试次数 {MAX_RETRIES}。请稍后再试。")
        retry_after = INITIAL_RETRY_DELAY * (RETRY_BACKOFF_FACTOR ** retry_count)
        sys.stderr.write(f"⚠️ 请求过于频繁，等待 {retry_after} 秒后重试... (第 {retry_count + 1}/{MAX_RETRIES} 次重试)\n")
        time.sleep(retry_after)
        return submit_task(api_base, api_key, file_url, ocr_type, retry_count + 1)

    if response.status_code != 200:
        # 处理 401/403
        if response.status_code in (401, 403):
            error_msg = (
                "\n===============================================\n"
                "Scnet API Token 无效或已过期\n"
                "===============================================\n"
                f"HTTP 状态码: {response.status_code}\n\n"
                "请更新 config/.env 中的 SCNET_API_KEY。"
            )
            sys.exit(error_msg)
        sys.exit(f"HTTP 错误 {response.status_code}: {response.text}")

    try:
        resp_json = response.json()
    except Exception:
        sys.exit(f"响应不是有效的 JSON: {response.text}")

    # 检查业务错误（不同错误格式处理）
    if 'error' in resp_json:
        error_info = resp_json['error']
        sys.exit(f"API 错误 [{error_info.get('code', 'unknown')}]: {error_info.get('message', '')}")
    if resp_json.get('code') not in (None, '200', '0'):
        sys.exit(f"API 错误 {resp_json.get('code')}: {resp_json.get('msg', '')}")

    # 提取 task_id
    data = resp_json.get('data', {})
    output = data.get('output', {})
    task_id = output.get('task_id')
    if not task_id:
        sys.exit(f"响应中未找到 task_id: {resp_json}")

    return task_id

def query_result(api_base, api_key, task_id):
    """查询单个任务状态，返回 (task_status, result_urls, error_msg)"""
    url = f"{api_base}/ocrdoc/result"
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    payload = {
        'task_ids': [task_id]
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
    except Exception as e:
        sys.exit(f"查询网络请求失败: {str(e)}")

    if response.status_code != 200:
        sys.exit(f"查询 HTTP 错误 {response.status_code}: {response.text}")

    try:
        resp_json = response.json()
    except Exception:
        sys.exit(f"查询响应不是 JSON: {response.text}")

    if 'error' in resp_json:
        error_info = resp_json['error']
        sys.exit(f"查询 API 错误 [{error_info.get('code', 'unknown')}]: {error_info.get('message', '')}")

    # 响应结构：data 是一个数组，每个元素包含 output
    data_list = resp_json.get('data', [])
    if not data_list:
        sys.exit(f"查询响应无 data 字段: {resp_json}")

    for item in data_list:
        output = item.get('output', {})
        if output.get('task_id') == task_id:
            task_status = output.get('task_status', 'unknown')
            results = output.get('results', [])
            error_code = output.get('error_code', '')
            error_message = output.get('error_message', '')
            return task_status, results, error_message

    # 未找到匹配的 task_id
    return 'unknown', [], f"未找到任务 {task_id} 的状态"

def download_result_json(url):
    """下载结果文件并返回解析后的 JSON 对象"""
    try:
        resp = requests.get(url, timeout=60)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        sys.exit(f"下载结果文件失败: {str(e)}")

def poll_until_complete(api_base, api_key, task_id):
    """轮询查询任务状态直到完成或超时"""
    start_time = time.time()
    while True:
        elapsed = time.time() - start_time
        if elapsed > POLL_TIMEOUT:
            sys.exit(f"错误: 任务处理超时（超过 {POLL_TIMEOUT} 秒），最后状态未知。请稍后手动查询 task_id={task_id}")

        task_status, results, error_msg = query_result(api_base, api_key, task_id)

        if task_status == 'succeeded':
            if not results:
                sys.exit("任务成功但未返回结果文件地址")
            # 下载并输出第一个结果文件的内容（通常只有一个）
            result_json = download_result_json(results[0])
            # 输出结果 JSON
            print(json.dumps(result_json, ensure_ascii=False, indent=2))
            return
        elif task_status == 'failed':
            sys.exit(f"任务失败: {error_msg}")
        elif task_status in ('pending', 'running'):
            sys.stderr.write(f"任务状态: {task_status}，等待 {POLL_INTERVAL} 秒后重新查询...\n")
            time.sleep(POLL_INTERVAL)
        else:
            sys.exit(f"未知任务状态: {task_status}")

def main():
    # 解析命令行参数：支持 "ocrType fileUrl" 或 "fileUrl"（默认 ocrType = DOC_PARSING）
    args = sys.argv[1:]
    if len(args) == 1:
        ocr_type = "DOC_PARSING"
        file_url = args[0]
    elif len(args) == 2:
        ocr_type = args[0]
        file_url = args[1]
    else:
        print("用法: python main.py [ocrType] <fileUrl>")
        print("  ocrType: 可选，默认为 DOC_PARSING（目前仅支持此值）")
        print("  fileUrl: 公网可访问的文件下载地址")
        sys.exit(1)

    # 简单校验 URL 格式
    if not file_url.startswith(('http://', 'https://')):
        sys.exit("错误: fileUrl 必须是公网可访问的 HTTP/HTTPS 地址，不支持本地文件路径。")

    config = load_config()
    api_base = config['SCNET_API_BASE']
    api_key = config['SCNET_API_KEY']

    # 提交任务
    sys.stderr.write(f"正在提交任务，文件 URL: {file_url}\n")
    task_id = submit_task(api_base, api_key, file_url, ocr_type)
    sys.stderr.write(f"任务提交成功，task_id: {task_id}\n")

    # 轮询结果
    poll_until_complete(api_base, api_key, task_id)

if __name__ == '__main__':
    main()