"""
视频下载工具模块
从 ComfyCloud API 下载生成的视频文件
"""

import os
from utils import setup_logger, download_output

logger = setup_logger(__name__)


def register_tools(mcp):
    """注册工具到 MCP 服务器"""

    @mcp.tool()
    def download_video(prompt_id: str, output_dir: str = "output/videos", filename: str = None) -> str:
        """
        下载指定 prompt_id 的视频文件

        Args:
            prompt_id: ComfyCloud 生成的 prompt ID
            output_dir: 保存目录
            filename: 自定义文件名，默认为 {prompt_id}.mp4

        Returns:
            str: 保存的文件路径

        Raises:
            Exception: 下载失败时抛出异常
        """
        os.makedirs(output_dir, exist_ok=True)

        if not filename:
            filename = f"{prompt_id}.mp4"

        try:
            data = download_output(filename, "", "output")
            output_path = os.path.join(output_dir, filename)
            with open(output_path, "wb") as f:
                f.write(data)
            logger.info(f"视频已保存到：{output_path}")
            return output_path
        except Exception as e:
            logger.error(f"下载视频失败：{e}")
            raise