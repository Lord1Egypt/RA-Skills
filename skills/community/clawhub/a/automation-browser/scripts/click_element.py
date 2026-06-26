import asyncio
import logging
import sys
import traceback

sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from mcp_client import MCPClient


async def main():
    """点击页面上的指定元素"""
    if len(sys.argv) < 2:
        print("用法: python3 click_element.py <index> [xpath]")
        print("  index: 要点击的元素索引（必填）")
        print("  xpath: 元素的 XPath 路径（可选）")
        sys.exit(1)

    index = int(sys.argv[1])
    args = {"index": index}
    if len(sys.argv) > 2:
        args["xpath"] = sys.argv[2]

    client = MCPClient()
    try:
        await client.initialize()
        logging.info(f"正在调用 browser_click_element，目标索引: {index}")
        result = await client.call_tool("browser_click_element", args)
        print(result)
    except Exception as e:
        logging.error(f"执行过程中出错: {e}")
        traceback.print_exc()
    finally:
        await client.close()
        logging.info("客户端已关闭")


if __name__ == "__main__":
    asyncio.run(main())
