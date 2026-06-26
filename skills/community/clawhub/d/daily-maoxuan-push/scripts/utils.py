#!/usr/bin/env python3
"""
工具函数模块
包含生成每日语录所需的各种工具函数
"""

import json
import logging
import os
import random
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

# 基础目录
BASE_DIR = Path(__file__).parent.parent


def setup_logging() -> logging.Logger:
    """设置日志"""
    log_dir = BASE_DIR / "logs"
    log_dir.mkdir(exist_ok=True)
    
    logger = logging.getLogger("daily_maoxuan")
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        # 文件处理器
        log_file = log_dir / f"generate-{datetime.now().strftime('%Y-%m-%d')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger


def get_config() -> Dict[str, Any]:
    """获取配置"""
    config_file = BASE_DIR / "references" / "config.json"
    default_config = {
        "output_dir": "/tank/obsidian/每日语录",
        "voice_enabled": True,
        "channels": ["telegram"],
        "voice_speed": 1.0,
        "template_file": "references/template.md"
    }
    
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        except Exception as e:
            logging.warning(f"读取配置文件失败: {e}")
    
    return default_config


import re

# 严格日期格式校验，防止路径穿越攻击
DATE_PATTERN = re.compile(r'^\d{4}-\d{2}-\d{2}$')

def validate_date_str(date_str: str) -> str:
    """验证日期格式为 YYYY-MM-DD，拒绝包含路径分隔符等危险字符的输入"""
    if not date_str or not DATE_PATTERN.match(date_str):
        raise ValueError(f"无效日期格式: '{date_str}'，必须为 YYYY-MM-DD")
    return date_str


def get_today_quote(date_str: Optional[str] = None) -> Dict[str, str]:
    """获取今日语录"""
    quotes_file = BASE_DIR / "references" / "maoxuan_quotes.json"
    
    if quotes_file.exists():
        try:
            with open(quotes_file, 'r', encoding='utf-8') as f:
                quotes = json.load(f)
        except Exception as e:
            logging.error(f"读取语录文件失败: {e}")
            quotes = []
    else:
        quotes = []
    
    # 如果没有语录文件，使用内置语录
    if not quotes:
        quotes = [
            {
                "id": "1",
                "text": "社会主义制度的建立给我们开辟了一条到达理想境界的道路，而理想境界的实现还要靠我们的辛勤劳动。",
                "source": "毛泽东《关于正确处理人民内部矛盾的问题》，1957年2月27日",
                "date": "1957-02-27",
                "background": "1957年，中国社会主义改造基本完成，社会主义制度刚刚建立。",
                "effect": "这句话成为社会主义建设时期的重要指导思想。",
                "similarities": "• 理想从来都需要劳动来实现\n• 制度提供的是可能性，不是必然性",
                "differences": "| | 1957年 | 今天 |\n|---|---|---|\n| 阶段 | 制度初建 | 制度成熟 |\n| 任务 | 打破旧世界 | 建设新世界 |\n| 挑战 | 物质匮乏 | 精神迷茫 |",
                "thinking_prompt": "你的理想是什么？你为它付出了什么？",
                "data_points": "• 1957年GDP增速：约5%\n• 2024年GDP增速：约5%"
            }
        ]
    
    # 根据日期选择语录
    if date_str:
        import hashlib
        hash_value = int(hashlib.md5(date_str.encode()).hexdigest(), 16)
        index = hash_value % len(quotes)
    else:
        index = random.randint(0, len(quotes) - 1)
    
    return quotes[index]


def create_document(quote: Dict[str, str], date_str: str) -> str:
    """创建简单文档（AI生成失败时的回退方案，v5.0兼容）"""
    template = """# 每日毛选语录 - {date}

## 今日语录
> **{text}**
>
> ——{source}

---

## 📌 出处与背景

{context}

---

*自动生成于 {generate_time} | 简单模式（AI生成未成功）*
*完整硬核解读请稍后重试或查看每日毛选文章推送*"""
    
    # 构建上下文（兼容新旧语录格式）
    context_parts = []
    if quote.get('background'):
        context_parts.append(f"**历史背景**\n{quote['background']}")
    if quote.get('effect'):
        context_parts.append(f"**后续影响**\n{quote['effect']}")
    if quote.get('thinking_prompt'):
        context_parts.append(f"**留给你的思考**\n{quote['thinking_prompt']}")
    if not context_parts:
        context_parts.append("（AI深度解读生成中，请稍后查看 Obsidian 完整文档）")
    
    document = template.format(
        date=date_str,
        text=quote['text'],
        source=quote.get('source', ''),
        context='\n\n'.join(context_parts),
        generate_time=datetime.now().strftime("%Y-%m-%d %H:%M")
    )
    
    return document


def format_telegram_message(quote: Dict[str, str], date_str: str) -> str:
    """格式化 Telegram 消息（简单模式回退，v5.0兼容）"""
    msg = f"""📖 <b>每日毛选语录</b> | {date_str}

━━━━━━━━━━━━━━━━━━

<b>今日语录</b>
<blockquote>{quote['text']}</blockquote>
<blockquote expandable>——{quote.get('source', '')}</blockquote>

━━━━━━━━━━━━━━━━━━

<i>⚠️ AI硬核解读暂未生成，请查看 Obsidian 获取完整内容</i>"""

    return msg


def save_files(document: str, date_str: str, output_base: str) -> Dict[str, str]:
    """保存文件"""
    date_str = validate_date_str(date_str)
    output_dir = Path(output_base).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    saved_files = {}
    
    # 保存文档
    doc_file = output_dir / f"{date_str}.md"
    try:
        with open(doc_file, 'w', encoding='utf-8') as f:
            f.write(document)
        saved_files['doc'] = str(doc_file)
        logging.info(f"文档保存成功: {doc_file}")
    except Exception as e:
        logging.error(f"保存文档失败: {e}")
    
    return saved_files


if __name__ == "__main__":
    # 测试函数
    logger = setup_logging()
    logger.info("测试工具函数...")
    
    config = get_config()
    print(f"配置: {config}")
    
    quote = get_today_quote()
    print(f"语录: {quote['text'][:50]}...")
    
    doc = create_document(quote, "2026-05-08")
    print(f"\n文档预览:\n{doc[:500]}...")