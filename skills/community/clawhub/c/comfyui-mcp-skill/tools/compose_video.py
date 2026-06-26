"""
视频合成工具模块
使用 ffmpeg 将多个视频文件合成为一个完整视频
"""

import subprocess
import os
from utils import setup_logger

logger = setup_logger(__name__)


def register_tools(mcp):
    """注册工具到 MCP 服务器"""

    @mcp.tool()
    def compose_video(video_files: list, output_file: str = "final_video.mp4"):
        """
        合成多个视频文件

        Args:
            video_files: 视频文件路径列表
            output_file: 输出视频文件名

        Returns:
            dict: 包含合成视频 URL 的字典

        Raises:
            CalledProcessError: ffmpeg 执行失败
            Exception: 其他异常
        """
        logger.info(f"合成视频：从 {len(video_files)} 个文件合成到：{output_file}")
        logger.debug(f"Input files: {video_files}")

        try:
            list_file = "list.txt"
            with open(list_file, "w") as f:
                for file in video_files:
                    f.write(f"file '{file}'\n")
            logger.info(f"创建 ffmpeg 列表文件：{list_file}")

            logger.info("运行 ffmpeg 合成视频...")
            result = subprocess.run(
                ["ffmpeg", "-f", "concat", "-safe", "0", "-i", list_file, "-c", "copy", output_file],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                logger.error(f"ffmpeg 执行失败：{result.stderr}")
                raise subprocess.CalledProcessError(result.returncode, result.args)

            output_path = os.path.abspath(output_file)
            logger.info(f"视频合成完成：{output_path}")
            return {"video_url": output_path}

        except subprocess.CalledProcessError as e:
            logger.error(f"ffmpeg 合成失败：{e}")
            raise
        except Exception as e:
            logger.error(f"视频合成失败：{e}")
            raise