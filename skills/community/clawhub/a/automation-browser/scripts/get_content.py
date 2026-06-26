import asyncio
import logging
import sys
import traceback

sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from mcp_client import MCPClient


async def main():
    """获取当前页面的 Markdown 内容"""
    client = MCPClient()
    try:
        await client.initialize()
        logging.info("正在调用 browser_markdownify")
        result = await client.call_tool("browser_markdownify", {})
        print(result)
    except Exception as e:
        logging.error(f"执行过程中出错: {e}")
        traceback.print_exc()
    finally:
        await client.close()
        logging.info("客户端已关闭")


if __name__ == "__main__":
    asyncio.run(main())
