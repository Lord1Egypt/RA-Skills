import asyncio
import logging
import sys
import traceback

sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from mcp_client import MCPClient


async def main():
    """滚动到页面上的指定文本位置"""
    if len(sys.argv) < 2:
        print("用法: python3 scroll_to_text.py <text>")
        print("  text: 要滚动到的目标文本（必填）")
        sys.exit(1)

    text = sys.argv[1]
    args = {"text": text}

    client = MCPClient()
    try:
        await client.initialize()
        logging.info(f"正在调用 browser_scroll_to_text，目标文本: {text}")
        result = await client.call_tool("browser_scroll_to_text", args)
        print(result)
    except Exception as e:
        logging.error(f"执行过程中出错: {e}")
        traceback.print_exc()
    finally:
        await client.close()
        logging.info("客户端已关闭")


if __name__ == "__main__":
    asyncio.run(main())
