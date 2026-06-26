
"""
渲染模块单元测试
"""

import pytest
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, PROJECT_ROOT)

from scripts.renderer import Renderer
from scripts.analyzer import Analyzer


class TestRenderer:
    """Renderer 测试类"""

    @pytest.fixture
    def config(self):
        """测试配置"""
        return {
            'watchlist': {'path': 'config/watchlist.yaml'}
        }

    @pytest.fixture
    def renderer(self, config):
        """创建 Renderer 实例"""
        return Renderer(config)

    @pytest.fixture
    def sample_analysis_result(self):
        """生成示例分析结果"""
        analyzer = Analyzer({'watchlist': {'path': 'config/watchlist.yaml'}})
        data = {}
        data['summary'] = analyzer.generate_summary({}, mode='morning')
        data['watchlist_morning'] = analyzer.analyze_watchlist_morning({})
        data['strategy'] = analyzer.generate_trading_strategy({})
        data['focus_stocks'] = analyzer.analyze_focus_stocks({})
        data['position'] = analyzer.suggest_position({})
        data['us_market'] = {
            'data': {
                'indices': {
                    'nasdaq': {'change_pct': 0.53},
                    'sp500': {'change_pct': 0.36},
                    'dow': {'change_pct': -0.12}
                },
                'chinadotcom': {
                    'tencent': {'change_pct': 5.15}
                }
            }
        }
        data['news'] = {'data': [
            {'title': '测试新闻', 'content': '新闻内容', 'importance': 'medium'}
        ]}
        return data

    def test_init(self, renderer):
        """测试初始化"""
        assert renderer is not None

    def test_render_morning_report_structure(self, renderer, sample_analysis_result):
        """测试早报结构"""
        markdown = renderer.render_morning_report(sample_analysis_result, '2026-03-28')
        assert '# A股日报 - 早报预测版' in markdown
        assert '【30秒总览】' in markdown
        assert '【自选股简洁预测】' in markdown
        assert '【核心决策】' in markdown
        assert '【昨夜今晨】' in markdown

    def test_render_morning_report_content(self, renderer, sample_analysis_result):
        """测试早报内容"""
        markdown = renderer.render_morning_report(sample_analysis_result, '2026-03-28')
        # 检查关键内容
        assert '一句话总结' in markdown
        assert '核心机会' in markdown
        assert '风险提示' in markdown
        assert '自选股' in markdown
        assert '仓位建议' in markdown

    def test_render_evening_report_structure(self, renderer):
        """测试晚报结构"""
        # 生成示例晚报复盘数据
        analyzer = Analyzer({'watchlist': {'path': 'config/watchlist.yaml'}})
        data = {}
        data['summary'] = analyzer.generate_summary({}, mode='evening')
        data['watchlist_evening'] = analyzer.analyze_watchlist_evening({})
        data['news'] = {'data': [
            {'title': '测试新闻', 'content': '新闻内容', 'importance': 'medium'}
        ]}

        markdown = renderer.render_evening_report(data, '2026-03-28')
        assert '# A股日报 - 晚报复盘版' in markdown
        assert '【30秒总览】' in markdown
        assert '【自选股复盘】' in markdown
        assert '【今日复盘】' in markdown
        assert '【明日展望】' in markdown

    def test_render_empty_data(self, renderer):
        """测试数据缺失时的渲染"""
        empty_result = {
            'summary': None,
            'watchlist_morning': {'data': []},
            'strategy': {'data': {}},
            'focus_stocks': {'data': []},
            'position': {'data': {}},
            'us_market': {},
            'news': {'data': []}
        }
        markdown = renderer.render_morning_report(empty_result, '2026-03-28')
        # 应该显示"数据获取失败"或基本结构
        assert '# A股日报' in markdown or len(markdown) > 0

    def test_percentage_formatting(self, renderer):
        """测试百分比格式化（要求总是保留两位小数）"""
        from scripts.utils import format_percent
        assert format_percent(0.5) == '50.00%'
        assert format_percent(1) == '100.00%'
        assert format_percent(-0.34) == '-34.00%'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
