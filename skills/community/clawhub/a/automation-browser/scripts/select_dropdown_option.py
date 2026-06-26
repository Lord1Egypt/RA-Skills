import asyncio
import logging
import sys
import traceback

sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from mcp_client import MCPClient


async def main():
    """从下拉框中选择一个选项"""
    if len(sys.argv) < 3:
        print("用法: python3 select_dropdown_option.py <index> <text>")
        print("  index: 下拉框元素的索引（必填）")
        print("  text:  要选择的选项文本（必填）")
        sys.exit(1)

    index = int(sys.argv[1])
    text = sys.argv[2]
    args = {"index": index, "text": text}

    client = MCPClient()
    try:
        await client.initialize()
        logging.info(f"正在调用 browser_select_dropdown_option，目标索引: {index}，选项: {text}")
        result = await client.call_tool("browser_select_dropdown_option", args)
        print(result)
    except Exception as e:
        logging.error(f"执行过程中出错: {e}")
        traceback.print_exc()
    finally:
        await client.close()
        logging.info("客户端已关闭")


if __name__ == "__main__":
    asyncio.run(main())
