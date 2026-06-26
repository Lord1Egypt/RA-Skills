import asyncio
import json
import logging
import sys
import traceback

sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from mcp_client import MCPClient


def print_usage():
    print("用法: python3 download_videos.py <json_args>")
    print("  json_args: JSON 格式的参数字符串（必填）")
    print()
    print("JSON 参数说明:")
    print("  title:       视频主标题（必填）")
    print("  indexes:     视频元素索引数组，如 [2, 3]（可选）")
    print("  urls:        视频播放页 URL 数组（可选）")
    print("  season:      季标识，如 '第1季'（可选）")
    print("  installment: 部标识，如 '第1部'（可选）")
    print("  episodes:    集标识数组，如 ['EP1', '第2集']（可选）")
    print()
    print("示例:")
    print('  python3 download_videos.py \'{"title":"我的视频","indexes":[1,2,3],"episodes":["第1集","第2集","第3集"]}\'')


async def main():
    """批量下载视频"""
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    try:
        args = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(f"JSON 参数解析失败: {e}")
        print_usage()
        sys.exit(1)

    if "title" not in args:
        print("错误: 缺少必填参数 'title'")
        print_usage()
        sys.exit(1)

    client = MCPClient()
    try:
        await client.initialize()
        logging.info(f"正在调用 browser_download_videos，标题: {args.get('title')}")
        result = await client.call_tool("browser_download_videos", args)
        print(result)
    except Exception as e:
        logging.error(f"执行过程中出错: {e}")
        traceback.print_exc()
    finally:
        await client.close()
        logging.info("客户端已关闭")


if __name__ == "__main__":
    asyncio.run(main())
