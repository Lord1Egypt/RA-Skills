"""
多渠道推送 - 支持终端输出/Markdown文件/飞书Webhook
"""

import json
import os
from datetime import datetime
from pathlib import Path


OUTPUT_DIR = Path.home() / "info-digest"


def push_to_terminal(digest_md):
    """推送到终端（始终可用）"""
    print("\n" + "=" * 60)
    print(digest_md)
    print("=" * 60)


def push_to_file(digest_md, filename=None):
    """保存为Markdown文件"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    if not filename:
        date_str = datetime.now().strftime("%Y%m%d_%H%M")
        filename = "digest_{}.md".format(date_str)
    
    filepath = OUTPUT_DIR / filename
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(digest_md)
    
    print("[OK] 简报已保存: {}".format(filepath))
    return filepath


def push_to_feishu(digest_md):
    """推送到飞书群（通过Webhook机器人）"""
    webhook_url = os.environ.get("FEISHU_WEBHOOK_URL", "")
    if not webhook_url:
        print("[SKIP] 未配置 FEISHU_WEBHOOK_URL，跳过飞书推送")
        return False
    
    try:
        import requests
        
        payload = {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {"tag": "plain_text", "content": "📡 每日信息简报"},
                    "template": "blue"
                },
                "elements": [
                    {
                        "tag": "markdown",
                        "content": digest_md[:3000]
                    },
                    {
                        "tag": "note",
                        "elements": [{"tag": "plain_text", "content": "由信息源监控助手自动生成"}]
                    }
                ]
            }
        }
        
        resp = requests.post(webhook_url, json=payload, timeout=10)
        resp.raise_for_status()
        print("[OK] 已推送到飞书")
        return True
    except Exception as e:
        print("[ERROR] 飞书推送失败: {}".format(e))
        return False


def push_all(digest_md, channels=None):
    """推送到所有已配置的渠道
    
    Args:
        digest_md: Markdown格式的内容
        channels: list of channel names, default=["terminal", "file"]
    
    Returns:
        dict: {"terminal": bool, "file": path_or_None, "feishu": bool}
    """
    if channels is None:
        channels = ["terminal", "file"]
    
    results = {}
    
    if "terminal" in channels:
        push_to_terminal(digest_md)
        results["terminal"] = True
    
    if "file" in channels:
        results["file"] = push_to_file(digest_md)
    
    if "feishu" in channels:
        results["feishu"] = push_to_feishu(digest_md)
    
    return results


if __name__ == "__main__":
    test_digest = "# 测试简报\n\n这是一条测试消息。\n"
    push_all(test_digest, ["terminal", "file"])
