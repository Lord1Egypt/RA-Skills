"""
每日简报主编排 - 串联监控→去重→摘要→推送的完整流程
这是用户最常直接调用的入口。
"""

import json
import sys
import os
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from monitor import run_monitor, load_sources
from summarizer import generate_digest
from pusher import push_all


def main(keywords=None, channels=None, title=None):
    """执行一次完整的每日简报生成流程
    
    Args:
        keywords: list of str, 关键词过滤
        channels: list of str, 推送渠道 ["terminal", "file", "feishu"]
        title: str, 报告标题
    
    Returns:
        dict: 完整结果
    """
    if title is None:
        title = "📡 每日信息简报 — {}".format(datetime.now().strftime("%Y/%m/%d"))
    
    if channels is None:
        channels = ["terminal", "file"]
    
    step1 = run_monitor(keywords=keywords)
    
    if step1.get("status") == "quota_exceeded":
        return step1
    
    if step1.get("status") == "no_sources":
        print("[ERROR] 没有配置任何信息源。请先运行:")
        print("  cd skills/cn-info-monitor && python scripts/setup.py")
        return step1
    
    articles = step1.get("articles", [])
    
    if not articles:
        print("\n✅ 所有信息源均无更新，无需生成简报。")
        return {**step1, "digest": "", "push_results": {}}
    
    digest = generate_digest(articles, keywords=keywords, title=title)
    push_results = push_all(digest, channels=channels)
    
    return {
        **step1,
        "digest": digest,
        "push_results": push_results,
        "generated_at": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="信息源监控助手 - 每日简报生成")
    parser.add_argument("--keywords", "-k", nargs="+", help="关键词过滤")
    parser.add_argument("--channels", "-c", nargs="+", default=["terminal", "file"],
                        choices=["terminal", "file", "feishu"], help="推送渠道")
    parser.add_argument("--title", "-t", default=None, help="报告标题")
    args = parser.parse_args()
    
    result = main(
        keywords=args.keywords,
        channels=args.channels,
        title=args.title
    )
    
    print("\n--- 执行完毕 ---")
    print("新文章: {} 篇 | 渠道: {}".format(
        result.get("new_articles", 0),
        ", ".join(str(v) for v in result.get("push_results", {}).values())
    ))
