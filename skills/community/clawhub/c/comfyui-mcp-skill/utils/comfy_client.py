"""
ComfyUI 客户端模块
负责与 ComfyUI API 通信，发送工作流并获取结果
"""

import requests
import yaml
import os
from utils.logger import setup_logger

logger = setup_logger(__name__)

# 读取配置文件，支持环境变量覆盖
with open("config/settings.yaml") as f:
    settings = yaml.safe_load(f)

COMFY_CLOUD_API = os.getenv('COMFY_CLOUD_API', settings['comfy_cloud_api'])
COMFY_CLOUD_API_KEY = os.getenv('COMFY_CLOUD_API_KEY', settings['comfy_cloud_api_key'])


def get_headers():
    """获取 API 请求头"""
    return {"X-API-Key": COMFY_CLOUD_API_KEY, "Content-Type": "application/json"}


def submit_workflow(workflow_json):
    """
    调用 ComfyUI API 执行工作流
    
    Args:
        workflow_json: 工作流 JSON 数据
    
    Returns:
        dict: API 响应结果
    
    Raises:
        RequestException: 网络请求异常
        Exception: 其他异常
    """
    logger.info(f"发送工作流到 ComfyUI API: {COMFY_CLOUD_API}")
    logger.debug(f"工作流数据: {workflow_json}")

    try:
        r = requests.post(
            f"{COMFY_CLOUD_API}/api/prompt",
            json={"prompt": workflow_json},
            headers=get_headers()
        )
        r.raise_for_status()
        result = r.json()
        prompt_id = result["prompt_id"]
        logger.info(f"工作流提交成功，prompt_id: {prompt_id}")
        return prompt_id
    except requests.exceptions.RequestException as e:
        logger.error(f"提交工作流到 ComfyUI 失败: {e}")
        raise
    except Exception as e:
        logger.error(f"run_workflow 中发生意外错误: {e}")
        raise


def download_output(filename: str, subfolder: str = "", output_type: str = "output") -> bytes:
    """下载输出文件

    Args:
        filename: 文件名
        subfolder: 子文件夹路径
        output_type: "output" 表示最终输出，"temp" 表示预览

    Returns:
        文件字节
    """
    params = {
        "filename": filename,
        "subfolder": subfolder,
        "type": output_type
    }

    response = requests.get(
        f"{COMFY_CLOUD_API}/api/view",
        headers={"X-API-Key": COMFY_CLOUD_API_KEY},
        params=params
    )
    response.raise_for_status()
    return response.content


def task_status(prompt_id: str) -> dict:
    """
    检查任务进度

    Args:
        prompt_id: 任务 ID

    Returns:
        dict: 任务状态信息
    """
    response = requests.get(
        f"{COMFY_CLOUD_API}/api/job/{prompt_id}/status",
        headers={"X-API-Key": COMFY_CLOUD_API_KEY}
    )
    response.raise_for_status()
    return response.json()
