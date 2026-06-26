import asyncio
import logging
import sys
import traceback

sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from mcp_client import MCPClient

# 默认目标 URL
DEFAULT_TARGET_URL = "https://www.baidu.com/"


async def main():
    """访问指定的 URL"""
    # 支持通过命令行参数动态传入目标 URL，未传则使用默认值
    target_url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_TARGET_URL

    client = MCPClient()
    try:
        # 1. 初始化连接
        await client.initialize()

        # 2. 调用 browser_go_to_url
        logging.info(f"正在调用 browser_go_to_url，目标地址: {target_url}")
        result = await client.call_tool("browser_go_to_url", {"url": target_url})
        print(result)
    except Exception as e:
        logging.error(f"执行过程中出错: {e}")
        traceback.print_exc()
    finally:
        # 3. 清理资源
        await client.close()
        logging.info("客户端已关闭")


if __name__ == "__main__":
    asyncio.run(main())
