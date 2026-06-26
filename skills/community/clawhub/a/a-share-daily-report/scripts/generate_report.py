
#!/usr/bin/env python3
"""
A股日报生成器 - 主入口脚本
"""

import os
import sys
import argparse
import yaml
from datetime import datetime, date

# 添加项目路径（让模块可以导入）
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from utils import get_logger, format_date
from data_fetcher import DataFetcher
from analyzer import Analyzer
from renderer import Renderer
from trade_calendar import get_effective_date
from publisher import Publisher

logger = get_logger('report_generator')


class ReportGenerator:
    """
    报告生成主控制器
    协调整个报告生成流程
    """

    def __init__(self, config_path=None):
        """
        初始化报告生成器

        Args:
            config_path: 配置文件路径
        """
        if config_path is None:
            config_path = os.path.join(current_dir, '..', 'config', 'config.yaml')
            config_path = os.path.normpath(config_path)

        self.config = self._load_config(config_path)
        self.data_fetcher = DataFetcher(self.config)
        self.analyzer = Analyzer(self.config)
        self.renderer = Renderer(self.config)
        self.publisher = Publisher(self.config)

        logger.info("ReportGenerator 初始化完成")

    def _load_config(self, config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.warning(f"加载配置文件失败，使用默认配置: {e}")
            return {}

    def generate_morning_report(self, dt=None, publish=False):
        """
        生成早报

        Args:
            dt: 报告日期（默认为最近交易日）
            publish: 是否发布到飞书

        Returns:
            包含 markdown 和发布信息的字典
        """
        logger.info("开始生成早报...")
        effective_dt = get_effective_date(dt, mode='morning')
        date_str = format_date(effective_dt)
        logger.info(f"使用日期: {date_str}")

        logger.info("步骤1: 采集数据...")
        data = self._fetch_morning_data(effective_dt)

        logger.info("步骤2: 分析数据...")
        analysis_result = self._analyze_morning_data(data)

        logger.info("步骤3: 渲染报告...")
        markdown = self.renderer.render_morning_report(analysis_result, effective_dt)

        logger.info("步骤4: 保存报告...")
        output_path = self._save_report(markdown, 'morning', effective_dt)

        result = {
            'markdown': markdown,
            'output_path': output_path,
            'date': date_str,
            'mode': 'morning'
        }

        if publish:
            logger.info("步骤5: 发布到飞书...")
            publish_result = self.publisher.publish_morning_report(
                markdown, effective_dt, send_notification=True
            )
            result['publish'] = publish_result

        logger.info(f"早报生成完成: {output_path}")
        return result

    def generate_evening_report(self, dt=None, publish=False):
        """
        生成晚报

        Args:
            dt: 报告日期（默认为最近交易日）
            publish: 是否发布到飞书

        Returns:
            包含 markdown 和发布信息的字典
        """
        logger.info("开始生成晚报...")
        effective_dt = get_effective_date(dt, mode='evening')
        date_str = format_date(effective_dt)
        logger.info(f"使用日期: {date_str}")

        logger.info("步骤1: 采集数据...")
        data = self._fetch_evening_data(effective_dt)

        logger.info("步骤2: 分析数据...")
        analysis_result = self._analyze_evening_data(data)

        logger.info("步骤3: 渲染报告...")
        markdown = self.renderer.render_evening_report(analysis_result, effective_dt)

        logger.info("步骤4: 保存报告...")
        output_path = self._save_report(markdown, 'evening', effective_dt)

        result = {
            'markdown': markdown,
            'output_path': output_path,
            'date': date_str,
            'mode': 'evening'
        }

        if publish:
            logger.info("步骤5: 发布到飞书...")
            publish_result = self.publisher.publish_evening_report(
                markdown, effective_dt, send_notification=True
            )
            result['publish'] = publish_result

        logger.info(f"晚报生成完成: {output_path}")
        return result

    def _fetch_morning_data(self, dt):
        data = {}
        logger.info("采集A股指数数据...")
        data['index_sh'] = self.data_fetcher.get_index_data("000001.SH", dt)
        data['index_sz'] = self.data_fetcher.get_index_data("399001.SZ", dt)
        data['index_cyb'] = self.data_fetcher.get_index_data("399006.SZ", dt)
        # 早报也需要 major_indices（供渲染器展示指数表格）
        data['major_indices'] = self.data_fetcher.get_major_indices(dt)

        logger.info("采集市场情绪数据...")
        data['sentiment'] = self.data_fetcher.get_market_sentiment(dt)

        logger.info("采集资金流向数据（北向/主力）...")
        data['money_flow'] = self.data_fetcher.get_money_flow(dt)

        logger.info("采集行业资金流向...")
        data['industry_fund_flow'] = self.data_fetcher.get_industry_fund_flow(dt)

        logger.info("采集美股数据...")
        data['us_market'] = self.data_fetcher.get_us_market()

        logger.info("采集期指数据...")
        data['futures'] = self.data_fetcher.get_futures_data()

        logger.info("采集新闻数据...")
        data['news'] = self.data_fetcher.get_news(dt, limit=10)

        logger.info("获取自选股表现...")
        try:
            import yaml as _yaml
            current_dir = os.path.dirname(os.path.abspath(__file__))
            watchlist_path = self.config.get('watchlist', {}).get('path', 'config/watchlist.yaml')
            if not os.path.isabs(watchlist_path):
                watchlist_path = os.path.join(os.path.dirname(current_dir), watchlist_path)
            with open(watchlist_path, 'r', encoding='utf-8') as f:
                watchlist = _yaml.safe_load(f).get('watchlist', [])
        except Exception as e:
            logger.warning(f"加载自选股配置失败: {e}")
            watchlist = []
        perf_result = self.data_fetcher.get_watchlist_performance(watchlist, dt)
        data['watchlist_performance'] = perf_result.get('data', []) if perf_result.get('success') else []
        logger.info(f"自选股行情获取完成: {len(data['watchlist_performance'])} 只")

        return data

    def _fetch_evening_data(self, dt):
        data = {}
        logger.info("采集A股指数数据...")
        data['index_sh'] = self.data_fetcher.get_index_data("000001.SH", dt)
        data['index_sz'] = self.data_fetcher.get_index_data("399001.SZ", dt)
        data['index_cyb'] = self.data_fetcher.get_index_data("399006.SZ", dt)

        logger.info("采集市场全景数据...")
        data['market_overview'] = self.data_fetcher.get_market_overview(dt)

        logger.info("采集市场深度数据...")
        data['market_depth'] = self.data_fetcher.get_market_depth(dt)

        logger.info("采集主要指数数据...")
        data['major_indices'] = self.data_fetcher.get_major_indices(dt)

        logger.info("采集全球资产数据...")
        data['global_assets'] = self.data_fetcher.get_global_assets()

        logger.info("采集市场情绪数据...")
        data['sentiment'] = self.data_fetcher.get_market_sentiment(dt)

        logger.info("采集资金流向数据（北向/主力）...")
        data['money_flow'] = self.data_fetcher.get_money_flow(dt)

        logger.info("采集行业资金流向...")
        data['industry_fund_flow'] = self.data_fetcher.get_industry_fund_flow(dt)

        logger.info("采集板块数据...")
        data['sectors'] = self.data_fetcher.get_sector_data(dt)

        logger.info("采集龙虎榜数据...")
        data['lhb'] = self.data_fetcher.get_lhb_data(dt)

        logger.info("采集新闻数据...")
        data['news'] = self.data_fetcher.get_news(dt, limit=10)

        logger.info("获取自选股表现...")
        # 读取自选股配置（与 Analyzer 相同逻辑）
        watchlist_path = self.config.get('watchlist', {}).get('path', 'config/watchlist.yaml')
        if not os.path.isabs(watchlist_path):
            watchlist_path = os.path.join(os.path.dirname(current_dir), watchlist_path)
        
        try:
            with open(watchlist_path, 'r', encoding='utf-8') as f:
                watchlist_config = yaml.safe_load(f)
                watchlist = watchlist_config.get('watchlist', [])
        except Exception as e:
            logger.warning(f"加载自选股配置失败: {e}")
            watchlist = []
        
        perf_result = self.data_fetcher.get_watchlist_performance(watchlist, dt)
        data['watchlist_performance'] = perf_result.get('data', []) if perf_result.get('success') else []

        return data

    def _analyze_morning_data(self, data):
        result = {}
        result['summary'] = self.analyzer.generate_summary(data, mode='morning')
        result['watchlist_morning'] = self.analyzer.analyze_watchlist_morning(data)
        result['strategy'] = self.analyzer.generate_trading_strategy(data)
        result['focus_stocks'] = self.analyzer.analyze_focus_stocks(data)
        result['position'] = self.analyzer.suggest_position(data)
        result['us_market'] = data.get('us_market', {})
        result['futures'] = data.get('futures', {})  # 新增期指数据
        result['industry_fund_flow'] = data.get('industry_fund_flow', {})
        result['major_indices'] = self.analyzer.analyze_major_indices(data)  # A股主要指数
        # 新闻分类
        news_list = data.get('news', {}).get('data', [])
        result['news'] = self.analyzer.classify_news(news_list)
        return result

    def _analyze_evening_data(self, data):
        result = {}
        try:
            logger.info("生成30秒速览...")
            result['summary'] = self.analyzer.generate_summary(data, mode='evening')
        except Exception as e:
            logger.error(f"summary 失败: {e}")
            result['summary'] = {"success": False, "data": None}
        try:
            logger.info("分析自选股表现...")
            result['watchlist_evening'] = self.analyzer.analyze_watchlist_evening(data)
        except Exception as e:
            logger.error(f"watchlist 失败: {e}")
            result['watchlist_evening'] = {"success": False, "data": None}
        
        # 新模块：每个独立 try-except，不因单个失败中断
        for key in ['market_overview', 'market_depth', 'major_indices', 'global_assets']:
            try:
                result[key] = data.get(key, {})
                logger.info(f"[OK] {key}: data ready")
            except Exception as e:
                logger.error(f"{key} 失败: {e}")
                result[key] = {"success": False, "data": None}
        
        # 技术分析类
        for key in ['technical', 'comprehensive', 'theme_tracking']:
            try:
                method = getattr(self.analyzer, f'analyze_{key}', None)
                if method:
                    result[key] = method(data)
                    logger.info(f"[OK] {key}: success={result[key].get('success')}")
                else:
                    result[key] = {"success": False, "data": None}
            except Exception as e:
                logger.error(f"{key} 失败: {e}")
                result[key] = {"success": False, "data": None, "error": str(e)}
        
        # 传递原始数据供渲染器使用
        for key in ['index_sh', 'index_sz', 'index_cyb', 'sentiment', 'money_flow',
                     'industry_fund_flow', 'sectors', 'lhb']:
            result[key] = data.get(key, {})
        
        # 新闻分类
        try:
            news_list = data.get('news', {}).get('data', [])
            result['news'] = self.analyzer.classify_news(news_list)
        except Exception as e:
            logger.error(f"news 失败: {e}")
            result['news'] = {"success": False, "data": []}
        
        logger.info(f"analysis_result keys: {list(result.keys())}")
        return result

    def _save_report(self, markdown, mode, dt):
        output_config = self.config.get('output', {})
        base_dir = output_config.get('base_dir', 'reports')
        sub_dir = output_config.get(f'{mode}_subdir', mode)

        # 处理绝对路径和相对路径
        if os.path.isabs(base_dir):
            # 如果是绝对路径，直接使用
            base_path = base_dir
        else:
            # 如果是相对路径，使用项目根目录
            project_root = os.path.dirname(current_dir)
            base_path = os.path.join(project_root, base_dir)
        
        output_dir = os.path.join(base_path, sub_dir)
        os.makedirs(output_dir, exist_ok=True)

        date_str = format_date(dt, '%Y%m%d')
        mode_name = '早报' if mode == 'morning' else '晚报'
        filename = f'A股{mode_name}-{date_str}.md'
        output_path = os.path.join(output_dir, filename)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown)

        logger.info(f"报告已保存: {output_path}")
        return output_path


def main():
    parser = argparse.ArgumentParser(description='A股日报生成器')
    parser.add_argument('--mode', type=str, choices=['morning', 'evening'],
                        default='morning', help='早报或晚报 (默认: morning)')
    parser.add_argument('--date', type=str, default=None,
                        help='日期 (默认: 今天)')
    parser.add_argument('--config', type=str, default=None,
                        help='配置文件路径')
    parser.add_argument('--publish', action='store_true',
                        help='发布到飞书（需要配置 feishu）')
    parser.add_argument('--outdir', type=str, default=None,
                        help='输出目录（覆盖配置文件中的设置）')

    args = parser.parse_args()

    generator = ReportGenerator(args.config)

    # 如果指定了outdir，覆盖配置
    if args.outdir:
        output_config = generator.config.get('output', {})
        output_config['base_dir'] = args.outdir
        generator.config['output'] = output_config

    if args.mode == 'morning':
        result = generator.generate_morning_report(args.date, publish=args.publish)
    else:
        result = generator.generate_evening_report(args.date, publish=args.publish)

    print("\n" + "="*80)
    print(result['markdown'])
    print("="*80 + "\n")

    if args.publish and result.get('publish', {}).get('success'):
        print(f"✅ 已发布到飞书: {result['publish']['doc_url']}")
    elif args.publish:
        print(f"⚠️ 发布失败: {result.get('publish', {}).get('error', '未知错误')}")


if __name__ == '__main__':
    main()
