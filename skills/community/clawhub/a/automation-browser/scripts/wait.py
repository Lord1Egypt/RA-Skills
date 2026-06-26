import asyncio
import logging
import sys
import traceback

sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from mcp_client import MCPClient

# 默认等待秒数
DEFAULT_SECONDS = 3


async def main():
    """等待指定的时间"""
    seconds = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SECONDS
    args = {"seconds": seconds}

    client = MCPClient()
    try:
        await client.initialize()
        logging.info(f"正在调用 browser_wait，等待 {seconds} 秒")
        result = await client.call_tool("browser_wait", args)
        print(result)
    except Exception as e:
        logging.error(f"执行过程中出错: {e}")
        traceback.print_exc()
    finally:
        await client.close()
        logging.info("客户端已关闭")


if __name__ == "__main__":
    asyncio.run(main())
