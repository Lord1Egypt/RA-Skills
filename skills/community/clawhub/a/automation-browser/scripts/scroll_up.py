import asyncio
import logging
import sys
import traceback

sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from mcp_client import MCPClient

# 默认滚动量
DEFAULT_AMOUNT = 3


async def main():
    """向上滚动页面"""
    amount = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_AMOUNT
    args = {"amount": amount}

    client = MCPClient()
    try:
        await client.initialize()
        logging.info(f"正在调用 browser_scroll_up，滚动量: {amount}")
        result = await client.call_tool("browser_scroll_up", args)
        print(result)
    except Exception as e:
        logging.error(f"执行过程中出错: {e}")
        traceback.print_exc()
    finally:
        await client.close()
        logging.info("客户端已关闭")


if __name__ == "__main__":
    asyncio.run(main())
