"""P0: 数据源异常处理测试 - 连接失败、超时、缓存、多数据源切换"""
import pytest
import time
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from datetime import date, timedelta


class TestCache:
    """缓存机制测试"""

    def test_cache_ttl_expiry(self):
        """缓存过期后返回 None"""
        from stock_skill.providers.providers import _Cache
        cache = _Cache(ttl=0.1)  # 100ms TTL
        cache.set("key1", "value1")
        assert cache.get("key1") == "value1"
        time.sleep(0.15)
        assert cache.get("key1") is None

    def test_cache_overwrite(self):
        """同 key 覆盖写入返回新值"""
        from stock_skill.providers.providers import _Cache
        cache = _Cache()
        cache.set("key1", "old_value")
        cache.set("key1", "new_value")
        assert cache.get("key1") == "new_value"

    def test_cache_nonexistent_key(self):
        """不存在的 key 返回 None"""
        from stock_skill.providers.providers import _Cache
        cache = _Cache()
        assert cache.get("nonexistent") is None

    def test_cache_custom_ttl(self):
        """自定义 TTL 覆盖默认值"""
        from stock_skill.providers.providers import _Cache
        cache = _Cache(ttl=300)
        cache.set("key1", "value1", ttl=0.1)
        time.sleep(0.15)
        assert cache.get("key1") is None


class TestRetryMechanism:
    """重试机制测试"""

    @patch("stock_skill.providers.providers.requests.get")
    def test_retry_on_connection_error(self, mock_get):
        """连接失败触发重试"""
        mock_get.side_effect = ConnectionError("Connection refused")
        from stock_skill.providers.providers import EastMoneyProvider
        provider = EastMoneyProvider()
        with pytest.raises(ConnectionError):
            provider.get_realtime_quote("600036.SH")

    @patch("stock_skill.providers.providers.requests.get")
    def test_retry_on_timeout(self, mock_get):
        """超时触发重试"""
        mock_get.side_effect = TimeoutError("Request timeout")
        from stock_skill.providers.providers import EastMoneyProvider
        provider = EastMoneyProvider()
        with pytest.raises(TimeoutError):
            provider.get_realtime_quote("600036.SH")

    @patch("stock_skill.providers.providers.requests.get")
    def test_no_retry_on_value_error(self, mock_get):
        """非网络异常不重试"""
        mock_get.side_effect = ValueError("Invalid data")
        from stock_skill.providers.providers import EastMoneyProvider
        provider = EastMoneyProvider()
        with pytest.raises(ValueError):
            provider.get_realtime_quote("600036.SH")


class TestTushareProvider:
    """Tushare 数据源测试"""

    @patch("stock_skill.providers.providers.ts")
    def test_tushare_empty_result(self, mock_ts):
        """Mock 返回空 DataFrame"""
        mock_ts.pro_api.return_value.daily.return_value = pd.DataFrame()
        from stock_skill.providers.providers import TushareProvider
        provider = TushareProvider()
        result = provider.get_daily("600036.SH", "20240101", "20240105")
        assert result.empty

    @patch("stock_skill.providers.providers.ts")
    def test_tushare_none_result(self, mock_ts):
        """Mock 返回 None"""
        mock_ts.pro_api.return_value.daily.return_value = None
        from stock_skill.providers.providers import TushareProvider
        provider = TushareProvider()
        result = provider.get_daily("600036.SH", "20240101", "20240105")
        assert result.empty

    @patch("stock_skill.providers.providers.ts")
    def test_tushare_stock_info(self, mock_ts):
        """股票信息查询"""
        mock_ts.pro_api.return_value.stock_basic.return_value = pd.DataFrame({
            "ts_code": ["600036.SH"],
            "name": ["招商银行"],
            "industry": ["银行"],
            "market": ["主板"]
        })
        from stock_skill.providers.providers import TushareProvider
        provider = TushareProvider()
        info = provider.get_stock_info("600036.SH")
        assert info.name == "招商银行"
        assert info.industry == "银行"

    def test_import_error_graceful(self):
        """tushare 未安装时优雅降级"""
        with patch.dict("sys.modules", {"tushare": None}):
            from stock_skill.providers.providers import TushareProvider
            provider = TushareProvider()
            assert provider._pro is None
            result = provider.get_daily("600036.SH", "20240101", "20240105")
            assert result.empty


class TestEastMoneyProvider:
    """东方财富数据源测试"""

    def test_secid_sh(self):
        """SH 后缀 -> 1.xxx"""
        from stock_skill.providers.providers import EastMoneyProvider
        assert EastMoneyProvider._secid("600036.SH") == "1.600036"

    def test_secid_sz(self):
        """SZ 后缀 -> 0.xxx"""
        from stock_skill.providers.providers import EastMoneyProvider
        assert EastMoneyProvider._secid("000001.SZ") == "0.000001"

    @patch("stock_skill.providers.providers.requests.get")
    def test_realtime_quote_parse(self, mock_get):
        """行情数据解析正确"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": {
                "f57": "600036",
                "f58": "招商银行",
                "f43": 3650,
                "f169": 50,
                "f170": 137,
                "f46": 1400000,
                "f44": 3680,
                "f51": 3600,
            }
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        from stock_skill.providers.providers import EastMoneyProvider
        provider = EastMoneyProvider()
        quote = provider.get_realtime_quote("600036.SH")

        assert quote["code"] == "600036.SH"
        assert quote["name"] == "招商银行"
        assert quote["price"] == 36.5
        assert quote["high"] == 36.8
        assert quote["low"] == 36.0

    @patch("stock_skill.providers.providers.requests.get")
    def test_realtime_quote_empty_data(self, mock_get):
        """行情数据为空"""
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": None}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        from stock_skill.providers.providers import EastMoneyProvider
        provider = EastMoneyProvider()
        quote = provider.get_realtime_quote("600036.SH")
        assert quote == {}

    @patch("stock_skill.providers.providers.requests.get")
    def test_money_flow_parse(self, mock_get):
        """资金流向解析正确"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": {
                "klines": ["20240101,1000000,500000,300000,200000,-100000"]
            }
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        from stock_skill.providers.providers import EastMoneyProvider
        provider = EastMoneyProvider()
        flow = provider.get_money_flow("600036.SH")

        assert flow is not None
        assert flow.code == "600036.SH"


class TestYahooProvider:
    """Yahoo 数据源测试"""

    def test_convert_code_sh(self):
        """SH -> SS 转换"""
        from stock_skill.providers.providers import YahooProvider
        provider = YahooProvider()
        assert provider._convert_code("600036.SH") == "600036.SS"

    def test_convert_code_sz(self):
        """SZ 保持不变"""
        from stock_skill.providers.providers import YahooProvider
        provider = YahooProvider()
        assert provider._convert_code("000001.SZ") == "000001.SZ"

    def test_convert_code_hk(self):
        """HK 保持不变"""
        from stock_skill.providers.providers import YahooProvider
        provider = YahooProvider()
        assert provider._convert_code("0700.HK") == "0700.HK"

    def test_convert_code_us(self):
        """美股代码保持不变"""
        from stock_skill.providers.providers import YahooProvider
        provider = YahooProvider()
        assert provider._convert_code("AAPL") == "AAPL"

    def test_import_error_graceful(self):
        """yfinance 未安装时优雅降级"""
        with patch.dict("sys.modules", {"yfinance": None}):
            from stock_skill.providers.providers import YahooProvider
            provider = YahooProvider()
            assert provider._yf is None
            result = provider.get_daily("AAPL", "20240101", "20240105")
            assert result.empty

    def test_empty_ticker_result(self):
        """Ticker 返回空数据"""
        mock_yf_module = MagicMock()
        mock_ticker = MagicMock()
        mock_ticker.history.return_value = pd.DataFrame()
        mock_yf_module.Ticker.return_value = mock_ticker

        with patch.dict("sys.modules", {"yfinance": mock_yf_module}):
            from stock_skill.providers.providers import YahooProvider
            provider = YahooProvider()
            provider._yf = mock_yf_module
            result = provider.get_daily("AAPL", "20240101", "20240105")
            assert result.empty


class TestLongportProvider:
    """长桥数据源测试"""

    def test_convert_code_sh(self):
        """SH 保持不变"""
        from stock_skill.providers.providers import LongportProvider
        provider = LongportProvider()
        assert provider._convert_code("600036.SH") == "600036.SH"

    def test_convert_code_sz(self):
        """SZ 保持不变"""
        from stock_skill.providers.providers import LongportProvider
        provider = LongportProvider()
        assert provider._convert_code("000001.SZ") == "000001.SZ"

    def test_convert_code_hk(self):
        """HK 保持不变"""
        from stock_skill.providers.providers import LongportProvider
        provider = LongportProvider()
        assert provider._convert_code("0700.HK") == "0700.HK"

    def test_import_error_graceful(self):
        """longport 未安装时优雅降级"""
        with patch.dict("sys.modules", {"longport": None, "longport.openapi": None}):
            from stock_skill.providers.providers import LongportProvider
            provider = LongportProvider()
            provider._init_context()
            assert provider._quote_ctx is None
            result = provider.get_quote(["600036.SH"])
            assert result == []


class TestDataGateway:
    """DataGateway 多数据源切换测试"""

    @patch("stock_skill.providers.providers.TushareProvider")
    @patch("stock_skill.providers.providers.YahooProvider")
    def test_get_kline_tushare(self, mock_yahoo, mock_tushare):
        """默认使用 Tushare"""
        mock_tushare.return_value.get_daily.return_value = pd.DataFrame({
            "trade_date": ["20240101"], "open": [10], "high": [11],
            "low": [9], "close": [10.5], "vol": [1000000], "amount": [10500000]
        })
        mock_tushare.return_value._pro = True
        from stock_skill.providers.providers import DataGateway
        gw = DataGateway()
        df = gw.get_kline("600036.SH", source="tushare")
        assert not df.empty
        mock_tushare.return_value.get_daily.assert_called_once()

    @patch("stock_skill.providers.providers.TushareProvider")
    @patch("stock_skill.providers.providers.YahooProvider")
    def test_get_kline_yahoo(self, mock_yahoo, mock_tushare):
        """source=yahoo 时使用 Yahoo"""
        mock_yahoo.return_value.get_daily.return_value = pd.DataFrame({
            "date": ["2024-01-01"], "open": [10], "high": [11],
            "low": [9], "close": [10.5], "volume": [1000000]
        })
        from stock_skill.providers.providers import DataGateway
        gw = DataGateway()
        df = gw.get_kline("AAPL", source="yahoo")
        assert not df.empty
        mock_yahoo.return_value.get_daily.assert_called_once()

    @patch("stock_skill.providers.providers.EastMoneyProvider")
    @patch("stock_skill.providers.providers.YahooProvider")
    @patch("stock_skill.providers.providers.LongportProvider")
    def test_get_realtime_quote_source_switch(self, mock_longport, mock_yahoo, mock_eastmoney):
        """实时行情多数据源切换"""
        mock_eastmoney.return_value.get_realtime_quote.return_value = {"price": 36.5}
        mock_yahoo.return_value.get_realtime_quote.return_value = {"price": 150.0}
        mock_longport.return_value.get_realtime_quote.return_value = {"price": 350.0}

        from stock_skill.providers.providers import DataGateway
        gw = DataGateway()

        # 默认 eastmoney
        quote1 = gw.get_realtime_quote("600036.SH")
        assert quote1["price"] == 36.5

        # yahoo
        quote2 = gw.get_realtime_quote("AAPL", source="yahoo")
        assert quote2["price"] == 150.0

        # longport
        quote3 = gw.get_realtime_quote("0700.HK", source="longport")
        assert quote3["price"] == 350.0

    def test_tushare_not_installed_kline(self):
        """tushare 未安装时 K线返回空 DataFrame"""
        with patch.dict("sys.modules", {"tushare": None}):
            from stock_skill.providers.providers import DataGateway
            gw = DataGateway()
            df = gw.get_kline("600036.SH", source="tushare")
            assert df.empty

    def test_tushare_not_installed_market_snapshot(self):
        """tushare 未安装时市场快照返回空 DataFrame"""
        with patch.dict("sys.modules", {"tushare": None}):
            from stock_skill.providers.providers import DataGateway
            gw = DataGateway()
            df = gw.get_market_snapshot()
            assert df.empty

    def test_tushare_not_installed_stock_info(self):
        """tushare 未安装时股票信息返回默认值"""
        with patch.dict("sys.modules", {"tushare": None}):
            from stock_skill.providers.providers import DataGateway
            gw = DataGateway()
            info = gw.get_stock_info("600036.SH")
            assert info.code == "600036.SH"
            assert info.name == "600036.SH"

    def test_tushare_not_installed_dragon_tiger(self):
        """tushare 未安装时龙虎榜返回空列表"""
        with patch.dict("sys.modules", {"tushare": None}):
            from stock_skill.providers.providers import DataGateway
            gw = DataGateway()
            result = gw.get_dragon_tiger()
            assert result == []

    def test_tushare_not_installed_trade_dates(self):
        """tushare 未安装时交易日期返回空列表"""
        with patch.dict("sys.modules", {"tushare": None}):
            from stock_skill.providers.providers import DataGateway
            gw = DataGateway()
            result = gw.get_recent_trade_dates()
            assert result == []


class TestCacheIntegration:
    """缓存集成测试"""

    @patch("stock_skill.providers.providers.requests.get")
    def test_cache_hit_no_network(self, mock_get):
        """缓存命中时不发起网络请求"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": {"f57": "600036", "f58": "招商银行", "f43": 3650, "f169": 50, "f170": 137, "f46": 1400000, "f44": 3680, "f51": 3600}
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        from stock_skill.providers.providers import EastMoneyProvider, _Cache
        # 清除缓存
        cache = _Cache()
        cache._s.clear()

        provider = EastMoneyProvider()
        # 第一次调用
        quote1 = provider.get_realtime_quote("600036.SH")
        # 第二次调用（应命中缓存）
        quote2 = provider.get_realtime_quote("600036.SH")

        assert quote1 == quote2
        # 只应发起一次网络请求
        assert mock_get.call_count == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
