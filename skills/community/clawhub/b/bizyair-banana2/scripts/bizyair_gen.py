#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BizyAir Banana 2 图像生成脚本
使用 BizyAir API 直接调用 Nano Banana 2 模型
支持文生图、图生图、表情包生成
"""

import requests
import json
import sys
import os
import time
import argparse
from datetime import datetime

# 配置
BIZYAIR_BASE_URL = "https://api.bizyair.cn"
BIZYAIR_API_KEY = os.environ.get("BIZYAIR_API_KEY")

# 默认工作流配置（从用户提供的示例）
DEFAULT_WEB_APP_ID = 47091  # Nano Banana 2 表情包生成

def get_api_key():
    """获取 API Key"""
    # 优先级：环境变量 > 技能目录.env > 用户目录.env > 报错
    if BIZYAIR_API_KEY:
        return BIZYAIR_API_KEY
    
    # 尝试从配置文件读取（通用路径）
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_dir = os.path.dirname(script_dir)
    
    config_paths = [
        # 优先使用技能目录下的.env（最通用）
        os.path.join(skill_dir, ".env"),
        # 兼容旧版本：脚本同目录
        os.path.join(script_dir, ".env"),
        # 用户目录配置（可选）
        os.path.expanduser("~/.config/bizyair-banana2/.env"),
        os.path.expanduser("~/.bizyair-banana2/.env"),
        # 兼容 baoyu 用户（如果有）
        os.path.expanduser("~/.baoyu-skills/bizyair-banana2/.env"),
    ]
    
    for path in config_paths:
        if os.path.exists(path):
            with open(path, 'r') as f:
                for line in f:
                    if line.startswith("BIZYAIR_API_KEY="):
                        return line.split("=", 1)[1].strip()
    
    return None

def upload_file(file_path):
    """
    上传文件到 BizyAir OSS
    返回 OSS URL
    """
    import base64
    import hmac
    import hashlib
    from urllib.parse import quote
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在：{file_path}")
    
    file_name = os.path.basename(file_path)
    print(f"📤 上传文件：{file_name}")
    
    # 步骤 1: 获取上传凭证
    token_url = f"{BIZYAIR_BASE_URL}/x/v1/upload/token"
    params = {
        "file_name": file_name,
        "file_type": "inputs"
    }
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    response = requests.get(token_url, params=params, headers=headers, timeout=30)
    if response.status_code != 200:
        raise Exception(f"获取上传凭证失败：{response.status_code} {response.text}")
    
    token_data = response.json()
    if not token_data.get("status"):
        raise Exception(f"获取上传凭证失败：{token_data.get('message')}")
    
    file_info = token_data["data"]["file"]
    storage_info = token_data["data"]["storage"]
    
    object_key = file_info['object_key']
    access_key_id = file_info['access_key_id']
    access_key_secret = file_info['access_key_secret']
    security_token = file_info['security_token']
    bucket = storage_info['bucket']
    endpoint = storage_info['endpoint']
    
    # 步骤 2: 构造 Policy
    import datetime
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    expiration_str = expiration.strftime('%Y-%m-%dT%H:%M:%SZ')
    
    policy_dict = {
        "expiration": expiration_str,
        "conditions": [
            {"bucket": bucket},
            ["starts-with", "$key", "inputs/"],
            {"x-oss-security-token": security_token},
        ]
    }
    
    policy_base64 = base64.b64encode(json.dumps(policy_dict).encode()).decode()
    
    # 计算 Signature
    signature = base64.b64encode(
        hmac.new(access_key_secret.encode(), policy_base64.encode(), hashlib.sha1).digest()
    ).decode()
    
    # 步骤 3: 上传到 OSS
    oss_url = f"https://{bucket}.{endpoint}"
    
    files = {
        'file': (file_name, open(file_path, 'rb'), 'image/png' if file_name.endswith('.png') else 'image/jpeg')
    }
    
    oss_data = {
        'key': object_key,
        'OSSAccessKeyId': access_key_id,
        'policy': policy_base64,
        'Signature': signature,
        'x-oss-security-token': security_token,
    }
    
    response = requests.post(oss_url, data=oss_data, files=files, timeout=60)
    if response.status_code != 204:
        raise Exception(f"OSS 上传失败：{response.status_code} {response.text}")
    
    print(f"✅ OSS 上传成功")
    
    # 步骤 4: 提交输入资源
    commit_url = f"{BIZYAIR_BASE_URL}/x/v1/input_resource/commit"
    commit_data = {
        "name": file_name,
        "object_key": object_key
    }
    
    response = requests.post(commit_url, json=commit_data, headers=headers, timeout=30)
    if response.status_code != 200:
        raise Exception(f"提交资源失败：{response.status_code} {response.text}")
    
    commit_result = response.json()
    if not commit_result.get("status"):
        raise Exception(f"提交资源失败：{commit_result.get('message')}")
    
    file_url = commit_result["data"]["url"]
    print(f"✅ 上传成功：{file_url}")
    
    return file_url

def submit_task(web_app_id, input_values, suppress_preview=False, timeout=120):
    """
    提交生成任务
    
    Args:
        web_app_id: Web 应用 ID（如 47091）
        input_values: 输入值字典，格式如 {"2:LoadImage.image": "url", ...}
        suppress_preview: 是否禁用预览
        timeout: 超时时间（秒）
    
    Returns:
        request_id: 任务 ID
    """
    url = f"{BIZYAIR_BASE_URL}/w/v1/webapp/task/openapi/create"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    data = {
        "web_app_id": web_app_id,
        "suppress_preview_output": suppress_preview,
        "input_values": input_values
    }
    
    print(f"🚀 提交任务到 Web App {web_app_id}...")
    response = requests.post(url, headers=headers, json=data, timeout=timeout)
    
    result = response.json()
    
    # 处理两种响应模式：
    # 1. 异步模式 (202): 返回 requestId
    # 2. 同步模式 (200): 直接返回完整结果
    if response.status_code == 202:
        request_id = result.get("requestId")
        print(f"📋 请求 ID: {request_id}")
        return request_id
    elif response.status_code == 200:
        # 同步模式，直接返回结果
        if result.get("status") == "Success":
            print(f"✅ 任务已完成！")
            request_id = result.get("request_id")
            # 直接保存输出
            outputs = result.get("outputs", [])
            if outputs:
                print(f"📊 输出数量：{len(outputs)}")
                return request_id
            return request_id
        else:
            raise Exception(f"任务失败：{result}")
    else:
        error_text = response.text
        raise Exception(f"提交任务失败：{response.status_code} {error_text}")

def query_task_status(request_id):
    """查询任务状态"""
    url = f"{BIZYAIR_BASE_URL}/w/v1/webapp/task/openapi/detail"
    params = {"requestId": request_id}
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    response = requests.get(url, params=params, headers=headers, timeout=30)
    if response.status_code != 200:
        raise Exception(f"查询状态失败：{response.status_code}")
    
    result = response.json()
    return result.get("data", {})

def get_task_outputs(request_id):
    """获取任务输出"""
    url = f"{BIZYAIR_BASE_URL}/w/v1/webapp/task/openapi/outputs"
    params = {"requestId": request_id}
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    response = requests.get(url, params=params, headers=headers, timeout=30)
    if response.status_code != 200:
        raise Exception(f"获取结果失败：{response.status_code}")
    
    result = response.json()
    return result.get("data", {}).get("outputs", [])

def wait_for_task(request_id, timeout=120, poll_interval=2):
    """
    轮询等待任务完成
    
    Args:
        request_id: 任务 ID
        timeout: 超时时间（秒）
        poll_interval: 轮询间隔（秒）
    
    Returns:
        任务状态数据
    """
    start_time = time.time()
    
    # 如果没有 request_id，返回空结果
    if not request_id:
        print("⚠️ 无任务 ID，跳过等待")
        return {"status": "Success", "outputs": []}
    
    while time.time() - start_time < timeout:
        status_data = query_task_status(request_id)
        status = status_data.get("status", "Unknown")
        
        print(f"⏳ 任务状态：{status}")
        
        if status == "Success":
            return status_data
        elif status in ["Failed", "Canceled"]:
            raise Exception(f"任务失败：{status_data}")
        
        time.sleep(poll_interval)
    
    raise Exception(f"任务超时（{timeout}秒）")

def download_file(url, output_path):
    """下载文件"""
    print(f"📥 下载结果：{output_path}")
    
    response = requests.get(url, stream=True, timeout=60)
    if response.status_code != 200:
        raise Exception(f"下载失败：{response.status_code}")
    
    # 确保目录存在
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    print(f"✅ 保存成功：{output_path}")

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="BizyAir Banana 2 图像生成")
    
    parser.add_argument("-p", "--prompt", required=True, help="提示词")
    parser.add_argument("-i", "--image", required=True, help="输出图片路径")
    parser.add_argument("-r", "--ref", action="append", help="参考图片路径（可多个）")
    parser.add_argument("--web-app-id", type=int, default=47091, help="Web App ID（默认：47091）")
    parser.add_argument("--ar", default="9:16", help="宽高比（默认：9:16）")
    parser.add_argument("--mode", default="third-party", help="模式：third-party|custom")
    parser.add_argument("--resolution", default="1k", help="分辨率：auto, 1k, 2k")
    parser.add_argument("--timeout", type=int, default=120, help="超时时间（秒）")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    
    return parser.parse_args()

def main():
    global api_key
    args = parse_args()
    
    # 获取 API Key
    api_key = get_api_key()
    if not api_key:
        print("❌ 错误：未配置 BIZYAIR_API_KEY")
        print("\n请通过以下方式之一配置：")
        print("1. 环境变量：export BIZYAIR_API_KEY=\"your_key\"")
        print("2. 配置文件：在技能目录创建 .env 文件")
        print("   位置：" + os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/.env")
        print("\n获取 API Key: https://www.bizyair.cn")
        sys.exit(1)
    
    print("🎨 BizyAir Banana 2 图像生成")
    print("=" * 50)
    print(f"提示词：{args.prompt}")
    print(f"输出：{args.image}")
    print(f"Web App ID: {args.web_app_id}")
    print(f"宽高比：{args.ar}")
    print(f"模式：{args.mode}")
    print("")
    
    try:
        # 准备输入值
        input_values = {
            "10:BizyAir_NanoBanana2.resolution": args.resolution,
            "10:BizyAir_NanoBanana2.aspect_ratio": args.ar,
            "10:BizyAir_NanoBanana2.mode": args.mode,
        }
        
        # 处理参考图
        if args.ref:
            for idx, ref_path in enumerate(args.ref):
                if os.path.exists(ref_path):
                    # 上传参考图
                    file_url = upload_file(ref_path)
                    # 根据序号映射到节点（示例代码中的 2/3/4 节点）
                    node_id = 2 + idx
                    input_values[f"{node_id}:LoadImage.image"] = file_url
                    print(f"✅ 参考图 {idx+1}: {ref_path} -> {file_url}")
                else:
                    print(f"⚠️  参考文件不存在：{ref_path}")
        
        # 添加提示词（节点 9）
        input_values["9:JjkText.text"] = args.prompt
        
        # 分辨率参数转换为大写
        resolution_map = {"1k": "1K", "2k": "2K", "4k": "4K", "auto": "auto"}
        input_values["10:BizyAir_NanoBanana2.resolution"] = resolution_map.get(args.resolution.lower(), "auto")
        
        # 提交任务
        request_id = submit_task(args.web_app_id, input_values, timeout=args.timeout)
        
        # 等待完成（如果是异步任务）
        print("")
        result = wait_for_task(request_id, timeout=args.timeout)
        
        # 获取输出
        outputs = get_task_outputs(request_id)
        
        if not outputs:
            raise Exception("没有生成结果")
        
        # 下载结果
        output_url = outputs[0]["object_url"]
        download_file(output_url, args.image)
        
        # 输出统计
        print("")
        print("✅ 生成完成！")
        cost_times = result.get("cost_times", {})
        if cost_times:
            print(f"📊 总耗时：{cost_times.get('total_cost_time', 'N/A')}ms")
            print(f"📊 推理耗时：{cost_times.get('inference_cost_time', 'N/A')}ms")
        
        if args.json:
            print(json.dumps({
                "success": True,
                "image": args.image,
                "request_id": request_id,
                "outputs": outputs,
                "cost_times": cost_times,
            }, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print("")
        print(f"❌ 生成失败：{e}")
        
        if args.json:
            print(json.dumps({
                "success": False,
                "error": str(e),
            }, indent=2, ensure_ascii=False))
        
        sys.exit(1)

if __name__ == "__main__":
    main()
