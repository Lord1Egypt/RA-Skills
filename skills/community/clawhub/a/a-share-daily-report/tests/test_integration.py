
"""
集成测试 - 完整报告生成流程
"""

import pytest
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, PROJECT_ROOT)

from scripts.generate_report import ReportGenerator
from scripts.utils.cache import clear_cache


class TestIntegration:
    """集成测试类"""

    @pytest.fixture
    def cleanup(self):
        """清理测试环境"""
        # 清理缓存
        clear_cache(namespace='akshare')
        clear_cache(namespace='sina')
        # 清理报告目录
        reports_dir = os.path.join(os.path.dirname(__file__), '..', 'reports')
        if os.path.exists(reports_dir):
            for subdir in ['morning', 'evening']:
                dir_path = os.path.join(reports_dir, subdir)
                if os.path.exists(dir_path):
                    for file in os.listdir(dir_path):
                        if file.endswith('.md'):
                            os.remove(os.path.join(dir_path, file))
        yield
        # 测试后再次清理
        clear_cache()

    def test_morning_report_generation(self, cleanup):
        """测试早报完整生成流程"""
        generator = ReportGenerator()
        markdown = generator.generate_morning_report('2026-03-28')

        # 验证输出
        assert '# A股日报 - 早报预测版' in markdown
        assert '【30秒总览】' in markdown
        assert '【自选股简洁预测】' in markdown
        assert '比亚迪' in markdown
        assert '中际旭创' in markdown
        assert '腾讯控股' in markdown

        # 验证文件保存
        report_path = os.path.join(
            os.path.dirname(__file__), '..', 'reports', 'morning', 'A股早报-20260328.md'
        )
        assert os.path.exists(report_path)

        with open(report_path, 'r', encoding='utf-8') as f:
            content = f.read()
        assert content == markdown

    def test_evening_report_generation(self, cleanup):
        """测试晚报完整生成流程"""
        generator = ReportGenerator()
        markdown = generator.generate_evening_report('2026-03-28')

        # 验证输出
        assert '# A股日报 - 晚报复盘版' in markdown
        assert '【30秒总览】' in markdown
        assert '【自选股复盘】' in markdown
        assert '【今日复盘】' in markdown

        # 验证文件保存
        report_path = os.path.join(
            os.path.dirname(__file__), '..', 'reports', 'evening', 'A股晚报-20260328.md'
        )
        assert os.path.exists(report_path)

    def test_non_trading_day_handling(self, cleanup):
        """测试非交易日处理（2026-03-29 是周六）"""
        generator = ReportGenerator()
        markdown = generator.generate_morning_report('2026-03-29')

        # 应该使用前一个交易日（2026-03-27 或 2026-03-28）
        assert '# A股日报 - 早报预测版' in markdown
        # 日期应该是 2026-03-27 或 2026-03-28
        assert ('2026-03-27' in markdown) or ('2026-03-28' in markdown)

    def test_data_fetcher_integration(self):
        """测试数据采集器集成"""
        from scripts.data_fetcher import DataFetcher

        fetcher = DataFetcher({})

        # 测试所有数据接口
        result1 = fetcher.get_index_data('000001.SH', '2026-03-27')
        assert result1['success'] is True

        result2 = fetcher.get_market_sentiment('2026-03-27')
        assert result2['success'] is True

        result3 = fetcher.get_money_flow('2026-03-27')
        assert result3['success'] is True

        result4 = fetcher.get_us_market()
        assert result4['success'] is True

        result5 = fetcher.get_news('2026-03-27')
        assert result5['success'] is True

    def test_full_pipeline_structure(self, cleanup):
        """测试完整管道的内容结构"""
        generator = ReportGenerator()
        markdown = generator.generate_morning_report('2026-03-28')

        # 检查所有必要章节
        required_sections = [
            '【30秒总览】',
            '【自选股简洁预测】',
            '【核心决策】',
            '【昨夜今晨】',
            '国内要闻'
        ]

        for section in required_sections:
            assert section in markdown, f"缺少章节: {section}"

    def test_watchlist_loading(self):
        """测试自选股加载"""
        from scripts.analyzer import Analyzer

        analyzer = Analyzer({'watchlist': {'path': 'config/watchlist.yaml'}})

        assert len(analyzer.watchlist) == 3
        stock_codes = [s['code'] for s in analyzer.watchlist]
        assert '002594.SZ' in stock_codes  # 比亚迪
        assert '300308.SZ' in stock_codes  # 中际旭创
        assert '00700.HK' in stock_codes  # 腾讯控股


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
