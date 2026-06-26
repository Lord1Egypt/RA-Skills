#!/usr/bin/env python3
"""
Chaoji Utils - 潮际工具模块
处理任务轮询、图片下载等通用功能
"""
import os
import time
import urllib.request
from datetime import datetime
from typing import Dict, Any, List, Optional, Callable

try:
    from chaoji_client import ChaojiApiClient
except ImportError:
    from .chaoji_client import ChaojiApiClient


def poll_task_result(client: ChaojiApiClient,
                     task_id: str,
                     max_retries: int = 300,
                     interval: int = 2,
                     on_status_change: Optional[Callable[[str], None]] = None) -> Dict[str, Any]:
    """
    轮询任务结果

    Args:
        client: ChaojiApiClient实例
        task_id: 任务ID
        max_retries: 最大重试次数
        interval: 轮询间隔（秒）
        on_status_change: 状态变更回调函数

    Returns:
        任务结果
    """
    api_name = "marketing_model_task_fetchWithMarketingModelTaskOutputPO_id"

    for i in range(max_retries):
        result = client.get(f"/marketing/model_task/fetchWithMarketingModelTaskOutputPO?id={task_id}", api_name=api_name)

        if result.get("code") == 2000 and result.get("data"):
            data = result["data"]
            status = data.get("status")

            if on_status_change:
                on_status_change(status)

            if status == 2:  # 成功
                outputs = data.get("marketingModelTaskOutputVOS", [])
                return {
                    "status": "success",
                    "data": data,
                    "outputs": outputs
                }
            elif status == 3:  # 失败
                return {
                    "status": "failed",
                    "data": data,
                    "error_msg": data.get("errorMsg") or data.get("failReason", "未知错误")
                }
            elif status == 6:  # 部分失败
                return {
                    "status": "partial_failed",
                    "data": data,
                    "outputs": data.get("marketingModelTaskOutputVOS", []),
                    "error_msg": data.get("errorMsg")
                }

        time.sleep(interval)

    return {"status": "timeout", "error_msg": "轮询超时"}


def download_image(url: str,
                   output_dir: Optional[str] = None,
                   filename: Optional[str] = None) -> Optional[str]:
    """
    下载图片到本地

    Args:
        url: 图片URL
        output_dir: 输出目录，默认 ~/.openclaw/media/outbound
        filename: 自定义文件名，默认从URL提取

    Returns:
        本地文件路径，下载失败返回None
    """
    if output_dir is None:
        output_dir = os.path.expanduser("~/.openclaw/media/outbound")

    os.makedirs(output_dir, exist_ok=True)

    # 确定文件名
    if not filename:
        filename = os.path.basename(url.split("?")[0])
    if not filename:
        filename = f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"

    local_path = os.path.join(output_dir, filename)

    try:
        urllib.request.urlretrieve(url, local_path)
        return local_path
    except Exception as e:
        print(f"下载图片失败: {e}", file=os.sys.stderr)
        return None


def download_outputs(outputs: List[Dict[str, Any]],
                     output_dir: Optional[str] = None,
                     auto_download: bool = True) -> List[Dict[str, Any]]:
    """
    下载输出列表中的图片

    Args:
        outputs: 输出列表
        output_dir: 输出目录
        auto_download: 是否自动下载

    Returns:
        添加了localPath的输出列表
    """
    if not auto_download or not outputs:
        return outputs

    for output in outputs:
        url = output.get("workOutputUrl")
        if url:
            local_path = download_image(url, output_dir)
            if local_path:
                output["localPath"] = local_path

    return outputs


def prepare_image_input(image_input: str,
                        upload_func: Optional[Callable[[str], str]] = None) -> str:
    """
    准备图片输入

    Args:
        image_input: 图片输入（本地路径、URL或OSS Path）
        upload_func: 上传函数，用于处理本地文件

    Returns:
        OSS Path
    """
    # 如果是URL，提取Path
    if image_input.startswith("http"):
        if ".com/" in image_input:
            return image_input.split(".com/", 1)[1]
        elif ".aliyuncs.com/" in image_input:
            return image_input.split(".aliyuncs.com/", 1)[1]
        return image_input

    # 如果是本地文件路径（文件存在），上传
    if os.path.exists(image_input):
        if upload_func:
            return upload_func(image_input)
        raise RuntimeError(f"需要提供上传函数来处理本地文件: {image_input}")

    # 否则视为已经是OSS Path，直接使用
    return image_input
