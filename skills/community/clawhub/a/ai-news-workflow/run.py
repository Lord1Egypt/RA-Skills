from __future__ import annotations
from app.services.translation_service import TranslationService
from pathlib import Path
from datetime import datetime
from app.services.relevance_service import RelevanceService
from app.services.source_scope_service import SourceScopeService
import os
import sys
import traceback

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.core.settings import get_settings
from app.core.logger import setup_logger, get_logger
from app.core.time_window import build_time_window
from app.core.database import DatabaseManager

from app.loaders.company_loader import CompanyLoader
from app.loaders.source_loader import SourceLoader
from app.crawlers.rss_crawler import RSSCrawler
from app.crawlers.web_crawler import WebCrawler

from app.services.filter_service import FilterService
from app.services.match_service import MatchService
from app.services.classify_service import ClassifyService
from app.services.importance_service import ImportanceService
from app.services.dedup_service import DedupService
from app.services.briefing_service import BriefingService

from app.repositories.news_repository import NewsRepository
from app.exporters.excel_exporter import ExcelExporter
from app.exporters.word_exporter import WordExporter
from app.exporters.simple_excel_exporter import SimpleExcelExporter

from app.services.company_event_split_service import CompanyEventSplitService
from app.services.ai_summary_service import AISummaryService
from app.services.global_key_event_service import GlobalKeyEventService

def main(
        config_path: str | None = None,
        model: str | None = None,
        rss_lookback_days: int | None = None,
        web_lookback_days: int | None = None,
        window_mode: str | None = None,
        start_hour: int | None = None,
        end_hour: int | None = None,
        window_lookback_days: int | None = None,
        ) -> None:
    if config_path is None:
        config_path = str(PROJECT_ROOT / "config.yaml")
    settings = get_settings(config_path)
    logger.info(f"config_path = {config_path}")
    logger.info(f"paths.web_source_file = {settings.get('paths','web_source_file', default='(missing)')}")
    setup_logger(settings, log_name="run.log")
    logger = get_logger()

    run_start = datetime.now()
    run_date = run_start.strftime("%Y-%m-%d")

    logger.info("=" * 80)
    logger.info("AI资讯自动化工作流启动")
    logger.info(f"项目根目录: {PROJECT_ROOT}")
    logger.info(f"运行日期: {run_date}")

    try:
        # 1. 初始化数据库
        db_manager = DatabaseManager(settings)
        db_manager.init_db()
        repo = NewsRepository(db_manager)
        logger.info(f"数据库初始化完成: {db_manager.db_path}")

        # 2. 时间窗口（老版）
        #window = build_time_window()
        #time_window_text = window.to_text()
        #logger.info(f"统计窗口: {time_window_text}")

        time_window_mode = settings.get("time_window", "mode", default="previous_day")
        time_window_timezone = settings.get("time_window", "timezone", default="Asia/Shanghai")
        time_window_start_hour = settings.get("time_window", "start_hour", default=0)
        time_window_end_hour = settings.get("time_window", "end_hour", default=0)
        time_window_lookback_days = settings.get("time_window", "lookback_days", default=3)

        # 参数覆盖（如果传了）
        if window_mode:
            time_window_mode = window_mode
        if start_hour is not None:
            time_window_start_hour = int(start_hour)
        if end_hour is not None:
            time_window_end_hour = int(end_hour)
        if window_lookback_days is not None:
            time_window_lookback_days_cfg = int(window_lookback_days)

        window = build_time_window(
            mode=time_window_mode,
            timezone_str=time_window_timezone,
            start_hour=time_window_start_hour,
            end_hour=time_window_end_hour,
            lookback_days=time_window_lookback_days_cfg,
        )
        time_window_text = window.to_text()

        logger.info(f"统计窗口模式: {time_window_mode}")
        logger.info(f"统计窗口: {time_window_text}")


        # 3. 读取输入配置
        company_file = settings.get("paths", "company_file")
        source_file = settings.get("paths", "source_file")

        logger.info(f"企业名单文件: {company_file}")
        logger.info(f"来源配置文件: {source_file}")

        companies = CompanyLoader(company_file).load()
        sources = SourceLoader(source_file).load(enabled_only=True)
        web_source_file = settings.get("paths", "web_source_file", default="")

        logger.info(f"企业名单文件: {company_file}")
        logger.info(f"来源配置文件(RSS等):{source_file}")
        logger.info(f"网页来源配置文件: {web_source_file}")

        companies = CompanyLoader(company_file).load()

        sources = SourceLoader(source_file).load(enabled_only=True)

        web_sources = []
        if web_source_file:
            try:
                web_sources = SourceLoader(web_source_file).load(enabled_only=True)
            except Exception as e:
                logger.warning(f"读取网页来源配置失败，跳过网页来源：{e}")

        all_sources = sources + web_sources

        logger.info(f"企业数量: {len(companies)}")
        logger.info(f"启用来源数量(RSS等): {len(sources)}")
        logger.info(f"启用网页来源数量: {len(web_sources)}")
        logger.info(f"启用来源总数量: {len(all_sources)}")

        # 4. 当前版本先抓 RSS 来源
        rss_lb = rss_lookback_days or settings.get("crawler", "rss_lookback_days", default=3)
        web_lb = web_lookback_days or settings.get("crawler", "web_lookback_days", default=rss_lb)

        logger.info(f"RSS抓取时间窗口: {rss_lb} 天")
        logger.info(f"网页抓取时间窗口: {web_lb} 天")

        rss_sources = [s for s in all_sources if (s.fetch_method or "").lower() == "rss"]
        webpage_sources = [s for s in all_sources if (s.fetch_method or "").lower() in {"webpage", "web"}]

        logger.info(f"RSS 来源数量: {len(rss_sources)}")
        logger.info(f"网页 来源数量: {len(webpage_sources)}")

        rss_crawler = RSSCrawler(
            request_timeout=settings.get("crawler", "request_timeout_seconds", default=20),
            lookback_days=rss_lb,
        )

        web_crawler = WebCrawler(
            request_timeout=settings.get("crawler", "request_timeout_seconds", default=20),
            lookback_days=web_lb,
        )

        all_items = []

        # 4.1 抓 RSS
        for source in rss_sources:
            try:
                items = rss_crawler.fetch(source)
                logger.info(f"[RSS][{source.source_name}] 抓取到 {len(items)} 条")
                all_items.extend(items)
            except Exception as e:
                logger.exception(f"[RSS][{source.source_name}] 抓取失败: {e}")

        # 4.2 抓网页
        for source in webpage_sources:
            try:
                items = web_crawler.fetch(source)
                logger.info(f"[WEB][{source.source_name}] 抓取到 {len(items)} 条")
                all_items.extend(items)
            except Exception as e:
                logger.exception(f"[WEB][{source.source_name}] 抓取失败: {e}")

                logger.info(f"总抓取条数(RSS+WEB): {len(all_items)}")

                logger.info(f"总抓取条数: {len(all_items)}")
                logger.info(
                    f"RSS抓取时间窗口: 近 {settings.get('crawler', 'rss_lookback_days', default=3)} 天"
                )

        # 6. 企业匹配
        match_service = MatchService(companies)
        all_items = match_service.match_items(all_items)
        logger.info("企业匹配完成")

        # 6.5 企业级拆分：一行只保留一家企业
        split_service = CompanyEventSplitService(companies)
        before_split_count = len(all_items)
        all_items = split_service.split_items(all_items)
        logger.info(f"企业级拆分前条数: {before_split_count}")
        logger.info(f"企业级拆分后条数: {len(all_items)}")

        for item in all_items[:10]:
            logger.info(
                f"[拆分样本] 企业={item.related_companies} | 标题={item.title}"
            )


        # 6.5 来源地区约束过滤
        source_scope_service = SourceScopeService(companies)
        scoped_items, scoped_out_items = source_scope_service.filter_items(all_items)

        logger.info(f"来源地区约束后保留条数: {len(scoped_items)}")
        logger.info(f"来源地区约束后剔除条数: {len(scoped_out_items)}")

        for item in scoped_out_items[:10]:
            logger.info(
                f"[来源地区剔除样本] 来源地区={item.source_region_scope} | 标题={item.title} | 企业={item.related_companies} | 备注={item.remarks}"
            )

        all_items = scoped_items

        # 7. 分类
        classify_service = ClassifyService()
        all_items = classify_service.classify_items(all_items)
        logger.info("资讯分类完成")

        # 8. 重要性评分
        importance_service = ImportanceService()
        all_items = importance_service.score_items(all_items)
        logger.info("重要性评分完成")

        # 8.5 相关性筛选
        relevance_service = RelevanceService()
        relevant_items, irrelevant_items = relevance_service.filter_items(all_items)

        logger.info(f"相关性筛选后保留条数: {len(relevant_items)}")
        logger.info(f"相关性筛选后剔除条数: {len(irrelevant_items)}")

        for item in irrelevant_items[:10]:
            logger.info(
                f"[无关样本] 标题={item.title} | 分类={item.category_level_2} | 企业={item.related_companies} | 备注={item.remarks}"
            )

        # 9. 过滤（放到后面，让高价值资讯先被识别）
        filter_service = FilterService(
            min_title_length=settings.get("filter_rules", "min_title_length", default=8),
            require_source_url=settings.get("filter_rules", "require_source_url", default=True),
        )
        valid_items, invalid_items = filter_service.filter_items(relevant_items, window)

        logger.info(f"过滤后有效条数: {len(valid_items)}")
        logger.info(f"过滤后无效条数: {len(invalid_items)}")

        for item in invalid_items[:10]:
            logger.info(
                f"[无效样本] 标题={item.title} | 企业={item.related_companies} | 分类={item.category_level_2} | 备注={item.remarks} | 发布时间={item.publish_time}"
            )

        for item in valid_items[:10]:
            logger.info(
                f"[有效样本] 标题={item.title} | 企业={item.related_companies} | 分类={item.category_level_1}/{item.category_level_2} | 重要性={item.importance} | 状态={item.entry_status}"
            )

        # 10. 内存去重前打印  
        for item in valid_items[:20]:
            logger.info(
                f"[去重前样本] 标题={item.title} | 发布时间={item.publish_time} | 来源={item.source_name}"
            )
        # 10. 内存去重
        dedup_service = DedupService(
            title_similarity_threshold=settings.get("dedup", "title_similarity_threshold", default=90),
            event_similarity_threshold=0.72,
        )
        unique_items, duplicate_items = dedup_service.dedup_items(valid_items)

        logger.info(f"内存去重后保留条数: {len(unique_items)}")
        logger.info(f"内存去重后重复条数: {len(duplicate_items)}")

        # 10. 内存去重后打印
        for item in unique_items[:20]:
            logger.info(
                f"[去重后保留样本] 标题={item.title} | 发布时间={item.publish_time} | 来源={item.source_name}"
            )

        # 11. 数据库去重
        before_db_filter = len(unique_items)
        unique_items = repo.filter_existing_advanced(
            unique_items,
            similar_title_threshold=88,
            similar_title_recent_days=30,
        )
        logger.info(f"数据库去重前条数: {before_db_filter}")
        logger.info(f"数据库去重后条数: {len(unique_items)}")
        logger.info(f"数据库级过滤掉条数: {before_db_filter - len(unique_items)}")



        # 11. 对最终有效数据调用豆包，生成中文标题和100字内摘要
        from app.services.ai_summary_service import AISummaryService

        ark_model =  model or settings.get("ark", "summary_model", default="")
        ark_base_url = settings.get("ark", "base_url", default="https://ark.cn-beijing.volces.com/api/v3")
        ark_api_key = settings.get("ark", "api_key") or os.getenv("ARK_API_KEY")
       

        logger.info(f"方舟 API Key 是否已配置: {'是' if ark_api_key else '否'}")
        logger.info(f"数据库去重后有效条数: {len(unique_items)}")

        if ark_api_key and unique_items:
            ai_summary_service = AISummaryService(
                api_key=ark_api_key,
                model=ark_model,
                base_url=ark_base_url,
                max_retries=2,
                retry_sleep_seconds=1.5,
            )
            unique_items = ai_summary_service.process_items(unique_items)
            logger.info("已完成最终有效资讯的豆包标题/摘要标准化")

            for item in unique_items[:10]:
                logger.info(
                    f"[豆包样本] 原标题={item.original_title or ''} | 新标题={item.title or ''} | 新摘要={item.summary or ''}"
                )
        else:
            logger.info(f"方舟 API Key 是否已配置: {'是' if ark_api_key else '否'}")
            logger.info(f"数据库去重后有效条数: {len(unique_items)}")
            logger.warning("未配置方舟 API Key 或未指定模型或无有效资讯，跳过豆包标题/摘要标准化")

        # 11.5 从全球AI产业动态中选出5个重点事件（仅用于Word）
        global_key_event_service = GlobalKeyEventService(top_n=5)
        selected_global_key_events = global_key_event_service.select_top_events(unique_items)

        logger.info(f"全球AI产业动态重点事件条数: {len(selected_global_key_events)}")
        for item in selected_global_key_events:
            logger.info(
                f"[全球重点事件] 分数={item.global_key_event_score} | 归属={item.global_region_label} | 标题={item.title}"
            )

        # 13. 写入数据库
        repo.save_items(unique_items)
        logger.info(f"写入数据库条数: {len(unique_items)}")

        # 14. 导出 Excel
        excel_output_dir = settings.get("paths", "output_excel_dir")
        excel_filename_prefix = settings.get("output", "excel_filename_prefix", default="AI资讯信息表")

        excel_exporter = ExcelExporter(
            output_dir=excel_output_dir,
            filename_prefix=excel_filename_prefix,
        )
        excel_path = excel_exporter.export_full(
            valid_items=unique_items,
            duplicate_items=duplicate_items,
            invalid_items=invalid_items,
            run_date=run_date,
        )
        logger.info(f"Excel 导出完成: {excel_path}")

        # 14.b 额外导出简表版 Excel（仅有效数据）
        simple_excel_exporter = SimpleExcelExporter(
            output_dir=excel_output_dir,
            filename_prefix="AI资讯有效数据简表",
        )
        simple_excel_path = simple_excel_exporter.export(
            valid_items=unique_items,
            run_date=run_date,
        )
        logger.info(f"简表版 Excel 导出完成: {simple_excel_path}") 


        # 15. 导出 Word
        word_output_dir = settings.get("paths", "output_word_dir")
        word_filename_prefix = settings.get("output", "word_filename_prefix", default="AI资讯简报")

        briefing_service = BriefingService(
            max_items_per_section=settings.get("briefing", "max_items_per_section", default=100),
        )
        briefing_data = briefing_service.build_briefing(
            items=unique_items,
            run_date=run_date,
            time_window=time_window_text,
            global_items_override=selected_global_key_events,
        )

        word_exporter = WordExporter(
            output_dir=word_output_dir,
            filename_prefix=word_filename_prefix,
        )
        word_path = word_exporter.export(
            briefing_data=briefing_data,
            run_date=run_date,
        )
        logger.info(f"Word 导出完成: {word_path}")

        # 16. 结果摘要
        logger.info("-" * 80)
        logger.info("本次运行结果汇总")
        logger.info(f"总抓取条数: {len(all_items)}")
        logger.info(f"有效资讯条数: {len(unique_items)}")
        logger.info(f"重复资讯条数: {len(duplicate_items)}")
        logger.info(f"无效资讯条数: {len(invalid_items)}")
        logger.info(f"Excel 文件: {excel_path}")
        logger.info(f"简表 Excel 文件: {simple_excel_path}")
        logger.info(f"Word 文件: {word_path}")

        run_end = datetime.now()
        logger.info(f"运行完成，用时: {run_end - run_start}")
        logger.info("=" * 80)

        print("运行完成。")
        print(f"Excel: {excel_path}")
        print(f"简表 Excel: {simple_excel_path}")
        print(f"Word : {word_path}")

    except Exception as e:
        logger.exception(f"主流程运行失败: {e}")
        print("运行失败。")
        print(traceback.format_exc())
        raise


if __name__ == "__main__":
    main()