#!/usr/bin/env python3
"""
定时任务调度器
使用apscheduler定时执行采集、生成PDF、推送等任务
"""

import os
import logging
from datetime import datetime, timedelta
from typing import Optional, List
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

# 导入所需模块
import sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from scripts.crawler import DatabaseManager
from scripts.crawler import (
    YanchengGovCrawler,
    BigDataCrawler,
    JscnCrawler,
    DongfangCrawler,
    DushiCrawler,
    ChengnanCrawler,
    JingkaiCrawler,
    YuedaCrawler,
    KfqaCrawler,
    SufuCrawler
)
from scripts.pdf_generator import PDFGenerator
from scripts.feishu_notifier import FeishuNotifier

logger = logging.getLogger(__name__)


class TaskScheduler:
    """任务调度器"""

    def __init__(self):
        """初始化任务调度器"""
        self.scheduler = BlockingScheduler()
        self.db_manager = DatabaseManager()
        self.pdf_generator = PDFGenerator()
        self.feishu_notifier = FeishuNotifier()

        # 配置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('./招投标数据/logs/scheduler.log'),
                logging.StreamHandler()
            ]
        )

    def crawl_all_sites(self, date: Optional[str] = None) -> Dict:
        """
        采集所有网站数据

        Args:
            date: 采集日期，格式: YYYY-MM-DD，如果不提供则采集今天的数据

        Returns:
            采集结果
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')

        logger.info(f"开始采集所有网站数据，日期: {date}")

        # 定义采集器列表
        crawlers = [
            YanchengGovCrawler,
            BigDataCrawler,
            JscnCrawler,
            DongfangCrawler,
            DushiCrawler,
            ChengnanCrawler,
            JingkaiCrawler,
            YuedaCrawler,
            KfqaCrawler,
            SufuCrawler
        ]

        results = {
            'total_sites': len(crawlers),
            'successful_sites': 0,
            'total_projects': 0,
            'new_projects': 0,
            'site_results': []
        }

        for crawler_class in crawlers:
            try:
                crawler = crawler_class(self.db_manager)
                result = crawler.crawl(date, date)

                if result.get('total', 0) >= 0:
                    results['successful_sites'] += 1
                    results['total_projects'] += result.get('total', 0)
                    results['new_projects'] += result.get('new', 0)

                    results['site_results'].append({
                        'site': crawler.SITE_NAME,
                        'total': result.get('total', 0),
                        'new': result.get('new', 0),
                        'success': True
                    })

                    logger.info(f"{crawler.SITE_NAME}: 采集成功，总计 {result.get('total', 0)} 条，新增 {result.get('new', 0)} 条")

                else:
                    results['site_results'].append({
                        'site': crawler.SITE_NAME,
                        'total': 0,
                        'new': 0,
                        'success': False,
                        'error': result.get('error')
                    })

                    logger.error(f"{crawler.SITE_NAME}: 采集失败")

            except Exception as e:
                logger.error(f"{crawler_class.__name__}: 采集异常 - {e}")
                results['site_results'].append({
                    'site': crawler_class.__name__,
                    'total': 0,
                    'new': 0,
                    'success': False,
                    'error': str(e)
                })

        logger.info(f"采集完成: 成功 {results['successful_sites']}/{results['total_sites']} 个网站，总计 {results['total_projects']} 条，新增 {results['new_projects']} 条")

        return results

    def generate_report(self, date: Optional[str] = None) -> Optional[str]:
        """
        生成PDF报告

        Args:
            date: 报告日期，格式: YYYY-MM-DD，如果不提供则生成今天的报告

        Returns:
            PDF文件路径，失败返回None
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')

        logger.info(f"开始生成PDF报告，日期: {date}")

        try:
            pdf_file = self.pdf_generator.generate_daily_report(date)

            if pdf_file:
                logger.info(f"PDF报告生成成功: {pdf_file}")
                return pdf_file
            else:
                logger.warning(f"PDF报告生成失败或无数据")
                return None

        except Exception as e:
            logger.error(f"生成PDF报告异常: {e}")
            return None

    def send_notification(self, date: Optional[str] = None, pdf_file: Optional[str] = None) -> bool:
        """
        发送通知

        Args:
            date: 通知日期，格式: YYYY-MM-DD，如果不提供则发送今天的通知
            pdf_file: PDF文件路径，如果不提供则只发送文本消息

        Returns:
            是否发送成功
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')

        logger.info(f"开始发送通知，日期: {date}")

        try:
            # 查询数据
            conn = self.db_manager.conn
            cursor = conn.cursor()

            cursor.execute('''
                SELECT
                    project_name, region, source_site, budget_text, purchaser
                FROM bidding_projects
                WHERE publish_date = ?
                ORDER BY region, source_site, project_name
            ''', (date,))

            columns = ['project_name', 'region', 'source_site', 'budget_text', 'purchaser']
            projects = []
            for row in cursor.fetchall():
                project = dict(zip(columns, row))
                projects.append(project)

            if not projects:
                logger.warning(f"日期 {date} 没有数据，跳过发送通知")
                return False

            # 发送日报消息
            result = self.feishu_notifier.send_daily_report(date, projects, pdf_file)

            if result:
                logger.info(f"通知发送成功")
                # 更新推送状态
                self._update_push_status(date)
                return True
            else:
                logger.error(f"通知发送失败")
                return False

        except Exception as e:
            logger.error(f"发送通知异常: {e}")
            return False

    def _update_push_status(self, date: str):
        """更新推送状态"""
        try:
            cursor = self.db_manager.conn.cursor()
            cursor.execute('''
                UPDATE bidding_projects
                SET push_status = 1, push_time = CURRENT_TIMESTAMP
                WHERE publish_date = ?
            ''', (date,))
            self.db_manager.conn.commit()
            logger.info(f"推送状态已更新")
        except Exception as e:
            logger.error(f"更新推送状态失败: {e}")

    def run_daily_task(self):
        """执行每日任务：采集 → 生成PDF → 发送通知"""
        logger.info("=" * 80)
        logger.info(f"开始执行每日任务 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 80)

        try:
            # 1. 采集数据
            date = datetime.now().strftime('%Y-%m-%d')
            crawl_result = self.crawl_all_sites(date)

            if crawl_result['new_projects'] > 0:
                # 2. 生成PDF报告
                pdf_file = self.generate_report(date)

                # 3. 发送通知
                self.send_notification(date, pdf_file)
            else:
                logger.info("今日无新增数据，跳过生成PDF和发送通知")

        except Exception as e:
            logger.error(f"执行每日任务异常: {e}")

        logger.info("=" * 80)
        logger.info(f"每日任务执行完成 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 80)

    def add_daily_job(self, cron_expression: str = "0 9 * * *"):
        """
        添加每日定时任务

        Args:
            cron_expression: Cron表达式，默认为每天9:00执行
        """
        self.scheduler.add_job(
            func=self.run_daily_task,
            trigger=CronTrigger.from_crontab(cron_expression),
            id='daily_crawl_task',
            name='每日采集任务',
            replace_existing=True
        )

        logger.info(f"已添加每日定时任务: {cron_expression}")

    def start(self):
        """启动调度器"""
        logger.info("任务调度器启动中...")

        try:
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            logger.info("任务调度器已停止")

    def run_once(self):
        """立即执行一次任务"""
        logger.info("立即执行任务")
        self.run_daily_task()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='招投标信息采集任务调度器')
    parser.add_argument('--mode', choices=['once', 'schedule'], default='once',
                        help='运行模式：once（立即执行一次）或 schedule（定时执行）')
    parser.add_argument('--cron', default='0 9 * * *',
                        help='Cron表达式，默认为每天9:00执行')

    args = parser.parse_args()

    scheduler = TaskScheduler()

    if args.mode == 'once':
        # 立即执行一次
        scheduler.run_once()
    else:
        # 添加定时任务并启动
        scheduler.add_daily_job(args.cron)
        scheduler.start()
