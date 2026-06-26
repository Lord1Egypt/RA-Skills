"""
视频生成工具模块
使用 ComfyUI API 生成 AI 视频
"""

import os
import json
from utils import setup_logger, submit_workflow

logger = setup_logger(__name__)

# 工作流和输出目录配置
WORKFLOW_DIR = "workflows"


def load_workflow(name):
    """
    加载工作流配置文件

    Args:
        name: 工作流文件名

    Returns:
        dict: 工作流配置数据

    Raises:
        FileNotFoundError: 文件不存在
        JSONDecodeError: JSON 格式错误
    """
    logger.info(f"加载工作流：{name}")
    path = os.path.join(WORKFLOW_DIR, name)
    try:
        with open(path, "r") as f:
            workflow = json.load(f)
        logger.info(f"工作流加载成功：{name}")
        return workflow
    except FileNotFoundError:
        logger.error(f"工作流文件未找到：{path}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"工作流文件 {name} JSON 格式无效：{e}")
        raise


def register_tools(mcp):
    """注册工具到 MCP 服务器"""

    @mcp.tool()
    def generate_video(prompt: str, duration: float = 5, width: int = 512, height: int = 512, fps: int = 12):
        """
        生成 AI 视频（异步模式，立即返回 prompt_id）

        Args:
            prompt: 视频生成提示词
            duration: 视频时长（秒）
            width: 视频宽度
            height: 视频高度
            fps: 帧率（frames per second）

        Returns:
            dict: 包含 prompt_id 的字典

        Raises:
            Exception: 生成过程中的异常
        """
        logger.info(f"生成视频：提示词='{prompt}', 时长={duration}s, 尺寸={width}x{height}, fps={fps}")

        try:
            workflow = load_workflow("video_workflow.json")
            # 更新节点 1 (CLIPTextEncode) 的提示词
            workflow["prompt"]["1"]["inputs"]["text"] = prompt
            # 更新 AnimateDiff 节点
            workflow["prompt"]["3"]["inputs"].update({
                "duration": duration,
                "width": width,
                "height": height,
                "fps": fps,
                "frames": []  # 如果不提供关键帧，可留空，让 AnimateDiff 自动生成
            })

            logger.info("提交工作流到 ComfyUI...")
            prompt_id = submit_workflow(workflow)
            return {"prompt_id": prompt_id}
        except Exception as e:
            logger.error(f"视频生成失败：{e}")
            raise
