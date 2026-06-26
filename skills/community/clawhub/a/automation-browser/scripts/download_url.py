import asyncio
import logging
import sys
import traceback

sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from mcp_client import MCPClient


async def main():
    """通过 URL 下载文件"""
    if len(sys.argv) < 2:
        print("用法: python3 download_url.py <url>")
        print("  url: 要下载的文件 URL（必填）")
        sys.exit(1)

    url = sys.argv[1]
    args = {"url": url}

    client = MCPClient()
    try:
        await client.initialize()
        logging.info(f"正在调用 browser_download_url，目标 URL: {url}")
        result = await client.call_tool("browser_download_url", args)
        print(result)
    except Exception as e:
        logging.error(f"执行过程中出错: {e}")
        traceback.print_exc()
    finally:
        await client.close()
        logging.info("客户端已关闭")


if __name__ == "__main__":
    asyncio.run(main())
