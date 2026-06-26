import asyncio
import logging
import sys
import traceback

sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from mcp_client import MCPClient


async def main():
    """向指定元素输入文本"""
    if len(sys.argv) < 3:
        print("用法: python3 input_text.py <index> <text> [xpath]")
        print("  index: 目标输入框的元素索引（必填）")
        print("  text:  要输入的文本内容（必填）")
        print("  xpath: 元素的 XPath 路径（可选）")
        sys.exit(1)

    index = int(sys.argv[1])
    text = sys.argv[2]
    args = {"index": index, "text": text}
    if len(sys.argv) > 3:
        args["xpath"] = sys.argv[3]

    client = MCPClient()
    try:
        await client.initialize()
        logging.info(f"正在调用 browser_input_text，目标索引: {index}，文本: {text}")
        result = await client.call_tool("browser_input_text", args)
        print(result)
    except Exception as e:
        logging.error(f"执行过程中出错: {e}")
        traceback.print_exc()
    finally:
        await client.close()
        logging.info("客户端已关闭")


if __name__ == "__main__":
    asyncio.run(main())
