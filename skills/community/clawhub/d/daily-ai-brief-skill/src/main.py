#!/usr/bin/env python3
"""
AI Daily News Aggregator 主入口
"""
import asyncio
import logging
import sys
import os
from datetime import datetime

# 添加modules目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.config import get_config_loader
from modules.orchestrator import Orchestrator
from modules.report_generator import ReportGenerator


def setup_logging():
    """设置日志配置"""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, f"ai_news_{datetime.now().strftime('%Y%m%d_%H')}.log")

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )

    # 设置第三方库日志级别
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("playwright").setLevel(logging.WARNING)


async def main():
    """主函数"""
    print("=" * 60)
    print("AI Daily News Aggregator")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 设置日志
    setup_logging()
    logger = logging.getLogger(__name__)

    try:
        # 1. 加载配置
        logger.info("步骤1: 加载配置")
        config_loader = get_config_loader()
        config = config_loader.load()
        logger.info(f"配置加载完成，包含 {len(config_loader.get_rss_sources())} 个RSS源")

        # 2. 创建协调器
        logger.info("步骤2: 初始化协调器")
        orchestrator = Orchestrator(max_concurrent=25)

        # 3. 执行抓取
        logger.info("步骤3: 开始抓取数据")
        items = await orchestrator.run()

        if not items:
            logger.warning("没有抓取到任何数据，将继续生成空报告")

        # 4. 生成报告
        logger.info("步骤4: 生成报告")
        report_generator = ReportGenerator()
        reports = report_generator.generate_all_reports(items, orchestrator)

        # 5. 输出结果
        print("\n" + "=" * 60)
        print("抓取完成!")
        print(f"共获取 {len(items)} 个新闻条目")
        print(f"报告文件:")
        for report_type, report_path in reports.items():
            print(f"  - {report_type}: {report_path}")
        print("=" * 60)

        # 打印所有新闻
        print(f"\n📰 所有新闻 ({len(items)} 条):")
        for i, item in enumerate(items, 1):
            print(f"{i}. {item.title}")
            print(f"   来源: {item.source} | 时间: {item.publish_date.strftime('%Y-%m-%d %H:%M') if item.publish_date else '未知'}")
            print(f"   链接: {item.url}")
            if i < len(items):  # 不在最后一条后打印空行
                print()

    except KeyboardInterrupt:
        logger.info("用户中断执行")
        print("\n⏹️  用户中断执行")
    except Exception as e:
        logger.exception("执行过程中发生错误")
        print(f"\n❌ 错误: {e}")
        return 1

    return 0


if __name__ == "__main__":
    # 检查依赖
    try:
        import yaml
        import feedparser
        import requests
        import bs4
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: pip install -r requirements.txt")
        sys.exit(1)

    # 运行主程序
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n⏹️  用户中断执行")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ 程序崩溃: {e}")
        sys.exit(1)