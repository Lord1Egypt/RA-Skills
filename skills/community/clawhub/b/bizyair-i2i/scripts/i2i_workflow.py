#!/usr/bin/env python3
"""
BizyAir 图生图工作流脚本
整合图片上传和图生图 API 调用功能
"""

import os
import sys
import argparse
import json
import requests
from pathlib import Path

# 尝试导入阿里云 OSS SDK
try:
    import alibabacloud_oss_v2 as oss
except ImportError:
    print("❌ 请先安装 alibabacloud_oss_v2 库: pip install alibabacloud_oss_v2")
    sys.exit(1)

# BizyAir API 配置
API_BASE = "https://api.bizyair.cn"
UPLOAD_TOKEN_URL = f"{API_BASE}/x/v1/upload/token"
COMMIT_RESOURCE_URL = f"{API_BASE}/x/v1/input_resource/commit"
TASK_CREATE_URL = f"{API_BASE}/w/v1/webapp/task/openapi/create"
TASK_OUTPUTS_URL = f"{API_BASE}/w/v1/webapp/task/openapi/outputs"

# 图生图 API 配置
I2I_WEB_APP_ID = 48084


def get_api_key():
    """获取 API Key"""
    api_key = os.environ.get("BIZYAIR_API_KEY")
    if not api_key:
        print("❌ 未找到 BIZYAIR_API_KEY 环境变量")
        print("请设置: export BIZYAIR_API_KEY='your_api_key_here'")
        sys.exit(1)
    return api_key


# ==================== 图片上传模块 ====================

def get_upload_token(file_name: str, api_key: str) -> dict:
    """获取上传凭证"""
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {"file_name": file_name, "file_type": "inputs"}

    response = requests.get(UPLOAD_TOKEN_URL, headers=headers, params=params)

    if response.status_code != 200:
        print(f"❌ 获取上传凭证失败: HTTP {response.status_code}")
        sys.exit(1)

    result = response.json()
    if not result.get("status"):
        print(f"❌ 获取上传凭证失败: {result.get('message')}")
        sys.exit(1)

    data = result.get("data", {})
    file_info = data.get("file", {})
    storage_info = data.get("storage", {})

    return {
        "object_key": file_info.get("object_key"),
        "access_key_id": file_info.get("access_key_id"),
        "access_key_secret": file_info.get("access_key_secret"),
        "security_token": file_info.get("security_token"),
        "endpoint": storage_info.get("endpoint"),
        "bucket": storage_info.get("bucket"),
        "region": storage_info.get("region"),
    }


def upload_to_oss(region: str, endpoint: str, bucket: str, object_key: str,
                   file_path: str, access_key_id: str, access_key_secret: str,
                   security_token: str) -> bool:
    """上传文件到 OSS"""
    credentials_provider = oss.credentials.StaticCredentialsProvider(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        security_token=security_token
    )

    normalized_region = region[4:] if region and region.startswith("oss-") else region

    cfg = oss.config.Config(
        credentials_provider=credentials_provider,
        region=normalized_region,
        endpoint=endpoint or f"oss-{normalized_region}.aliyuncs.com"
    )

    try:
        client = oss.Client(cfg)
        client.put_object_from_file(
            oss.PutObjectRequest(bucket=bucket, key=object_key),
            file_path,
        )
        return True
    except Exception as e:
        print(f"❌ OSS 上传失败: {e}")
        return False


def commit_resource(name: str, object_key: str, api_key: str) -> dict:
    """提交输入资源"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {"name": name, "object_key": object_key}

    response = requests.post(COMMIT_RESOURCE_URL, headers=headers, json=data)

    if response.status_code != 200:
        print(f"❌ 提交资源失败: HTTP {response.status_code}")
        sys.exit(1)

    result = response.json()
    if not result.get("status"):
        print(f"❌ 提交资源失败: {result.get('message')}")
        sys.exit(1)

    return result.get("data", {})


def upload_image(file_path: str, api_key: str = None) -> str:
    """上传图片并返回 URL"""
    if not api_key:
        api_key = get_api_key()

    file_path = Path(file_path).resolve()
    if not file_path.exists():
        print(f"❌ 文件不存在: {file_path}")
        sys.exit(1)

    file_name = file_path.name
    print(f"📁 上传图片: {file_name}")

    # 获取上传凭证
    upload_params = get_upload_token(file_name, api_key)

    # 上传到 OSS
    if not upload_to_oss(
        region=upload_params["region"],
        endpoint=upload_params["endpoint"],
        bucket=upload_params["bucket"],
        object_key=upload_params["object_key"],
        file_path=str(file_path),
        access_key_id=upload_params["access_key_id"],
        access_key_secret=upload_params["access_key_secret"],
        security_token=upload_params["security_token"],
    ):
        sys.exit(1)

    # 提交资源
    resource_info = commit_resource(
        name=file_name,
        object_key=upload_params["object_key"],
        api_key=api_key
    )

    print(f"✅ 上传成功")
    print(f"   URL: {resource_info.get('url')}")
    return resource_info.get('url')


# ==================== 图生图 API 模块 ====================

def create_i2i_task(image_url: str, prompt: str, api_key: str, aspect_ratio: str = "16:9") -> str:
    """创建图生图任务"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-Bizyair-Task-Async": "enable"
    }

    payload = {
        "web_app_id": I2I_WEB_APP_ID,
        "suppress_preview_output": True,
        "input_values": {
            "2:LoadImage.image": image_url,
            "19:BizyAir_NanoBananaPro.prompt": prompt,
            "19:BizyAir_NanoBananaPro.aspect_ratio": aspect_ratio
        }
    }

    print(f"🎨 创建图生图任务...")
    print(f"   提示词: {prompt[:50]}...")
    print(f"   比例: {aspect_ratio}")

    response = requests.post(TASK_CREATE_URL, headers=headers, json=payload)

    if response.status_code != 200:
        print(f"❌ 创建任务失败: HTTP {response.status_code}")
        print(response.text)
        sys.exit(1)

    result = response.json()

    # 检查返回格式
    if isinstance(result, dict):
        request_id = result.get("requestId") or result.get("request_id")
        if request_id:
            print(f"✅ 任务创建成功")
            print(f"   Request ID: {request_id}")
            return request_id

    print(f"❌ 创建任务失败: {result}")
    sys.exit(1)


def get_task_results(request_id: str, api_key: str) -> dict:
    """获取任务结果"""
    headers = {"Authorization": f"Bearer {api_key}"}

    print(f"🔍 查询任务结果...")
    response = requests.get(TASK_OUTPUTS_URL, params={"requestId": request_id}, headers=headers)

    if response.status_code != 200:
        print(f"❌ 查询失败: HTTP {response.status_code}")
        return None

    result = response.json()
    data = result.get("data", {})
    status = data.get("status")

    print(f"   状态: {status}")

    if status == "Success":
        outputs = data.get("outputs", [])
        cost_time = data.get("cost_time", 0)

        print(f"✅ 生成成功！")
        print(f"   耗时: {cost_time} 毫秒")
        print(f"   生成 {len(outputs)} 张图片:")

        result_data = {"status": "Success", "cost_time": cost_time, "outputs": []}

        for idx, output in enumerate(outputs):
            url = output.get('object_url')
            print(f"   [{idx+1}] {url}")
            result_data["outputs"].append(url)

        return result_data

    elif status in ["Failed", "Canceled"]:
        print(f"❌ 任务{status}")
        return {"status": status}

    else:
        # 还在处理中
        return {"status": status}


# ==================== 完整工作流 ====================

def run_i2i_workflow(file_path: str, prompt: str, aspect_ratio: str = "16:9", api_key: str = None) -> str:
    """执行完整图生图工作流"""
    if not api_key:
        api_key = get_api_key()

    print("=" * 50)
    print("🚀 BizyAir 图生图工作流")
    print("=" * 50)
    print()

    # 步骤1: 上传图片
    image_url = upload_image(file_path, api_key)
    print()

    # 步骤2: 创建任务
    request_id = create_i2i_task(image_url, prompt, api_key, aspect_ratio)
    print()

    print("=" * 50)
    print(f"🔖 任务已提交")
    print(f"Request ID: {request_id}")
    print(f"图片正在后台生成，请稍后查询结果")
    print()
    print(f"查询命令: python3 {sys.argv[0]} --query {request_id}")
    print("=" * 50)

    return request_id


def wait_and_get_results(request_id: str, api_key: str = None, max_wait: int = 300):
    """等待并获取结果（轮询模式）"""
    if not api_key:
        api_key = get_api_key()

    import time

    print(f"⏳ 等待任务完成（最多 {max_wait} 秒）...")

    start_time = time.time()
    while time.time() - start_time < max_wait:
        result = get_task_results(request_id, api_key)

        if result.get("status") == "Success":
            print()
            print("=" * 50)
            print("🎉 图像生成完成！")
            print("=" * 50)
            print(f"任务 ID: {request_id}")
            print(f"耗时: {result['cost_time']} 毫秒")
            print()
            print("生成的图片:")
            for idx, url in enumerate(result['outputs'], 1):
                print(f"  [{idx}] {url}")
            print("=" * 50)
            return result

        elif result.get("status") in ["Failed", "Canceled"]:
            print("❌ 任务失败或取消")
            return None

        time.sleep(5)  # 每5秒查询一次

    print("⏰ 等待超时")
    return None


# ==================== 主函数 ====================

def main():
    parser = argparse.ArgumentParser(description="BizyAir 图生图工作流工具")
    parser.add_argument("--image", help="本地图片路径")
    parser.add_argument("--prompt", help="生成提示词")
    parser.add_argument("--aspect-ratio", default="16:9", help="图片比例 (默认: 16:9)")
    parser.add_argument("--query", help="查询指定任务的 Request ID")
    parser.add_argument("--wait", action="store_true", help="等待任务完成（轮询模式）")
    parser.add_argument("--api-key", help="BizyAir API Key")

    args = parser.parse_args()
    api_key = args.api_key or get_api_key()

    # 查询模式
    if args.query:
        if args.wait:
            wait_and_get_results(args.query, api_key)
        else:
            result = get_task_results(args.query, api_key)
            if result and result.get("status") == "Success":
                print()
                print("生成的图片 URL:")
                for url in result['outputs']:
                    print(f"  {url}")
        return

    # 生成模式
    if not args.image or not args.prompt:
        parser.error("生成模式需要 --image 和 --prompt 参数")

    request_id = run_i2i_workflow(args.image, args.prompt, args.aspect_ratio, api_key)

    # 如果指定了等待，自动查询结果
    if args.wait:
        print()
        wait_and_get_results(request_id, api_key)


if __name__ == "__main__":
    main()
