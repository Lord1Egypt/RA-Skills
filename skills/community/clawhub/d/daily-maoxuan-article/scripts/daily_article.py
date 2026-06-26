#!/usr/bin/env python3
"""
每日毛选文章推送脚本 v6.0
调用 DeepSeek API 生成高质量文章解读
版本：6.0 - 从静态到动态的飞跃
"""

import os
import re
import sys
import json
import hashlib
import argparse
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# 添加脚本目录到路径
BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR / "scripts"))

try:
    from deep_gen import (
        generate_article_deep_analysis,
        create_article_document,
        format_article_telegram_message
    )
    DEEP_GEN_AVAILABLE = True
except ImportError:
    DEEP_GEN_AVAILABLE = False
    logging.warning("deep_gen 模块未找到，使用简化模式")

# 基础路径
ARTICLES_FILE = BASE_DIR / 'references' / 'mao-articles.md'
STATE_FILE = BASE_DIR / '.article-state'
DEFAULT_OUTPUT_DIR = '/tank/obsidian/每日毛选'


def setup_logging():
    """设置日志"""
    logger = logging.getLogger("daily_maoxuan_article")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        logger.addHandler(handler)
    return logger


def parse_articles_md(filepath: Path) -> List[Dict]:
    """解析 mao-articles.md 文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    articles = []
    current_section = ""
    
    for line in content.split('\n'):
        line = line.strip()
        
        # 跳过空行和注释
        if not line or line.startswith('#'):
            if line.startswith('## '):
                current_section = line.replace('## ', '').strip()
            continue
        
        # 解析文章行
        if '|' in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 3:
                title = parts[0].strip()
                date = parts[1].strip()
                background = parts[2].strip()
                
                # 跳过标题行
                if title in ['每行一篇：标题', '标题']:
                    continue
                
                articles.append({
                    'title': title,
                    'date': date,
                    'background': background,
                    'section': current_section
                })
    
    return articles


def select_article_by_date(articles: List[Dict], target_date: str) -> Optional[Dict]:
    """根据日期选择文章"""
    if not articles:
        return None
    
    # 使用日期哈希确保同一天选择同一篇文章
    hash_value = int(hashlib.md5(target_date.encode()).hexdigest(), 16)
    index = hash_value % len(articles)
    return articles[index]


def get_config():
    """获取配置"""
    config_file = BASE_DIR / 'references' / 'config.json'
    default_config = {
        "output_dir": DEFAULT_OUTPUT_DIR,
        "image_enabled": False,
        "voice_enabled": False,
        "channels": ["obsidian", "telegram"]
    }
    
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        except Exception as e:
            logging.warning(f"读取配置文件失败: {e}")
    
    return default_config


def send_telegram(message: str) -> bool:
    """发送 Telegram 消息"""
    try:
        import requests
        
        bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        chat_id = os.environ.get('TELEGRAM_CHAT_ID')
        
        if not bot_token or not chat_id:
            logging.warning("未配置 Telegram BOT_TOKEN 或 CHAT_ID")
            return False
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML',
            'disable_web_page_preview': True
        }
        
        response = requests.post(url, data=data, timeout=30)
        result = response.json()
        
        if result.get('ok'):
            logging.info("Telegram 消息发送成功")
            return True
        else:
            logging.error(f"Telegram 发送失败: {result}")
            return False
            
    except Exception as e:
        logging.error(f"Telegram 发送异常: {e}")
        return False


def save_document(content: str, filename: str, output_dir: str) -> str:
    """保存文档到 Obsidian"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    filepath = output_path / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    logging.info(f"文档保存成功: {filepath}")
    return str(filepath)


def generate_simple_content(title: str, date: str, background: str) -> str:
    """生成简单内容（当 AI 不可用时）"""
    return f"""# 每日毛选文章 - {datetime.now().strftime('%Y-%m-%d')}

## 文章信息
- **标题**：{title}
- **写作日期**：{date}

## 原文背景
{background}

## 现代启示
• 深入理解本文的历史背景和现实意义
• 把握文章的核心思想和理论贡献
• 思考对当代的现实指导意义

---
*自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""


def main():
    parser = argparse.ArgumentParser(description="每日毛选文章推送 v6.0")
    parser.add_argument("--date", help="指定日期 (YYYY-MM-DD)，默认为今天")
    parser.add_argument("--output-dir", help="输出目录")
    parser.add_argument("--chat", action="store_true", help="仅输出到对话")
    parser.add_argument("--no-send", action="store_true", help="不发送 Telegram")
    parser.add_argument("--simple", action="store_true", help="使用简单模式（不调用AI）")
    args = parser.parse_args()
    
    logger = setup_logging()
    
    # 确定日期并校验
    import re
    target_date = args.date or datetime.now().strftime("%Y-%m-%d")
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', target_date):
        raise ValueError(f"无效日期格式: '{target_date}'，必须为 YYYY-MM-DD")
    logger.info(f"开始生成 {target_date} 的毛选文章")
    
    try:
        # 获取配置
        config = get_config()
        if args.output_dir:
            config["output_dir"] = args.output_dir
        
        # 解析文章库
        if not ARTICLES_FILE.exists():
            logger.error(f"文章库文件不存在: {ARTICLES_FILE}")
            return 1
        
        articles = parse_articles_md(ARTICLES_FILE)
        logger.info(f"解析到文章数: {len(articles)}")
        
        if not articles:
            logger.error("文章库为空")
            return 1
        
        # 选择今日文章
        article = select_article_by_date(articles, target_date)
        if not article:
            logger.error("无法选择文章")
            return 1
        
        logger.info(f"今日文章：{article['title']}")
        logger.info(f"写作时间：{article['date']}")
        
        # 生成内容
        if args.simple or not DEEP_GEN_AVAILABLE:
            logger.info("使用简单模式")
            doc_content = generate_simple_content(
                article['title'],
                article['date'],
                article['background']
            )
            deep = None
        else:
            logger.info("调用 AI 生成深度解读...")
            deep = generate_article_deep_analysis(
                article['title'],
                article['date'],
                article['background']
            )
            
            if deep:
                doc_content = create_article_document(
                    article['title'],
                    article['date'],
                    article['background'],
                    deep,
                    target_date
                )
            else:
                logger.warning("AI 生成失败，使用简单模式")
                doc_content = generate_simple_content(
                    article['title'],
                    article['date'],
                    article['background']
                )
                deep = None
        
        # 输出
        if args.chat:
            print(f"\n{'='*50}")
            print(f"📚 每日毛选文章推送 v6.0")
            print(f"{'='*50}")
            print(f"\n📅 文章：{article['title']}")
            print(f"📆 日期：{article['date']}")
            print(f"🤖 AI深度解读：{'是' if deep else '否'}")
            print(f"\n{'='*50}")
            print(f"📄 文档内容：")
            print(f"{'='*50}")
            print(doc_content[:2000] + "..." if len(doc_content) > 2000 else doc_content)
        else:
            # 保存文档
            filename = f"{target_date}.md"
            filepath = save_document(doc_content, filename, config["output_dir"])
            
            # 发送 Telegram
            if not args.no_send and deep:
                telegram_msg = format_article_telegram_message(
                    article['title'],
                    article['date'],
                    deep,
                    target_date
                )
                send_telegram(telegram_msg)
            elif not args.no_send:
                # 简单模式只发标题
                simple_msg = f"📚 每日毛选文章 | {target_date}\n\n{article['title']}\n{article['date']}"
                send_telegram(simple_msg)
            
            print(f"\n✅ 生成完成!")
            print(f"📅 日期: {target_date}")
            print(f"📄 文档: {filepath}")
            print(f"🤖 AI深度解读: {'是' if deep else '否'}")
            if deep:
                total_len = sum(len(v) for v in deep.values())
                print(f"📊 深度内容字数: {total_len}")
        
        logger.info(f"{target_date} 文章生成成功")
        return 0
        
    except Exception as e:
        logger.error(f"生成失败: {str(e)}", exc_info=True)
        print(f"❌ 生成失败: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())