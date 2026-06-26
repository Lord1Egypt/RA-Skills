#!/usr/bin/env python3
"""
每日语录推送脚本
将生成的语录内容推送到配置的渠道
"""

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# 添加技能目录到路径
BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR / "scripts"))

from utils import get_config, setup_logging


def read_document(date_str: str, output_dir: str) -> Optional[str]:
    """读取生成的文档"""
    from utils import validate_date_str
    date_str = validate_date_str(date_str)
    output_dir = str(Path(output_dir).resolve())
    doc_file = Path(output_dir) / f"{date_str}.md"
    if doc_file.exists():
        with open(doc_file, 'r', encoding='utf-8') as f:
            return f.read()
    return None


def extract_sections(document: str) -> Dict[str, str]:
    """从文档中提取各个部分"""
    sections = {
        "quote": "",
        "source": "",
        "background": "",
        "image": "",
        "voice": "",
        "analysis": ""
    }
    
    try:
        lines = document.split('\n')
        
        # 提取语录
        for i, line in enumerate(lines):
            if line.strip().startswith("> **"):
                sections["quote"] = line.strip()[4:-4]  # 去掉 > ** 和 **
                break
        
        # 提取出处
        for i, line in enumerate(lines):
            if "出处与时间线" in line:
                # 获取下一行非空内容
                for j in range(i+1, min(i+10, len(lines))):
                    if lines[j].strip():
                        sections["source"] = lines[j].strip()
                        break
                break
        
        # 提取背景
        for i, line in enumerate(lines):
            if "历史语境与作用" in line:
                # 获取下一行非空内容
                for j in range(i+1, min(i+10, len(lines))):
                    if lines[j].strip():
                        sections["background"] = lines[j].strip()
                        break
                break
        
        # 提取图片引用
        for line in lines:
            if "![[assets/" in line and ".png" in line:
                sections["image"] = line.strip()
                break
        
        # 提取语音引用
        for line in lines:
            if "![[assets/" in line and ".mp3" in line:
                sections["voice"] = line.strip()
                break
        
        # 提取价值分析
        analysis_lines = []
        capturing = False
        for line in lines:
            if "当代价值分析" in line:
                capturing = True
                continue
            if capturing and line.strip() and not line.startswith("#"):
                if "现实参考案例" in line:
                    break
                if line.strip():
                    analysis_lines.append(line.strip())
        
        sections["analysis"] = " ".join(analysis_lines[:3])  # 取前三句
        
    except Exception as e:
        logging.warning(f"提取文档段落失败: {e}")
    
    return sections


def format_for_telegram(sections: Dict[str, str]) -> str:
    """格式化Telegram推送内容"""
    message = f"""
📖 **每日毛选语录**

💬 {sections['quote']}

📜 **出处**：
{sections['source']}

🎨 **配图**：
{sections['image'] if sections['image'] else '今日无配图'}

🎤 **语音播报**：
{sections['voice'] if sections['voice'] else '今日无语音'}

💡 **价值分析**：
{sections['analysis'][:100]}...

---
🕐 {datetime.now().strftime('%Y-%m-%d %H:%M')}
    """.strip()
    
    return message


def format_for_feishu(sections: Dict[str, str]) -> str:
    """格式化飞书推送内容"""
    message = f"""
每日毛选语录

语录内容：
{sections['quote']}

出处：
{sections['source']}

历史背景：
{sections['background'][:100]}...

今日价值：
{sections['analysis'][:80]}...

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}
    """.strip()
    
    return message


def push_to_telegram(message: str, logger: logging.Logger, bot_token: str = "", chat_id: str = "") -> bool:
    """推送到Telegram"""
    try:
        logger.info("尝试推送到Telegram...")
        
        # 从环境变量或参数获取配置
        bot_token = bot_token or os.environ.get("TELEGRAM_BOT_TOKEN", "")
        chat_id = chat_id or os.environ.get("TELEGRAM_CHAT_ID", "")
        
        if not bot_token or not chat_id:
            logger.warning("Telegram配置不完整，跳过推送 (需要 TELEGRAM_BOT_TOKEN 和 TELEGRAM_CHAT_ID)")
            return False
        
        # 调用Telegram Bot API
        import urllib.request
        import urllib.parse
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = urllib.parse.urlencode({
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True
        }).encode()
        
        req = urllib.request.Request(url, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode())
            if result.get("ok"):
                logger.info("Telegram推送成功")
                return True
            else:
                logger.error(f"Telegram API错误: {result.get('description')}")
                return False
        
    except Exception as e:
        logger.error(f"Telegram推送失败: {e}")
        return False


def push_to_feishu(message: str, logger: logging.Logger, app_id: str = "", app_secret: str = "", chat_id: str = "") -> bool:
    """推送到飞书"""
    try:
        logger.info("尝试推送到飞书...")
        
        # 从环境变量或参数获取配置
        app_id = app_id or os.environ.get("FEISHU_APP_ID", "")
        app_secret = app_secret or os.environ.get("FEISHU_APP_SECRET", "")
        chat_id = chat_id or os.environ.get("FEISHU_CHAT_ID", "")
        
        if not app_id or not app_secret or not chat_id:
            logger.warning("飞书配置不完整，跳过推送 (需要 FEISHU_APP_ID, FEISHU_APP_SECRET, FEISHU_CHAT_ID)")
            return False
        
        # 获取tenant_access_token
        import urllib.request
        import urllib.parse
        
        # 1. 获取token
        token_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        token_data = urllib.parse.urlencode({
            "app_id": app_id,
            "app_secret": app_secret
        }).encode()
        
        token_req = urllib.request.Request(token_url, data=token_data, method="POST")
        with urllib.request.urlopen(token_req, timeout=30) as token_response:
            token_result = json.loads(token_response.read().decode())
            if not token_result.get("code") == 0:
                logger.error(f"飞书认证失败: {token_result.get('msg')}")
                return False
            feishu_token = token_result.get("tenant_access_token")
        
        # 2. 发送消息
        msg_url = "https://open.feishu.cn/open-apis/im/v1/messages"
        msg_data = json.dumps({
            "receive_id": chat_id,
            "msg_type": "text",
            "content": json.dumps({"text": message})
        }).encode()
        
        msg_req = urllib.request.Request(
            msg_url,
            data=msg_data,
            method="POST",
            headers={
                "Authorization": f"Bearer {feishu_token}",
                "Content-Type": "application/json"
            }
        )
        
        with urllib.request.urlopen(msg_req, timeout=30) as msg_response:
            msg_result = json.loads(msg_response.read().decode())
            if msg_result.get("code") == 0:
                logger.info("飞书推送成功")
                return True
            else:
                logger.error(f"飞书消息发送失败: {msg_result.get('msg')}")
                return False
        
    except Exception as e:
        logger.error(f"飞书推送失败: {e}")
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="推送每日毛选语录")
    parser.add_argument("--date", help="指定日期 (YYYY-MM-DD)，默认为今天")
    parser.add_argument("--channel", choices=["telegram", "feishu", "all"], 
                       default="all", help="推送渠道")
    parser.add_argument("--dry-run", action="store_true", help="测试模式，不实际推送")
    args = parser.parse_args()
    
    # 设置日志
    logger = setup_logging()
    
    # 确定日期
    target_date = args.date or datetime.now().strftime("%Y-%m-%d")
    logger.info(f"开始推送 {target_date} 的毛选语录")
    
    try:
        # 获取配置
        config = get_config()
        output_dir = config.get("output_dir", "/tank/obsidian/每日语录")
        
        # 读取文档
        document = read_document(target_date, output_dir)
        if not document:
            logger.error(f"找不到 {target_date} 的文档")
            return 1
        
        # 提取段落
        sections = extract_sections(document)
        logger.info(f"文档解析完成，语录: {sections['quote'][:30]}...")
        
        # 确定推送渠道
        if args.channel == "all":
            channels = config.get("channels", ["telegram"])
        else:
            channels = [args.channel]
        
        # 推送结果
        results = {}
        
        for channel in channels:
            if channel == "telegram":
                message = format_for_telegram(sections)
                if args.dry_run:
                    logger.info(f"Telegram推送内容（测试）:\n{message}")
                    results["telegram"] = "dry_run"
                else:
                    success = push_to_telegram(message, logger)
                    results["telegram"] = "success" if success else "failed"
                    
            elif channel == "feishu":
                message = format_for_feishu(sections)
                if args.dry_run:
                    logger.info(f"飞书推送内容（测试）:\n{message}")
                    results["feishu"] = "dry_run"
                else:
                    success = push_to_feishu(message, logger)
                    results["feishu"] = "success" if success else "failed"
        
        # 输出总结
        logger.info("推送完成")
        print(f"\n📊 推送结果:")
        for channel, result in results.items():
            emoji = "✅" if result == "success" else "🟡" if result == "dry_run" else "❌"
            print(f"  {emoji} {channel}: {result}")
        
        if not args.dry_run:
            failed_channels = [c for c, r in results.items() if r == "failed"]
            if failed_channels:
                print(f"\n⚠️  失败渠道: {', '.join(failed_channels)}")
                return 1
        
        return 0
        
    except Exception as e:
        logger.error(f"推送失败: {str(e)}", exc_info=True)
        print(f"❌ 推送失败: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())