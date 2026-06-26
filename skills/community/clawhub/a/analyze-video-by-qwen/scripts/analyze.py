#!/usr/bin/env python3
"""
视频分析脚本 - 使用 Qwen 3.5 Plus 多模态模型
支持本地视频文件和远程 URL
"""

import os
import sys
import argparse
import json
from urllib.parse import urlparse
from pathlib import Path
from dashscope import MultiModalConversation
import dashscope

# 设置 DashScope API base_url
# 若使用弗吉尼亚地域模型，需要换成 https://dashscope-us.aliyuncs.com/api/v1
# 若使用新加坡地域的模型，需替换为：https://dashscope-intl.aliyuncs.com/api/v1
dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"


def get_api_key():
    """
    从 ~/.openclaw/openclaw.json 读取 API Key
    """
    config_path = Path.home() / ".openclaw" / "openclaw.json"

    if not config_path.exists():
        print(f"错误: 配置文件不存在: {config_path}")
        sys.exit(1)

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        # 尝试从 skills.dashscope.apiKey 获取
        api_key = config.get("skills", {}).get("dashscope", {}).get("apiKey")

        if not api_key:
            print("错误: 配置文件中未找到 skills.dashscope.apiKey")
            print(f"请在 {config_path} 中添加以下配置:")
            print(json.dumps({"skills": {"dashscope": {"apiKey": "your-api-key"}}}, indent=2))
            sys.exit(1)

        return api_key
    except json.JSONDecodeError as e:
        print(f"错误: 配置文件格式无效: {e}")
        sys.exit(1)


def is_url(text):
    """
    判断输入是否为 URL
    """
    try:
        result = urlparse(text)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def prepare_video_source(video_input):
    """
    准备视频源，支持本地路径和 URL

    Args:
        video_input: 视频路径或 URL

    Returns:
        tuple: (video_url, source_type)
    """
    # 检查是否为 URL
    if is_url(video_input):
        # 直接使用 URL
        return video_input, "remote"

    # 本地路径处理
    # 获取绝对路径
    video_path = os.path.abspath(video_input)

    # 检查文件是否存在
    if not os.path.exists(video_path):
        print(f"错误: 视频文件不存在: {video_path}")
        sys.exit(1)

    # 构造 file:// 协议路径
    video_url = f"file://{video_path}"

    return video_url, "local"


def analyze_video(video_input, fps=2, prompt="这段视频描绘的是什么景象？"):
    """
    使用 Qwen 3.5 Plus 分析视频

    Args:
        video_input: 视频文件的路径或 URL
        fps: 抽帧频率，每秒抽取的帧数
        prompt: 分析提示词
    """
    # 准备视频源
    video_url, source_type = prepare_video_source(video_input)

    # 获取 API Key
    api_key = get_api_key()

    # 构造消息
    messages = [
        {
            'role': 'user',
            'content': [
                {
                    'video': video_url,
                    'fps': fps
                },
                {
                    'text': prompt
                }
            ]
        }
    ]

    source_desc = "远程视频" if source_type == "remote" else "本地视频"
    print(f"正在分析{source_desc}: {video_url}")
    print(f"抽帧频率: {fps} fps")
    print(f"分析提示: {prompt}")
    print("-" * 50)

    try:
        # 调用 Qwen 3.5 Plus 模型
        response = MultiModalConversation.call(
            api_key=api_key,
            model='qwen3.5-plus',
            messages=messages
        )

        # 检查响应状态
        if response.status_code == 200:
            result = response.output.choices[0].message.content[0]["text"]
            print(result)
        else:
            print(f"API 调用失败: {response.status_code}")
            print(f"错误信息: {response.message}")
            sys.exit(1)

    except Exception as e:
        print(f"发生错误: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="使用 Qwen 3.5 Plus 模型分析视频内容，支持本地文件和远程 URL",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 分析本地视频
  %(prog)s video.mp4
  %(prog)s /path/to/video.mp4 --fps 5

  # 分析远程视频 URL
  %(prog)s https://example.com/video.mp4
  %(prog)s http://example.com/video.mp4 --fps 3

  # 自定义提示词
  %(prog)s video.mp4 --prompt "视频中出现了哪些人物？"
  %(prog)s https://example.com/video.mp4 --fps 4 --prompt "请详细描述视频场景"
        """
    )

    parser.add_argument(
        "video_source",
        help="视频文件的路径或远程 URL"
    )

    parser.add_argument(
        "--fps",
        type=int,
        default=2,
        help="抽帧频率，表示每秒抽取的帧数 (默认: 2)"
    )

    parser.add_argument(
        "--prompt",
        default="这段视频描绘的是什么景象？",
        help="分析提示词 (默认: '这段视频描绘的是什么景象？')"
    )

    args = parser.parse_args()

    analyze_video(args.video_source, args.fps, args.prompt)


if __name__ == "__main__":
    main()
