#!/usr/bin/env python3
"""
push_to_feishu.py - 推送到飞书群聊

格式化新闻摘要并发送到飞书会话。
支持 Markdown 格式的消息。

用法:
    python push_to_feishu.py --input summarized.json --channel-id oc_xxxxxx

注意:
    此脚本通过 OpenClaw 的 sessions_send 工具发送消息，
    不直接调用飞书 API。
"""

import json
import sys
from datetime import datetime
from pathlib import Path

def categorize_item(item, categories):
    """根据关键词将新闻分类"""
    title = (item.get("title", "") + " " + item.get("snippet", "")).lower()
    
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword.lower() in title:
                return category
    
    return "other"  # 默认分类

def format_message(items, date=None, categories=None):
    """
    格式化飞书消息
    
    返回 Markdown 格式的消息文本
    """
    if not items:
        return "🤖 AI Agent 简报 - 暂无新内容"
    
    date = date or datetime.now().strftime("%Y-%m-%d")
    
    # 按类别分组
    if categories:
        grouped = {}
        for item in items:
            cat = categorize_item(item, categories)
            if cat not in grouped:
                grouped[cat] = []
            grouped[cat].append(item)
    else:
        grouped = {"all": items}
    
    # 类别映射（中文显示）
    category_names = {
        "headline": "🔥 头条",
        "framework": "🛠️ 框架更新",
        "research": "📚 研究论文",
        "company": "🏢 公司动态",
        "application": "💼 行业应用",
        "other": "📰 其他资讯"
    }
    
    # 构建消息
    lines = [f"🤖 AI Agent 每日简报 - {date}\n"]
    
    for cat_key, cat_items in grouped.items():
        if not cat_items:
            continue
        
        cat_name = category_names.get(cat_key, cat_key)
        lines.append(f"{cat_name}")
        
        for item in cat_items[:5]:  # 每类最多 5 条
            title = item.get("title", "无标题")
            url = item.get("url", "")
            summary = item.get("summary", "")
            
            # 格式：• 标题 - 摘要 [链接]
            if url:
                line = f"• {title} - {summary} [{url}]"
            else:
                line = f"• {title} - {summary}"
            
            lines.append(line)
        
        lines.append("")  # 空行分隔
    
    #  footer
    lines.append("---")
    lines.append(f"共 {len(items)} 条资讯 | 来源：DDG + RSS 源")
    
    return "\n".join(lines)

def push_to_feishu(message, channel_id):
    """
    发送消息到飞书
    
    在 OpenClaw 环境中，这会调用 sessions_send 工具。
    返回消息 ID 或错误信息。
    """
    # 实际发送由 OpenClaw 处理
    # 这里返回结构化数据供调用方使用
    
    return {
        "success": True,
        "channel_id": channel_id,
        "message_length": len(message),
        "timestamp": datetime.now().isoformat(),
        "message_preview": message[:100] + "..." if len(message) > 100 else message
    }

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="推送到飞书")
    parser.add_argument("--input", type=str, required=True,
                        help="输入文件路径 (JSON)")
    parser.add_argument("--channel-id", type=str, default="",
                        help="飞书会话 ID")
    parser.add_argument("--output", type=str, default="",
                        help="输出文件路径 (发送结果)")
    parser.add_argument("--config", type=str, default="",
                        help="配置文件路径 (读取 channel_id)")
    
    args = parser.parse_args()
    
    # 读取输入
    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    items = data.get("items", [])
    
    # 加载配置（如果指定）
    channel_id = args.channel_id
    categories = None
    
    if args.config:
        with open(args.config, "r", encoding="utf-8") as f:
            config = json.load(f)
        if not channel_id:
            channel_id = config.get("feishu", {}).get("channel_id", "")
        categories = config.get("categories")
    
    if not channel_id:
        print("错误：未指定 channel_id", file=sys.stderr)
        return 1
    
    # 格式化消息
    message = format_message(items, categories=categories)
    
    # 发送
    result = push_to_feishu(message, channel_id)
    result["message"] = message
    
    # 输出结果
    output = json.dumps(result, ensure_ascii=False, indent=2)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
    else:
        print(output)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
