#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI日报定时调度器
每天早上6:00收集数据，8:00推送到飞书
"""

import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import schedule

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from collect_ai_news import main as collect_news
from push_to_feishu import main as push_news

# 配置日志
def setup_logging(log_dir="logs"):
    """设置日志"""
    Path(log_dir).mkdir(exist_ok=True)
    log_file = os.path.join(log_dir, f"scheduler_{datetime.now().strftime('%Y-%m-%d')}.log")
    
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

# 任务：收集数据
def job_collect():
    """收集AI新闻数据"""
    logger.info("=" * 60)
    logger.info("【定时任务】开始收集AI日报数据")
    logger.info("=" * 60)
    
    try:
        count = collect_news()
        logger.info(f"数据收集完成，共 {count} 条")
        return True
    except Exception as e:
        logger.error(f"数据收集失败: {e}")
        return False

# 任务：推送数据
def job_push():
    """推送AI日报到飞书"""
    logger.info("=" * 60)
    logger.info("【定时任务】开始推送AI日报到飞书")
    logger.info("=" * 60)
    
    try:
        success = push_news()
        if success:
            logger.info("日报推送成功")
        else:
            logger.error("日报推送失败")
        return success
    except Exception as e:
        logger.error(f"推送失败: {e}")
        return False

# 任务：收集并推送（一次性执行）
def job_collect_and_push():
    """收集并推送（用于测试）"""
    logger.info("=" * 60)
    logger.info("【测试任务】收集并推送")
    logger.info("=" * 60)
    
    if job_collect():
        # 等待几秒确保数据写入
        time.sleep(2)
        job_push()
    else:
        logger.error("收集失败，跳过推送")

# 主函数
def main():
    """主入口"""
    global logger
    
    # 设置日志
    logger = setup_logging()
    
    # 加载配置
    config = load_config()
    schedule_config = config.get('schedule', {})
    
    collect_time = schedule_config.get('collect_time', '06:00')
    push_time = schedule_config.get('push_time', '08:00')
    
    logger.info("=" * 60)
    logger.info("AI日报定时调度器已启动")
    logger.info(f"数据收集时间: {collect_time}")
    logger.info(f"日报推送时间: {push_time}")
    logger.info("=" * 60)
    
    # 设置定时任务
    schedule.every().day.at(collect_time).do(job_collect)
    schedule.every().day.at(push_time).do(job_push)
    
    logger.info(f"已设置每日 {collect_time} 自动收集数据")
    logger.info(f"已设置每日 {push_time} 自动推送日报")
    logger.info("按 Ctrl+C 停止调度器")
    logger.info("-" * 60)
    
    # 运行调度循环
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次
    except KeyboardInterrupt:
        logger.info("-" * 60)
        logger.info("调度器已停止")
        logger.info("=" * 60)

if __name__ == "__main__":
    # 检查命令行参数
    if len(sys.argv) > 1:
        if sys.argv[1] == "--collect":
            # 仅执行收集
            logger = setup_logging()
            job_collect()
        elif sys.argv[1] == "--push":
            # 仅执行推送
            logger = setup_logging()
            job_push()
        elif sys.argv[1] == "--run":
            # 立即执行一次（收集+推送）
            logger = setup_logging()
            job_collect_and_push()
        else:
            print(f"未知参数: {sys.argv[1]}")
            print("用法:")
            print("  python daily_scheduler.py          # 启动定时调度器")
            print("  python daily_scheduler.py --collect # 立即收集数据")
            print("  python daily_scheduler.py --push    # 立即推送日报")
            print("  python daily_scheduler.py --run     # 立即执行一次完整流程")
    else:
        main()
