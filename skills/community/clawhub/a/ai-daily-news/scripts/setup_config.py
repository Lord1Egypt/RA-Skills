#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Daily News - Interactive Configuration Setup
"""

import json
import os
from pathlib import Path


def setup_config():
    """Interactive configuration setup"""
    print("=" * 60)
    print("AI Daily News - Configuration Setup")
    print("=" * 60)
    
    config = {
        "feishu": {
            "webhook_url": "",
            "chat_id": "",
            "app_id": "",
            "app_secret": ""
        },
        "schedule": {
            "collect_time": "06:00",
            "push_time": "08:00",
            "timezone": "Asia/Shanghai"
        },
        "sources": {
            "arxiv": {
                "enabled": True,
                "categories": ["cs.CL", "cs.LG", "cs.AI"],
                "max_results": 5,
                "days_back": 1
            },
            "producthunt": {
                "enabled": True,
                "max_results": 4
            },
            "huggingface": {
                "enabled": True,
                "max_results": 4
            },
            "youtube": {
                "enabled": True,
                "creators": ["andrew_ng", "matt_wolfe", "ai_explained", "greg_isenberg"],
                "days_back": 7,
                "max_per_creator": 2
            },
            "paperweekly": {
                "enabled": False,
                "rss_url": "",
                "days_back": 7,
                "max_items": 3
            },
            "rss": {
                "enabled": False,
                "days_back": 7,
                "feeds": []
            }
        },
        "fallback": {
            "enabled": True,
            "timeout": 30,
            "retry_times": 2
        },
        "output": {
            "max_summary_length": 100,
            "max_total_items": 20,
            "data_file": "data/daily_news.json"
        },
        "logging": {
            "level": "INFO",
            "log_dir": "logs"
        }
    }
    
    # Feishu configuration
    print("\n📱 Feishu Configuration")
    print("-" * 40)
    webhook = input("Feishu Webhook URL (press Enter to skip): ").strip()
    if webhook:
        config["feishu"]["webhook_url"] = webhook
    
    chat_id = input("Feishu Chat ID (press Enter to skip): ").strip()
    if chat_id:
        config["feishu"]["chat_id"] = chat_id
    
    # Source selection
    print("\n📰 News Sources")
    print("-" * 40)
    
    sources = ["arxiv", "producthunt", "huggingface", "youtube"]
    for source in sources:
        enabled = input(f"Enable {source}? (Y/n): ").strip().lower()
        config["sources"][source]["enabled"] = enabled != "n"
    
    # PaperWeekly
    enable_pw = input("\nEnable PaperWeekly? (y/N): ").strip().lower()
    if enable_pw == "y":
        config["sources"]["paperweekly"]["enabled"] = True
        rss_url = input("PaperWeekly RSS URL (e.g., https://rsshub.app/zhihu/column/paperweekly): ").strip()
        if rss_url:
            config["sources"]["paperweekly"]["rss_url"] = rss_url
    
    # YouTube creators
    if config["sources"]["youtube"]["enabled"]:
        print("\n📺 YouTube Creators")
        print("Available: andrew_ng, matt_wolfe, ai_explained, ai_with_oliver, greg_isenberg")
        creators_input = input("Enter creators (comma-separated, or press Enter for default): ").strip()
        if creators_input:
            config["sources"]["youtube"]["creators"] = [c.strip() for c in creators_input.split(",")]
    
    # Save config
    output_path = Path("config.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Configuration saved to: {output_path.absolute()}")
    print("\nNext steps:")
    print("1. Review and edit config.json if needed")
    print("2. Run: python scripts/collect_ai_news.py")
    print("3. Run: python scripts/push_to_feishu.py")


if __name__ == "__main__":
    setup_config()
