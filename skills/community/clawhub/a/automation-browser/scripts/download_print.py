import asyncio
import logging
import sys
import traceback

sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from mcp_client import MCPClient


async def main():
    """通过打印功能将当前页面保存为 PDF 文件"""
    if len(sys.argv) < 2:
        print("用法: python3 download_print.py <index>")
        print("  index: 打印按钮元素的索引（必填）")
        sys.exit(1)

    index = int(sys.argv[1])
    args = {"index": index}

    client = MCPClient()
    try:
        await client.initialize()
        logging.info(f"正在调用 browser_download_print，目标索引: {index}")
        result = await client.call_tool("browser_download_print", args)
        print(result)
    except Exception as e:
        logging.error(f"执行过程中出错: {e}")
        traceback.print_exc()
    finally:
        await client.close()
        logging.info("客户端已关闭")


if __name__ == "__main__":
    asyncio.run(main())
