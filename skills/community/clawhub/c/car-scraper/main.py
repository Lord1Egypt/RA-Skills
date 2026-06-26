"""
万能反爬 Skill - 主入口
统一调度三大平台采集，输出 OpenClaw 兼容数据

用法:
    python main.py                     # 采集所有平台（各2页）
    python main.py --platform dasouche # 只采集大搜车
    python main.py --platform dongchedi --pages 5 --city 北京
    python main.py --platform autohome --pages 3
    python main.py --format all        # 输出 json + jsonl + csv
"""

import argparse
import logging
import sys
from datetime import datetime

from config import OUTPUT_DIR
from data_models import ScrapeResult
from dasouche_scraper import DasoucheScraper
from dongchedi_scraper import DongchediScraper
from autohome_scraper import AutohomeScraper
from openclaw_export import export_all_results, export_scrape_result


def setup_logging(verbose: bool = False):
    """配置日志"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(
                f"{OUTPUT_DIR}/scrape_{datetime.now().strftime('%Y%m%d')}.log",
                encoding="utf-8",
            ),
        ],
    )


def run_scraper(platform: str, pages: int = 2, city: str = "") -> ScrapeResult:
    """运行指定平台的采集"""
    scrapers = {
        "dasouche": DasoucheScraper,
        "dongchedi": DongchediScraper,
        "autohome": AutohomeScraper,
    }

    if platform not in scrapers:
        logging.error(f"不支持的平台: {platform}，可选: {', '.join(scrapers.keys())}")
        return ScrapeResult(success=False, source=platform, errors=[f"不支持的平台: {platform}"])

    scraper = scrapers[platform]()

    if platform == "dongchedi":
        return scraper.scrape(pages=pages, city=city)
    else:
        return scraper.scrape(pages=pages)


def main():
    parser = argparse.ArgumentParser(
        description="万能反爬 - 多平台车辆信息采集工具 (供 OpenClaw 使用)"
    )
    parser.add_argument(
        "--platform", "-p",
        choices=["dasouche", "dongchedi", "autohome", "all"],
        default="all",
        help="目标平台 (默认: all 采集所有平台)",
    )
    parser.add_argument(
        "--pages", "-n",
        type=int, default=2,
        help="每个平台采集页数 (默认: 2)",
    )
    parser.add_argument(
        "--city", "-c",
        default="",
        help="城市过滤 (仅懂车帝支持)",
    )
    parser.add_argument(
        "--format", "-f",
        choices=["json", "jsonl", "csv", "all"],
        default="json",
        help="输出格式 (默认: json)",
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="输出目录 (默认: output/openclaw/)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="详细日志",
    )

    args = parser.parse_args()
    setup_logging(args.verbose)

    logger = logging.getLogger("main")
    logger.info("=" * 60)
    logger.info("万能反爬 - 车辆信息采集启动")
    logger.info(f"平台: {args.platform} | 页数: {args.pages} | 格式: {args.format}")
    logger.info("=" * 60)

    results: list[ScrapeResult] = []

    if args.platform == "all":
        platforms = ["dasouche", "dongchedi", "autohome"]
    else:
        platforms = [args.platform]

    for platform in platforms:
        logger.info(f"\n>>> 开始采集: {platform}")
        try:
            result = run_scraper(platform, pages=args.pages, city=args.city)
            results.append(result)
            logger.info(result.summary())
        except Exception as e:
            logger.error(f"{platform} 采集异常: {e}", exc_info=True)
            results.append(ScrapeResult(
                success=False, source=platform,
                errors=[str(e)],
                started_at=datetime.now().isoformat(),
                finished_at=datetime.now().isoformat(),
            ))

    # 导出数据
    logger.info("\n>>> 导出数据到 OpenClaw 格式...")
    exported = export_all_results(results, output_format=args.format, output_dir=args.output)

    logger.info("\n" + "=" * 60)
    logger.info("采集完成汇总:")
    total_vehicles = sum(len(r.vehicles) for r in results)
    total_errors = sum(len(r.errors) for r in results)
    logger.info(f"  总车辆数: {total_vehicles}")
    logger.info(f"  总错误数: {total_errors}")
    logger.info(f"  导出文件: {len(exported)} 个")
    for f in exported:
        logger.info(f"    - {f}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
