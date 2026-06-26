#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI日报飞书推送脚本
将收集的新闻推送到飞书群
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path

import requests

# 配置日志
def setup_logging(log_dir="logs"):
    """设置日志"""
    Path(log_dir).mkdir(exist_ok=True)
    log_file = os.path.join(log_dir, f"ai_daily_{datetime.now().strftime('%Y-%m-%d')}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

# 加载配置
def load_config(config_path="config.json"):
    """加载配置文件"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"配置文件未找到: {config_path}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"配置文件格式错误: {e}")
        raise

# 加载收集的新闻数据
def load_news_data(data_path="data/daily_news.json"):
    """加载新闻数据"""
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"数据文件未找到: {data_path}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"数据文件格式错误: {e}")
        return None

# 构建飞书消息
def build_feishu_message(news_data, max_summary_length=100):
    """
    构建飞书卡片消息
    
    格式：
    📰 AI日报 - 2024年3月14日
    
    [论文] 论文标题
    一句话摘要...
    🔗 链接
    
    [产品] 产品名称
    一句话摘要...
    🔗 链接
    """
    if not news_data or 'items' not in news_data or not news_data['items']:
        return None
    
    date_str = news_data.get('date', datetime.now().strftime('%Y-%m-%d'))
    items = news_data['items']
    
    # 构建内容
    content_lines = []
    
    # 统计各类别数量
    paper_count = sum(1 for item in items if item.get('type') == '论文')
    product_count = sum(1 for item in items if item.get('type') == '产品')
    news_count = sum(1 for item in items if item.get('type') == '资讯')
    
    # 标题
    content_lines.append(f"📰 **AI日报 - {date_str}**")
    content_lines.append(f"今日精选 {len(items)} 条资讯 | 论文 {paper_count} | 产品 {product_count} | 资讯 {news_count}")
    content_lines.append("")
    
    # 按类型分组
    papers = [item for item in items if item.get('type') == '论文']
    products = [item for item in items if item.get('type') == '产品']
    news_items = [item for item in items if item.get('type') == '资讯']
    
    # 论文部分
    if papers:
        content_lines.append("---")
        content_lines.append("📚 **最新论文**")
        content_lines.append("")
        for item in papers:
            tag = item.get('tag', '[论文]')
            title = item.get('title', '无标题')
            summary = item.get('summary', '')
            # 限制摘要长度
            if len(summary) > max_summary_length:
                summary = summary[:max_summary_length] + "..."
            url = item.get('url', '')
            
            content_lines.append(f"**{tag} {title}**")
            content_lines.append(f"> {summary}")
            if url:
                content_lines.append(f"> 🔗 [查看详情]({url})")
            content_lines.append("")
    
    # 产品部分
    if products:
        content_lines.append("---")
        content_lines.append("🚀 **热门产品**")
        content_lines.append("")
        for item in products:
            tag = item.get('tag', '[产品]')
            title = item.get('title', '无标题')
            summary = item.get('summary', '')
            if len(summary) > max_summary_length:
                summary = summary[:max_summary_length] + "..."
            url = item.get('url', '')
            
            content_lines.append(f"**{tag} {title}**")
            content_lines.append(f"> {summary}")
            if url:
                content_lines.append(f"> 🔗 [查看详情]({url})")
            content_lines.append("")
    
    # 资讯部分
    if news_items:
        content_lines.append("---")
        content_lines.append("📰 **行业资讯**")
        content_lines.append("")
        for item in news_items:
            tag = item.get('tag', '[资讯]')
            title = item.get('title', '无标题')
            summary = item.get('summary', '')
            if len(summary) > max_summary_length:
                summary = summary[:max_summary_length] + "..."
            url = item.get('url', '')
            
            content_lines.append(f"**{tag} {title}**")
            content_lines.append(f"> {summary}")
            if url:
                content_lines.append(f"> 🔗 [查看详情]({url})")
            content_lines.append("")
    
    content_lines.append("---")
    content_lines.append("🐱 *由 Cookie 自动推送*")
    
    # 构建飞书卡片消息
    message = {
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": f"📰 AI日报 - {date_str}"
                },
                "template": "blue"
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": '\n'.join(content_lines)
                    }
                }
            ]
        }
    }
    
    return message

# 发送飞书消息（Webhook方式）
def send_feishu_webhook(message, webhook_url):
    """
    通过Webhook发送飞书消息
    """
    if not webhook_url or webhook_url == "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_WEBHOOK_TOKEN":
        logger.error("飞书Webhook URL未配置")
        return False
    
    try:
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.post(webhook_url, json=message, headers=headers, timeout=30)
        response_data = response.json()
        
        if response_data.get('code') == 0:
            logger.info("飞书消息发送成功")
            return True
        else:
            logger.error(f"飞书消息发送失败: {response_data}")
            return False
            
    except Exception as e:
        logger.error(f"发送飞书消息异常: {e}")
        return False

# 主函数
def main():
    """主入口"""
    global logger
    
    # 设置日志
    logger = setup_logging()
    logger.info("=" * 50)
    logger.info("开始推送AI日报到飞书")
    logger.info("=" * 50)
    
    # 加载配置
    config = load_config()
    
    # 加载新闻数据
    data_path = config.get('output', {}).get('data_file', 'data/daily_news.json')
    news_data = load_news_data(data_path)
    
    if not news_data:
        logger.error("没有新闻数据可推送")
        return False
    
    # 构建消息
    max_summary_length = config.get('output', {}).get('max_summary_length', 100)
    message = build_feishu_message(news_data, max_summary_length)
    
    if not message:
        logger.error("消息构建失败")
        return False
    
    # 发送消息
    webhook_url = config.get('feishu', {}).get('webhook_url', '')
    success = send_feishu_webhook(message, webhook_url)
    
    if success:
        logger.info("=" * 50)
        logger.info("AI日报推送完成")
        logger.info("=" * 50)
    else:
        logger.error("AI日报推送失败")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
