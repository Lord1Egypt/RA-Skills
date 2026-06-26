#!/usr/bin/env python3
"""
每日采集任务执行脚本（强制采集模式）
确保每次使用技能时都采集最新数据，避免定时任务失效导致数据中断
"""

import argparse
import logging
import os
import sqlite3
import sys
from datetime import datetime, timedelta

# 添加脚本目录到路径
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from crawler import DatabaseManager, YanchengGovCrawler, BigDataCrawler, JscnCrawler, DongfangCrawler, DushiCrawler, ChengnanCrawler, KfqaCrawler, YuedaCrawler, JingkaiCrawler
from sufu_crawler_final import SufuCrawlerNew

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('./招投标数据/logs/daily_collection_{}.log'.format(datetime.now().strftime('%Y-%m-%d'))),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def get_last_collection_date(db_manager: DatabaseManager) -> datetime:
    """获取最后采集日期"""
    conn = sqlite3.connect(db_manager.db_path)
    cursor = conn.cursor()

    cursor.execute('SELECT MAX(publish_date) FROM bidding_projects')
    result = cursor.fetchone()
    conn.close()

    if result and result[0]:
        return datetime.strptime(result[0], '%Y-%m-%d')
    else:
        return datetime.min


def should_collect(db_manager: DatabaseManager, force: bool = False) -> tuple[bool, str]:
    """
    判断是否需要采集

    Args:
        db_manager: 数据库管理器
        force: 是否强制采集

    Returns:
        (是否需要采集, 原因说明)
    """
    if force:
        return True, "强制采集模式"

    last_date = get_last_collection_date(db_manager)
    today = datetime.now().date()
    last_collection_date = last_date.date()

    # 计算距离上次采集的天数
    days_since_last = (today - last_collection_date).days

    # 如果距离上次采集超过1天，需要采集
    if days_since_last >= 1:
        return True, f"距离上次采集已过 {days_since_last} 天，需要更新数据"

    # 检查今天是否已采集（crawl_time 在今天）
    conn = sqlite3.connect(db_manager.db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT COUNT(*) FROM bidding_projects
        WHERE DATE(crawl_time) = ?
    ''', (today,))
    today_count = cursor.fetchone()[0]
    conn.close()

    if today_count == 0:
        return True, "今天还未采集数据"

    # 检查是否有最新的数据（今天发布的）
    conn = sqlite3.connect(db_manager.db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT COUNT(*) FROM bidding_projects
        WHERE publish_date = ?
    ''', (today,))
    today_publish_count = cursor.fetchone()[0]
    conn.close()

    if today_publish_count == 0:
        return True, "今天还没有新发布的招投标信息，需要采集"

    return False, "数据已是最新（距离上次采集不足1天且今天已有数据）"


def collect_data(db_manager: DatabaseManager, days_back: int = 3) -> dict:
    """
    执行数据采集

    Args:
        db_manager: 数据库管理器
        days_back: 采集最近几天的数据（默认3天）

    Returns:
        采集结果统计
    """
    logger.info("=" * 80)
    logger.info("开始执行数据采集任务")
    logger.info("=" * 80)

    # 计算采集日期范围
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days_back)

    logger.info(f"采集日期范围: {start_date} 至 {end_date}")

    # 定义所有采集器
    crawlers = [
        ('盐城市政府采购网', YanchengGovCrawler),
        ('盐城市大数据集团', BigDataCrawler),
        ('江苏世纪新城', JscnCrawler),
        ('盐城市东方集团', DongfangCrawler),
        ('盐城市都市建设投资集团', DushiCrawler),
        ('城南新区公共资源交易网', ChengnanCrawler),
        ('经开城发集团', KfqaCrawler),
        ('悦达集团', YuedaCrawler),
        ('开发区公共资源交易网', JingkaiCrawler),
        ('苏服采', SufuCrawlerNew),
    ]

    # 统计结果
    results = {
        'total': 0,
        'new': 0,
        'updated': 0,
        'errors': 0,
        'sites': {},
        'start_time': datetime.now()
    }

    # 逐个网站采集
    for site_name, crawler_class in crawlers:
        logger.info(f"\n{'=' * 80}")
        logger.info(f"开始采集: {site_name}")
        logger.info(f"{'=' * 80}")

        try:
            crawler = crawler_class(db_manager)
            site_result = crawler.crawl(str(start_date), str(end_date))

            # 统计结果
            results['sites'][site_name] = {
                'total': site_result.get('total', 0),
                'new': site_result.get('new', 0),
                'updated': site_result.get('updated', 0),
                'error': site_result.get('error', None)
            }

            results['total'] += site_result.get('total', 0)
            results['new'] += site_result.get('new', 0)
            results['updated'] += site_result.get('updated', 0)

            if site_result.get('error'):
                results['errors'] += 1
                logger.error(f"{site_name} 采集失败: {site_result['error']}")
            else:
                logger.info(f"{site_name} 采集成功: 新增 {site_result.get('new', 0)} 条，更新 {site_result.get('updated', 0)} 条")

        except Exception as e:
            logger.error(f"{site_name} 采集异常: {str(e)}", exc_info=True)
            results['sites'][site_name] = {
                'total': 0,
                'new': 0,
                'updated': 0,
                'error': str(e)
            }
            results['errors'] += 1

    results['end_time'] = datetime.now()
    results['duration'] = (results['end_time'] - results['start_time']).total_seconds()

    logger.info("\n" + "=" * 80)
    logger.info("采集任务完成")
    logger.info("=" * 80)
    logger.info(f"总采集数: {results['total']} 条")
    logger.info(f"新增数据: {results['new']} 条")
    logger.info(f"更新数据: {results['updated']} 条")
    logger.info(f"错误网站: {results['errors']} 个")
    logger.info(f"耗时: {results['duration']:.2f} 秒")
    logger.info("=" * 80)

    return results


def print_collection_report(results: dict):
    """打印采集报告"""
    print("\n" + "=" * 80)
    print("采集任务报告")
    print("=" * 80)
    print(f"执行时间: {results['start_time'].strftime('%Y-%m-%d %H:%M:%S')} - {results['end_time'].strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"总耗时: {results['duration']:.2f} 秒")
    print(f"\n采集统计:")
    print(f"  总处理数: {results['total']} 条")
    print(f"  新增数据: {results['new']} 条")
    print(f"  更新数据: {results['updated']} 条")
    print(f"  错误网站: {results['errors']} 个")

    if results['sites']:
        print(f"\n各网站采集详情:")
        for site_name, site_result in results['sites'].items():
            if site_result.get('error'):
                print(f"  ❌ {site_name}: 失败 - {site_result['error']}")
            else:
                print(f"  ✅ {site_name}: 新增 {site_result['new']} 条，更新 {site_result['updated']} 条")

    print("=" * 80)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='每日采集任务执行脚本（强制采集模式）')
    parser.add_argument('--force', action='store_true', help='强制采集，不检查数据时效性')
    parser.add_argument('--days', type=int, default=3, help='采集最近几天的数据（默认3天）')
    parser.add_argument('--check-only', action='store_true', help='只检查是否需要采集，不执行采集')

    args = parser.parse_args()

    # 初始化数据库
    db_manager = DatabaseManager()

    # 检查是否需要采集
    should_collect_flag, reason = should_collect(db_manager, args.force)

    print(f"\n检查结果: {reason}")

    if args.check_only:
        print("仅检查模式，不执行采集")
        if should_collect_flag:
            print(f"建议采集: 是 - {reason}")
            return 1  # 需要采集
        else:
            print(f"建议采集: 否 - {reason}")
            return 0  # 不需要采集

    if not should_collect_flag:
        print("数据已是最新，跳过采集")
        return 0

    # 执行采集
    try:
        results = collect_data(db_manager, args.days)
        print_collection_report(results)

        # 返回码：0=成功，1=有错误，2=无新增数据
        if results['errors'] > 0:
            return 1
        elif results['new'] == 0:
            return 2
        else:
            return 0

    except Exception as e:
        logger.error(f"采集任务失败: {str(e)}", exc_info=True)
        print(f"\n❌ 采集任务失败: {str(e)}")
        return 3


if __name__ == '__main__':
    sys.exit(main())
