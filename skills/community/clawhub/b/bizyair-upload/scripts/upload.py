#!/usr/bin/env python3
"""
BizyAir 文件上传脚本
支持上传图片、音频、视频等资源到 BizyAir 服务器
"""

import os
import sys
import json
import argparse
from pathlib import Path

# 尝试导入 requests
try:
    import requests
except ImportError:
    print("❌ 请先安装 requests 库: pip install requests")
    sys.exit(1)

# 尝试导入阿里云 OSS SDK
try:
    import alibabacloud_oss_v2 as oss
except ImportError:
    print("❌ 请先安装 alibabacloud_oss_v2 库: pip install alibabacloud_oss_v2")
    sys.exit(1)


# BizyAir API 端点
API_BASE = "https://api.bizyair.cn"
UPLOAD_TOKEN_URL = f"{API_BASE}/x/v1/upload/token"
COMMIT_RESOURCE_URL = f"{API_BASE}/x/v1/input_resource/commit"
LIST_RESOURCES_URL = f"{API_BASE}/x/v1/input_resource"


def get_api_key():
    """获取 API Key，优先从环境变量读取"""
    api_key = os.environ.get("BIZYAIR_API_KEY")
    if not api_key:
        print("❌ 未找到 BIZYAIR_API_KEY 环境变量")
        print("请设置: export BIZYAIR_API_KEY='your_api_key_here'")
        sys.exit(1)
    return api_key


def get_upload_token(file_name: str, api_key: str, file_type: str = "inputs") -> dict:
    """
    步骤一：获取上传凭证与参数

    Args:
        file_name: 文件名（需要包含扩展名）
        api_key: BizyAir API Key
        file_type: 文件类型，默认为 inputs

    Returns:
        包含上传参数的字典
    """
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    params = {
        "file_name": file_name,
        "file_type": file_type
    }

    print(f"📋 步骤一：获取上传凭证...")

    response = requests.get(UPLOAD_TOKEN_URL, headers=headers, params=params)

    if response.status_code != 200:
        print(f"❌ 获取上传凭证失败: HTTP {response.status_code}")
        print(response.text)
        sys.exit(1)

    result = response.json()

    if not result.get("status"):
        print(f"❌ 获取上传凭证失败: {result.get('message')}")
        sys.exit(1)

    data = result.get("data", {})
    file_info = data.get("file", {})
    storage_info = data.get("storage", {})

    print(f"✅ 上传凭证获取成功")
    print(f"   Object Key: {file_info.get('object_key')}")
    print(f"   Endpoint: {storage_info.get('endpoint')}")
    print(f"   Bucket: {storage_info.get('bucket')}")

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
    """
    步骤二：使用阿里云 OSS SDK 上传文件

    Args:
        region: OSS 区域
        endpoint: OSS 端点
        bucket: 存储桶名称
        object_key: 对象键
        file_path: 本地文件路径
        access_key_id: STS Access Key ID
        access_key_secret: STS Access Key Secret
        security_token: STS Security Token

    Returns:
        上传是否成功
    """
    print(f"📤 步骤二：上传到 OSS...")

    # 配置 OSS 客户端，使用 STS 凭证
    # 使用 StaticCredentialsProvider 直接设置 STS 凭证
    credentials_provider = oss.credentials.StaticCredentialsProvider(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        security_token=security_token
    )

    # 处理 region 前缀（oss-cn-shanghai -> cn-shanghai）
    normalized_region = region[4:] if region and region.startswith("oss-") else region

    cfg = oss.config.Config(
        credentials_provider=credentials_provider,
        region=normalized_region,
        endpoint=endpoint or f"oss-{normalized_region}.aliyuncs.com"
    )

    try:
        client = oss.Client(cfg)
        result = client.put_object_from_file(
            oss.PutObjectRequest(bucket=bucket, key=object_key),
            file_path,
        )
        print(f"✅ OSS 上传成功")
        print(f"   ETag: {result.etag}")
        return True
    except Exception as e:
        print(f"❌ OSS 上传失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def commit_resource(name: str, object_key: str, api_key: str) -> dict:
    """
    步骤三：提交输入资源

    Args:
        name: 文件名
        object_key: OSS 对象键
        api_key: BizyAir API Key

    Returns:
        提交结果，包含 URL 等信息
    """
    print(f"📝 步骤三：提交输入资源...")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "name": name,
        "object_key": object_key
    }

    response = requests.post(COMMIT_RESOURCE_URL, headers=headers, json=data)

    if response.status_code != 200:
        print(f"❌ 提交资源失败: HTTP {response.status_code}")
        print(response.text)
        sys.exit(1)

    result = response.json()

    if not result.get("status"):
        print(f"❌ 提交资源失败: {result.get('message')}")
        sys.exit(1)

    resource_data = result.get("data", {})

    print(f"✅ 资源提交成功")
    print(f"   ID: {resource_data.get('id')}")
    print(f"   URL: {resource_data.get('url')}")

    return resource_data


def list_resources(api_key: str, current: int = 1, page_size: int = 20) -> dict:
    """
    步骤四（可选）：查询已上传的输入资源列表

    Args:
        api_key: BizyAir API Key
        current: 当前页码
        page_size: 每页数量

    Returns:
        资源列表
    """
    print(f"📋 步骤四：查询输入资源列表...")

    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    params = {
        "current": current,
        "page_size": page_size
    }

    response = requests.get(LIST_RESOURCES_URL, headers=headers, params=params)

    if response.status_code != 200:
        print(f"❌ 查询列表失败: HTTP {response.status_code}")
        print(response.text)
        return {}

    result = response.json()

    if not result.get("status"):
        print(f"❌ 查询列表失败: {result.get('message')}")
        return {}

    data = result.get("data", {})
    resource_list = data.get("list", [])

    print(f"✅ 查询成功，共 {data.get('total', 0)} 个资源")

    for item in resource_list:
        print(f"   - {item.get('name')} (ID: {item.get('id')})")
        print(f"     URL: {item.get('url')}")

    return data


def upload_file(file_path: str, api_key: str = None) -> dict:
    """
    完整上传流程

    Args:
        file_path: 本地文件路径
        api_key: BizyAir API Key（可选，默认从环境变量读取）

    Returns:
        上传结果，包含 URL 等信息
    """
    # 验证文件存在
    file_path = Path(file_path).resolve()
    if not file_path.exists():
        print(f"❌ 文件不存在: {file_path}")
        sys.exit(1)

    # 获取 API Key
    if not api_key:
        api_key = get_api_key()

    file_name = file_path.name
    print(f"📁 准备上传文件: {file_name}")
    print(f"   路径: {file_path}")
    print()

    # 步骤一：获取上传凭证
    upload_params = get_upload_token(file_name, api_key)

    # 步骤二：上传到 OSS
    upload_success = upload_to_oss(
        region=upload_params["region"],
        endpoint=upload_params["endpoint"],
        bucket=upload_params["bucket"],
        object_key=upload_params["object_key"],
        file_path=str(file_path),
        access_key_id=upload_params["access_key_id"],
        access_key_secret=upload_params["access_key_secret"],
        security_token=upload_params["security_token"],
    )

    if not upload_success:
        sys.exit(1)

    print()

    # 步骤三：提交资源
    resource_info = commit_resource(
        name=file_name,
        object_key=upload_params["object_key"],
        api_key=api_key
    )

    print()
    print("=" * 50)
    print("🎉 上传完成！")
    print("=" * 50)
    print(f"文件名: {resource_info.get('name')}")
    print(f"URL: {resource_info.get('url')}")
    print(f"扩展名: {resource_info.get('ext')}")
    print(f"ID: {resource_info.get('id')}")
    print("=" * 50)

    return resource_info


def main():
    parser = argparse.ArgumentParser(description="BizyAir 文件上传工具")
    parser.add_argument("file", nargs="?", help="要上传的文件路径（使用 --list 时可选）")
    parser.add_argument("--api-key", help="BizyAir API Key（默认从环境变量 BIZYAIR_API_KEY 读取）")
    parser.add_argument("--list", action="store_true", help="查询已上传的资源列表")
    parser.add_argument("--page", type=int, default=1, help="列表页码（默认 1）")
    parser.add_argument("--page-size", type=int, default=20, help="每页数量（默认 20）")

    args = parser.parse_args()

    api_key = args.api_key or get_api_key()

    if args.list:
        # 查询列表
        list_resources(api_key, args.page, args.page_size)
    else:
        # 上传文件
        if not args.file:
            parser.error("需要指定要上传的文件路径，或使用 --list 查询资源列表")
        upload_file(args.file, api_key)


if __name__ == "__main__":
    main()
