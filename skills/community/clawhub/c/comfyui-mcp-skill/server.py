"""
AI ComfyUI MCP 服务器
提供视频生成、分镜生成和视频合成功能的 MCP 服务
"""

from fastmcp import FastMCP
import argparse
from utils import setup_logger
from tools import register_all_tools

logger = setup_logger(__name__)

# 创建 FastMCP 实例
mcp = FastMCP("comfyui-mcp-server")

# 注册所有工具
register_all_tools(mcp)

if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="ComfyUI MCP 服务器")
    parser.add_argument("--transport", default="http", choices=["stdio", "http"], help="传输模式")
    parser.add_argument("--host", default="0.0.0.0", help="服务器地址")
    parser.add_argument("--port", type=int, default=18060, help="服务器端口")
    parser.add_argument("--path", default="/mcp", help="HTTP 的路径前缀")
    parser.add_argument("--show_banner", action="store_true", help="显示启动横幅")
    args = parser.parse_args()

    # 启动服务器
    mcp.run(
        transport=args.transport,
        host=args.host,
        port=args.port,
        path=args.path,
        show_banner=args.show_banner
    )
