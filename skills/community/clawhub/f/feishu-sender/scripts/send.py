#!/usr/bin/env python3
"""
Feishu Sender CLI - 飞书消息发送工具

Usage:
    # 发送文本
    python3 send.py --text "Hello World"
    
    # 发送文件
    python3 send.py --file report.docx
    
    # 发送图片
    python3 send.py --image photo.png
    
    # 批量发送
    python3 send.py --text "报告" --file doc1.docx --file doc2.pdf
    
    # 指定目标群聊
    python3 send.py --text "Hello" --chat-id oc_xxx
"""

import sys
import os

# 添加父目录到路径以导入 feishu_sender
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from feishu_sender import FeishuSender, FeishuConfig
import argparse


def main():
    parser = argparse.ArgumentParser(
        description='飞书消息发送工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --text "早安！"
  %(prog)s --file report.docx
  %(prog)s --image screenshot.png
  %(prog)s --text "今日报告" --file doc1.docx --file doc2.pdf
        """
    )
    
    parser.add_argument('--text', '-t', help='发送文本消息')
    parser.add_argument('--file', '-f', action='append', help='发送文件（可多次使用）')
    parser.add_argument('--image', '-i', action='append', help='发送图片（可多次使用）')
    parser.add_argument('--chat-id', '-c', help='目标会话 ID（默认从环境变量读取）')
    parser.add_argument('--env', '-e', help='环境变量文件路径')
    
    args = parser.parse_args()
    
    if not args.text and not args.file and not args.image:
        parser.print_help()
        return
    
    # 加载配置
    config = FeishuConfig.from_env(args.env)
    sender = FeishuSender(config)
    
    try:
        # 发送文本
        if args.text:
            result = sender.send_text(args.text, args.chat_id)
            print(f"✅ 文本发送成功: {result.get('message_id', 'unknown')}")
        
        # 发送文件
        if args.file:
            for f in args.file:
                result = sender.send_file(f, args.chat_id)
                print(f"✅ 文件发送成功 [{os.path.basename(f)}]: {result.get('message_id', 'unknown')}")
        
        # 发送图片
        if args.image:
            for img in args.image:
                result = sender.send_image(img, args.chat_id)
                print(f"✅ 图片发送成功 [{os.path.basename(img)}]: {result.get('message_id', 'unknown')}")
                
    except Exception as e:
        print(f"❌ 发送失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
