import asyncio
import logging
import json
import sys
import traceback

sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from mcp_client import MCPClient


async def main():
    """点击视频播放按钮或剧集按钮来触发下载事件"""
    if len(sys.argv) < 3:
        print("用法: python3 click_video_button.py <index> <title> [installment] [season] [episode]")
        print("  index:       视频元素的索引（必填）")
        print("  title:       视频主标题（必填）")
        print("  installment: 电影系列的第几部，如 '第1部'（可选）")
        print("  season:      电视剧的第几季，如 '第1季'（可选）")
        print("  episode:     电视剧的第几集，如 '第1集'（可选）")
        sys.exit(1)

    index = int(sys.argv[1])
    title = sys.argv[2]
    args = {"index": index, "title": title}

    if len(sys.argv) > 3 and sys.argv[3]:
        args["installment"] = sys.argv[3]
    if len(sys.argv) > 4 and sys.argv[4]:
        args["season"] = sys.argv[4]
    if len(sys.argv) > 5 and sys.argv[5]:
        args["episode"] = sys.argv[5]

    client = MCPClient()
    try:
        await client.initialize()
        logging.info(f"正在调用 browser_click_video_button，索引: {index}，标题: {title}")
        result = await client.call_tool("browser_click_video_button", args)
        print(result)
    except Exception as e:
        logging.error(f"执行过程中出错: {e}")
        traceback.print_exc()
    finally:
        await client.close()
        logging.info("客户端已关闭")


if __name__ == "__main__":
    asyncio.run(main())
