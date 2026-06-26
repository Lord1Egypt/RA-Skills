#!/usr/bin/env python3
"""
每日毛选语录生成主脚本
调用 DeepSeek API 生成高质量深度解读
"""

import argparse
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

# 添加技能目录到路径
BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR / "scripts"))

try:
    from utils import (
        get_config,
        get_today_quote,
        save_files,
        setup_logging
    )
    from deep_gen import (
        generate_deep_analysis,
        create_deep_document,
        format_deep_telegram_message
    )
except ImportError as e:
    logging.error(f"导入模块失败: {e}")
    sys.exit(1)


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


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="生成每日毛选语录（深度版）")
    parser.add_argument("--date", help="指定日期 (YYYY-MM-DD)，默认为今天")
    parser.add_argument("--output-dir", help="输出目录")
    parser.add_argument("--test", action="store_true", help="测试模式，不保存文件")
    parser.add_argument("--no-send", action="store_true", help="不发送 Telegram")
    parser.add_argument("--simple", action="store_true", help="使用简单模式（不调用AI）")
    args = parser.parse_args()

    # 设置日志
    logger = setup_logging()

    # 确定日期并校验
    target_date = args.date or datetime.now().strftime("%Y-%m-%d")
    from utils import validate_date_str
    target_date = validate_date_str(target_date)
    logger.info(f"开始生成 {target_date} 的毛选语录（深度版）")

    try:
        # 获取配置
        config = get_config()
        if args.output_dir:
            config["output_dir"] = args.output_dir

        # 获取今日语录
        quote = get_today_quote(target_date)
        logger.info(f"获取到语录: {quote['text'][:50]}...")

        # 生成深度解读
        if args.simple:
            logger.info("简单模式，跳过AI深度生成")
            deep = None
        else:
            logger.info("调用 AI 生成深度解读...")
            deep = generate_deep_analysis(quote)
            if not deep:
                logger.warning("AI 生成失败，使用简单模式")
                deep = None

        # 创建文档
        logger.info("开始创建文档...")
        if deep:
            doc_content = create_deep_document(quote, deep, target_date)
        else:
            # 回退到简单格式
            from utils import create_document
            doc_content = create_document(quote, target_date)

        # 格式化 Telegram 消息
        if deep:
            telegram_msg = format_deep_telegram_message(quote, deep, target_date)
        else:
            from utils import format_telegram_message
            telegram_msg = format_telegram_message(quote, target_date)

        # 保存文件
        if not args.test:
            saved_files = save_files(doc_content, target_date, config["output_dir"])
            logger.info(f"文件保存完成: {len(saved_files)} 个文件")

            # 发送到 Telegram
            if not args.no_send:
                send_telegram(telegram_msg)

            # 输出结果
            print(f"\n✅ 生成完成!")
            print(f"📅 日期: {target_date}")
            print(f"📄 文档: {saved_files.get('doc')}")
            print(f"🤖 AI深度解读: {'是' if deep else '否'}")
        else:
            logger.info("测试模式，文件未保存")
            print(f"\n📄 文档内容预览:")
            print(doc_content[:1500], "\n...")
            print(f"\n📱 Telegram 消息预览:")
            print(telegram_msg[:800], "\n...")

        logger.info(f"{target_date} 语录生成成功")
        return 0

    except Exception as e:
        logger.error(f"生成失败: {str(e)}", exc_info=True)
        print(f"❌ 生成失败: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())