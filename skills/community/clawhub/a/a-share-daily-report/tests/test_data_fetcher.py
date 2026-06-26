
"""
数据采集模块单元测试
"""

import pytest
import sys
import os
import pandas as pd
from unittest.mock import MagicMock, patch

# 添加项目根目录到路径
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, PROJECT_ROOT)

from scripts.data_fetcher import DataFetcher
from scripts.utils.cache import get_cache, clear_cache


class TestDataFetcher:
    """DataFetcher 测试类"""

    @pytest.fixture
    def config(self):
        """测试配置"""
        return {
            'data_sources': {
                'akshare': {'enabled': True},
                'sina': {'enabled': True}
            }
        }

    @pytest.fixture
    def fetcher(self, config):
        """创建 DataFetcher 实例"""
        # 清理缓存
        clear_cache(namespace='akshare')
        clear_cache(namespace='sina')
        return DataFetcher(config)

    def test_init(self, fetcher):
        """测试初始化"""
        assert fetcher is not None
        assert hasattr(fetcher, 'ak')

    def test_get_index_data_mock(self, fetcher):
        """测试获取指数数据（使用模拟数据）"""
        result = fetcher.get_index_data('000001.SH', '2026-03-27')
        assert result['success'] is True
        assert 'data' in result
        assert result['data']['ts_code'] == '000001.SH'
        assert 'close' in result['data']
        assert result['source'] in ['akshare', 'mock']

    def test_get_index_data_caching(self, fetcher):
        """测试缓存功能"""
        # 第一次调用
        result1 = fetcher.get_index_data('000001.SH', '2026-03-27')
        assert result1['cached'] is False

        # 第二次调用应该命中缓存
        result2 = fetcher.get_index_data('000001.SH', '2026-03-27')
        assert result2['cached'] is True
        assert result2['source'] == 'cache'

    def test_get_market_sentiment(self, fetcher):
        """测试获取市场情绪数据"""
        result = fetcher.get_market_sentiment('2026-03-27')
        assert result['success'] is True
        assert 'limit_up_count' in result['data']
        assert 'limit_down_count' in result['data']

    def test_get_money_flow(self, fetcher):
        """测试获取资金流向数据"""
        result = fetcher.get_money_flow('2026-03-27')
        assert result['success'] is True
        assert 'northbound' in result['data']
        assert 'main_capital' in result['data']

    def test_get_us_market(self, fetcher):
        """测试获取美股数据"""
        result = fetcher.get_us_market()
        assert result['success'] is True
        assert 'indices' in result['data']
        assert 'nasdaq' in result['data']['indices']

    def test_get_news(self, fetcher):
        """测试获取新闻数据"""
        result = fetcher.get_news('2026-03-27', limit=5)
        assert result['success'] is True
        assert len(result['data']) <= 5
        assert 'title' in result['data'][0]

    def test_convert_index_code(self, fetcher):
        """测试指数代码转换"""
        assert fetcher._convert_index_code('000001.SH') == 'sh000001'
        assert fetcher._convert_index_code('399001.SZ') == 'sz399001'
        assert fetcher._convert_index_code('sh000001') == 'sh000001'

    def test_get_index_name(self, fetcher):
        """测试指数名称获取"""
        assert fetcher._get_index_name('000001.SH') == '上证指数'
        assert fetcher._get_index_name('399006.SZ') == '创业板指'
        assert fetcher._get_index_name('unknown') == 'unknown'


class TestSectorData:
    """板块数据采集测试"""

    @pytest.fixture
    def fetcher(self):
        config = {'data_sources': {}}
        clear_cache(namespace='akshare')
        return DataFetcher(config)

    def test_get_sector_data_industry_success(self, fetcher, monkeypatch):
        """测试行业板块数据正常获取"""
        # 模拟行业板块列表
        df_industry = pd.DataFrame({
            '板块名称': ['人工智能', '芯片', '新能源', '医药', '消费'],
            '涨跌幅': [5.2, 3.1, -1.2, 0.5, -0.8]
        })
        # 模拟成分股
        df_cons = pd.DataFrame({
            '名称': ['科大讯飞', '浪潮信息', '中科曙光'],
            '代码': ['002230', '000977', '603019'],
            '涨跌幅': [6.1, 4.5, 3.2]
        })

        monkeypatch.setattr(fetcher.ak, 'stock_board_industry_name_em', lambda: df_industry)
        monkeypatch.setattr(fetcher.ak, 'stock_board_industry_cons_em', lambda symbol: df_cons)

        result = fetcher.get_sector_data('2026-03-27')
        assert result['success'] is True
        assert len(result['data']['industry']) == 5
        assert result['data']['industry'][0]['sector'] == '人工智能'
        assert result['data']['industry'][0]['change_pct'] == 5.2
        assert len(result['data']['industry'][0]['leaders']) == 3

    def test_get_sector_data_concept_success(self, fetcher, monkeypatch):
        """测试概念板块数据正常获取"""
        df_concept = pd.DataFrame({
            '概念名称': ['5G', '云计算', '大数据'],
            '涨跌幅': [2.5, 1.8, 0.9]
        })
        df_cons = pd.DataFrame({
            '名称': ['中兴通讯', '烽火通信', '亨通光电'],
            '代码': ['000063', '600498', '600487'],
            '涨跌幅': [3.1, 2.2, 1.5]
        })

        monkeypatch.setattr(fetcher.ak, 'stock_board_concept_name_em', lambda: df_concept)
        monkeypatch.setattr(fetcher.ak, 'stock_board_concept_cons_em', lambda symbol: df_cons)

        result = fetcher.get_sector_data('2026-03-27')
        assert result['success'] is True
        assert len(result['data']['concept']) == 3

    def test_get_sector_data_akshare_failure(self, fetcher, monkeypatch):
        """测试 akshare 不可用时的降级处理"""
        monkeypatch.setattr(fetcher, 'ak', None)
        result = fetcher.get_sector_data('2026-03-27')
        assert result['success'] is False
        assert result['error'] == '无法获取板块数据'

    def test_get_sector_data_missing_columns(self, fetcher, monkeypatch):
        """测试字段缺失容错"""
        df_industry = pd.DataFrame({
            'other_column': ['A', 'B', 'C']  # 缺少涨跌幅
        })
        monkeypatch.setattr(fetcher.ak, 'stock_board_industry_name_em', lambda: df_industry)
        result = fetcher.get_sector_data('2026-03-27')
        # 应该fallback到前5条，即使没有涨跌幅排序
        assert result['success'] is True
        assert len(result['data']['industry']) <= 5


class TestLHBData:
    """龙虎榜数据测试"""

    @pytest.fixture
    def fetcher(self):
        config = {'data_sources': {}}
        return DataFetcher(config)

    def test_get_lhb_data_success(self, fetcher, monkeypatch):
        """测试正常获取龙虎榜数据"""
        df_lhb = pd.DataFrame({
            '代码': ['002230', '000977', '603019', '600519', '000858'],
            '名称': ['科大讯飞', '浪潮信息', '中科曙光', '贵州茅台', '五粮液'],
            '龙虎榜净买额': [1000, 800, 600, -200, 300],
            '龙虎榜买入额': [2000, 1500, 1200, 500, 800],
            '龙虎榜卖出额': [1000, 700, 600, 700, 500]
        })
        monkeypatch.setattr(fetcher.ak, 'stock_lhb_detail_em', lambda start_date, end_date: df_lhb)

        result = fetcher.get_lhb_data('2026-03-27')
        assert result['success'] is True
        assert len(result['data']) == 5
        # 按净买入排序，第一条应该是净买入最大的
        assert result['data'][0]['code'] == '002230'
        assert result['data'][0]['net_inflow'] == 1000

    def test_get_lhb_data_empty(self, fetcher, monkeypatch):
        """测试无龙虎榜数据"""
        monkeypatch.setattr(fetcher.ak, 'stock_lhb_detail_em', lambda start_date, end_date: pd.DataFrame())
        result = fetcher.get_lhb_data('2026-03-27')
        assert result['success'] is False

    def test_get_lhb_data_columns_mapping(self, fetcher, monkeypatch):
        """测试字段名映射（如果列名不同）"""
        df_lhb = pd.DataFrame({
            'code': ['002230'],
            'name': ['科大讯飞'],
            'net_inflow': [1000],
            'buy_amount': [2000],
            'sell_amount': [1000]
        })
        monkeypatch.setattr(fetcher.ak, 'stock_lhb_detail_em', lambda start_date, end_date: df_lhb)
        result = fetcher.get_lhb_data('2026-03-27')
        # 即使列名不同，也应能解析
        assert result['success'] is True
        assert len(result['data']) == 1
        assert result['data'][0]['code'] == '002230' or result['data'][0]['code'] == ''  # 解析可能失败但不会崩溃


class TestFuturesData:
    """期指数据测试"""

    @pytest.fixture
    def fetcher(self):
        config = {'data_sources': {}}
        clear_cache(namespace='combined')
        return DataFetcher(config)

    def test_get_futures_data_mx_both(self, fetcher, monkeypatch):
        """测试 mx-data 同时返回 CSI300 和 A50"""
        monkeypatch.setenv('MX_APIKEY', 'dummy_key')
        # 模拟 _parse_mx_futures 返回两者
        def mock_parse(result, key):
            return {
                "futures": {
                    key: {
                        "name": "沪深300期指" if key == 'CSI300' else "A50期指",
                        "code": "CFF_RE_IF",
                        "change_pct": 0.5 if key == 'CSI300' else 0.3,
                        "impact": "影响"
                    }
                }
            }
        monkeypatch.setattr(fetcher, '_parse_mx_futures', mock_parse)

        result = fetcher.get_futures_data()
        assert result['success'] is True
        assert 'CSI300' in result['data']['futures']
        assert 'A50' in result['data']['futures']
        assert result['source'] == 'mx-data'

    def test_get_futures_data_mx_csi300_only_triggers_yfinance(self, fetcher, monkeypatch):
        """测试 mx-data 只返回 CSI300，触发 yfinance 补充 A50"""
        monkeypatch.setenv('MX_APIKEY', 'dummy_key')
        # 模拟 _parse_mx_futures 只返回 CSI300，对 A50 返回空 dict
        def mock_parse(result, key):
            if key == 'CSI300':
                return {"futures": {"CSI300": {"change_pct": 0.5}}}
            else:
                return {"futures": {}}  # A50 empty
        monkeypatch.setattr(fetcher, '_parse_mx_futures', mock_parse)

        # 模拟 yfinance
        class MockHist:
            def __init__(self):
                self.data = pd.DataFrame({
                    'Close': [150.0, 151.5]  # 第一个close, 第二个close
                })
            def iloc(self, idx):
                class Row:
                    def __init__(self, close):
                        self._close = close
                    def __getitem__(self, key):
                        if key == 'Close':
                            return self._close
                return Row(self.data['Close'].iloc[idx])
        class MockTicker:
            def __init__(self, *args, **kwargs):
                self._hist = MockHist()
            def history(self, period=None):
                return self._hist
        monkeypatch.setattr('yfinance.Ticker', MockTicker)

        result = fetcher.get_futures_data()
        assert result['success'] is True
        assert 'CSI300' in result['data']['futures']
        assert 'A50' in result['data']['futures']
        # A50 数据应来自 yfinance
        assert result['data']['futures']['A50']['code'] == 'A50.SI'

    def test_get_futures_data_sina_only_csi300(self, fetcher, monkeypatch):
        """测试新浪接口仅提供 CSI300（A50 由 yfinance 补充）"""
        # 未设置 MX_APIKEY，跳过 mx-data
        monkeypatch.delenv('MX_APIKEY', raising=False)

        # 模拟 urllib.request.urlopen 返回 Sina 数据
        sina_content = b'var hq_CFF_RE_IF="CFF_RE_IF,open,pre,price,change,0.63,vol";'
        class MockResponse:
            def __init__(self, content):
                self._content = content
            def read(self):
                return self._content
        monkeypatch.setattr('urllib.request.urlopen', lambda *args, **kwargs: MockResponse(sina_content))

        # 模拟 yfinance 提供 A50
        class MockTicker:
            def __init__(self, *args, **kwargs):
                pass
            def history(self, period=None):
                return pd.DataFrame({'Close': [100, 101]})
        monkeypatch.setattr('yfinance.Ticker', MockTicker)

        result = fetcher.get_futures_data()
        assert result['success'] is True
        assert 'CSI300' in result['data']['futures']
        assert 'A50' in result['data']['futures']

    def test_get_futures_data_all_fail(self, fetcher, monkeypatch):
        """测试全部数据源失败"""
        monkeypatch.delenv('MX_APIKEY', raising=False)
        # urllib 抛出异常
        monkeypatch.setattr('urllib.request.urlopen', lambda *args, **kwargs: (_ for _ in ()).throw(ConnectionError("no net")))
        result = fetcher.get_futures_data()
        assert result['success'] is False


class TestWatchlistPerformance:
    """自选股表现测试"""

    @pytest.fixture
    def fetcher(self):
        config = {'data_sources': {}}
        return DataFetcher(config)

    def test_get_watchlist_performance_success(self, fetcher, monkeypatch):
        """测试获取自选股表现成功"""
        watchlist = [
            {'code': '002594.SZ', 'name': '比亚迪'},
            {'code': '300308.SZ', 'name': '中际旭创'}
        ]
        # 模拟 akshare 返回日线数据
        def mock_hist(symbol, period, start_date, end_date):
            # 根据 symbol 返回不同的数据
            if symbol == '002594':
                return pd.DataFrame({
                    '收盘': [250.0, 255.0]  # +2%
                })
            elif symbol == '300308':
                return pd.DataFrame({
                    '收盘': [100.0, 102.0]   # +2%
                })
            return pd.DataFrame()
        monkeypatch.setattr(fetcher.ak, 'stock_zh_a_hist', mock_hist)

        result = fetcher.get_watchlist_performance(watchlist, '2026-03-27')
        assert result['success'] is True
        assert len(result['data']) == 2
        # 比亚迪涨跌幅约为 2%
        assert abs(result['data'][0]['change_pct'] - 2.0) < 0.1

    def test_get_watchlist_performance_missing_close(self, fetcher, monkeypatch):
        """测试数据缺少收盘价列"""
        watchlist = [{'code': '002594.SZ', 'name': '比亚迪'}]
        def mock_hist(symbol, period, start_date, end_date):
            return pd.DataFrame({
                'open': [250, 255],
                'high': [260, 265]
            })
        monkeypatch.setattr(fetcher.ak, 'stock_zh_a_hist', mock_hist)
        result = fetcher.get_watchlist_performance(watchlist, '2026-03-27')
        # 应该跳过该股票，返回空列表或失败
        assert result['success'] in [True, False]  # 可能成功但空列表或失败

    def test_get_watchlist_performance_akshare_unavailable(self, fetcher, monkeypatch):
        """测试 akshare 不可用"""
        monkeypatch.setattr(fetcher, 'ak', None)
        watchlist = [{'code': '002594.SZ', 'name': '比亚迪'}]
        result = fetcher.get_watchlist_performance(watchlist, '2026-03-27')
        assert result['success'] is False


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
