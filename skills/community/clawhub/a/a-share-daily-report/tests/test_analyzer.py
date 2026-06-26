
"""
分析模块单元测试
"""

import pytest
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, PROJECT_ROOT)

from scripts.analyzer import Analyzer


class TestAnalyzer:
    """Analyzer 测试类"""

    @pytest.fixture
    def config(self):
        """测试配置"""
        return {
            'watchlist': {
                'path': 'config/watchlist.yaml'
            }
        }

    @pytest.fixture
    def analyzer(self, config):
        """创建 Analyzer 实例"""
        return Analyzer(config)

    def test_init(self, analyzer):
        """测试初始化"""
        assert analyzer is not None
        assert hasattr(analyzer, 'watchlist')

    def test_load_watchlist(self, analyzer):
        """测试加载自选股"""
        assert isinstance(analyzer.watchlist, list)
        assert len(analyzer.watchlist) == 3  # 比亚迪、中际旭创、腾讯控股

        # 检查自选股结构
        for stock in analyzer.watchlist:
            assert 'code' in stock
            assert 'name' in stock

    def test_generate_morning_summary(self, analyzer):
        """测试生成早报30秒总览"""
        result = analyzer.generate_summary({}, mode='morning')
        assert result['success'] is True
        assert 'one_sentence' in result['data']
        assert 'core_opportunities' in result['data']
        assert 'risk_warnings' in result['data']

    def test_generate_evening_summary(self, analyzer):
        """测试生成晚报30秒总览"""
        result = analyzer.generate_summary({}, mode='evening')
        assert result['success'] is True
        assert 'one_sentence' in result['data']
        assert 'core_highlights' in result['data']
        assert 'tomorrow_outlook' in result['data']

    def test_analyze_watchlist_morning(self, analyzer):
        """测试自选股早报分析"""
        result = analyzer.analyze_watchlist_morning({})
        assert result['success'] is True
        assert len(result['data']) == len(analyzer.watchlist)

        for stock in result['data']:
            assert 'code' in stock
            assert 'name' in stock
            assert 'view' in stock
            assert 'reason' in stock

    def test_analyze_watchlist_evening(self, analyzer):
        """测试自选股晚报复盘"""
        result = analyzer.analyze_watchlist_evening({})
        assert result['success'] is True
        assert 'overall' in result['data']
        assert 'best' in result['data']
        assert 'worst' in result['data']

    def test_generate_trading_strategy(self, analyzer):
        """测试交易策略生成"""
        result = analyzer.generate_trading_strategy({})
        assert result['success'] is True
        assert 'strategy' in result['data']
        assert result['data']['strategy'] in ['offensive', 'defensive', 'waiting']
        assert 'confidence' in result['data']

    def test_analyze_focus_stocks(self, analyzer):
        """测试关注标的分析"""
        result = analyzer.analyze_focus_stocks({})
        assert result['success'] is True
        assert len(result['data']) >= 2

        for stock in result['data']:
            assert 'code' in stock
            assert 'name' in stock
            assert 'entry_range' in stock
            assert 'stop_loss' in stock

    def test_suggest_position(self, analyzer):
        """测试仓位建议"""
        result = analyzer.suggest_position({})
        assert result['success'] is True
        assert 'position_min' in result['data']
        assert 'position_max' in result['data']
        assert 'position_suggestion' in result['data']

    def test_classify_news(self, analyzer):
        """测试新闻分级"""
        news_list = [
            {'title': '重大新闻', 'importance': 'high'},
            {'title': '普通新闻', 'importance': 'medium'},
            {'title': '小新闻', 'importance': 'low'}
        ]
        result = analyzer.classify_news(news_list)
        assert result['success'] is True
        assert len(result['data']) == 3

        # 检查分级标记
        high_news = [n for n in result['data'] if n['importance'] == 'high'][0]
        assert '🔴' in high_news.get('level', '')


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
