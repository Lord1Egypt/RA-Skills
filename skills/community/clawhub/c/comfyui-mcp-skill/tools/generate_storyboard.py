"""
分镜生成工具模块
根据用户提示词生成视频分镜脚本
"""

from utils import setup_logger

logger = setup_logger(__name__)


def register_tools(mcp):
    """注册工具到 MCP 服务器"""

    @mcp.tool()
    def generate_storyboard(user_prompt: str):
        """
        生成视频分镜脚本

        Args:
            user_prompt: 用户输入的场景描述

        Returns:
            list: 分镜场景列表，每个场景包含提示词和时长

        Raises:
            Exception: 生成过程中的异常
        """
        logger.info(f"为提示词生成分镜：'{user_prompt}'")

        try:
            storyboard = [
                {"scene": 1, "prompt": f"{user_prompt}, wide shot", "duration": 4},
                {"scene": 2, "prompt": f"{user_prompt}, close up", "duration": 3},
                {"scene": 3, "prompt": f"{user_prompt}, street view", "duration": 3}
            ]
            logger.info(f"分镜生成完成，包含 {len(storyboard)} 个场景")
            return storyboard

        except Exception as e:
            logger.error(f"分镜生成失败：{e}")
            raise