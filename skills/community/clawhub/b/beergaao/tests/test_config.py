"""P1: 配置管理测试 - 环境变量加载、默认值、验证"""
import pytest
import os
from unittest.mock import patch


class TestConfigDefaults:
    """配置默认值测试"""

    def test_default_tushare_token(self):
        """默认 Tushare Token"""
        with patch.dict(os.environ, {}, clear=True):
            from stock_skill.config import reload_config
            cfg = reload_config()
            assert cfg.tushare_token == ""

    def test_default_max_single_position(self):
        """默认单只仓位上限"""
        with patch.dict(os.environ, {}, clear=True):
            from stock_skill.config import reload_config
            cfg = reload_config()
            assert cfg.max_single_position == 0.30

    def test_default_max_total_position(self):
        """默认总仓位上限"""
        with patch.dict(os.environ, {}, clear=True):
            from stock_skill.config import reload_config
            cfg = reload_config()
            assert cfg.max_total_position == 0.80

    def test_default_min_market_score(self):
        """默认最低市场评分"""
        with patch.dict(os.environ, {}, clear=True):
            from stock_skill.config import reload_config
            cfg = reload_config()
            assert cfg.min_market_score == 4.0

    def test_default_stop_loss_rate(self):
        """默认止损率"""
        with patch.dict(os.environ, {}, clear=True):
            from stock_skill.config import reload_config
            cfg = reload_config()
            assert cfg.stop_loss_rate == -0.04

    def test_default_target_rate(self):
        """默认止盈率"""
        with patch.dict(os.environ, {}, clear=True):
            from stock_skill.config import reload_config
            cfg = reload_config()
            assert cfg.target_rate == 0.06

    def test_default_hold_days(self):
        """默认持仓天数"""
        with patch.dict(os.environ, {}, clear=True):
            from stock_skill.config import reload_config
            cfg = reload_config()
            assert cfg.hold_days == 5

    def test_default_backtest_days(self):
        """默认回测天数"""
        with patch.dict(os.environ, {}, clear=True):
            from stock_skill.config import reload_config
            cfg = reload_config()
            assert cfg.backtest_days == 250

    def test_default_commission_rate(self):
        """默认佣金费率"""
        with patch.dict(os.environ, {}, clear=True):
            from stock_skill.config import reload_config
            cfg = reload_config()
            assert cfg.commission_rate == 0.0003

    def test_default_stamp_tax_rate(self):
        """默认印花税率"""
        with patch.dict(os.environ, {}, clear=True):
            from stock_skill.config import reload_config
            cfg = reload_config()
            assert cfg.stamp_tax_rate == 0.001


class TestConfigFromEnv:
    """环境变量加载测试"""

    def test_tushare_token_from_env(self):
        """从环境变量加载 Tushare Token"""
        with patch.dict(os.environ, {"TUSHARE_TOKEN": "test_token_123"}):
            from stock_skill.config import reload_config
            cfg = reload_config()
            assert cfg.tushare_token == "test_token_123"

    def test_max_single_position_from_env(self):
        """从环境变量加载单只仓位上限"""
        with patch.dict(os.environ, {"MAX_SINGLE_POSITION": "0.25"}):
            from stock_skill.config import reload_config
            cfg = reload_config()
            assert cfg.max_single_position == 0.25

    def test_max_total_position_from_env(self):
        """从环境变量加载总仓位上限"""
        with patch.dict(os.environ, {"MAX_TOTAL_POSITION": "0.70"}):
            from stock_skill.config import reload_config
            cfg = reload_config()
            assert cfg.max_total_position == 0.70

    def test_vol_multi_from_env(self):
        """从环境变量加载量比倍数"""
        with patch.dict(os.environ, {"VOL_MULTI": "2.0"}):
            from stock_skill.config import reload_config
            cfg = reload_config()
            assert cfg.vol_multi == 2.0

    def test_target_rate_from_env(self):
        """从环境变量加载止盈率"""
        with patch.dict(os.environ, {"TARGET_RATE": "0.08"}):
            from stock_skill.config import reload_config
            cfg = reload_config()
            assert cfg.target_rate == 0.08

    def test_stop_loss_rate_from_env(self):
        """从环境变量加载止损率"""
        with patch.dict(os.environ, {"STOP_LOSS_RATE": "-0.05"}):
            from stock_skill.config import reload_config
            cfg = reload_config()
            assert cfg.stop_loss_rate == -0.05

    def test_hold_days_from_env(self):
        """从环境变量加载持仓天数"""
        with patch.dict(os.environ, {"HOLD_DAYS": "10"}):
            from stock_skill.config import reload_config
            cfg = reload_config()
            assert cfg.hold_days == 10

    def test_invalid_env_int(self):
        """无效整数环境变量 -> 使用默认值"""
        with patch.dict(os.environ, {"HOLD_DAYS": "invalid"}):
            from stock_skill.config import reload_config
            cfg = reload_config()
            assert cfg.hold_days == 5  # _env_int fallback 到字段默认值 5

    def test_invalid_env_float(self):
        """无效浮点数环境变量 -> 使用默认值"""
        with patch.dict(os.environ, {"MAX_SINGLE_POSITION": "invalid"}):
            from stock_skill.config import reload_config
            cfg = reload_config()
            assert cfg.max_single_position == 0.30  # _env_float fallback 到字段默认值 0.30


class TestConfigLongport:
    """长桥配置测试"""

    def test_longport_config_from_env(self):
        """从环境变量加载长桥配置"""
        env = {
            "LONGPORT_APP_KEY": "test_key",
            "LONGPORT_APP_SECRET": "test_secret",
            "LONGPORT_ACCESS_TOKEN": "test_token"
        }
        with patch.dict(os.environ, env):
            from stock_skill.config import reload_config
            cfg = reload_config()
            assert cfg.longport_app_key == "test_key"
            assert cfg.longport_app_secret == "test_secret"
            assert cfg.longport_access_token == "test_token"

    def test_longport_config_default(self):
        """长桥配置默认值"""
        with patch.dict(os.environ, {}, clear=True):
            from stock_skill.config import reload_config
            cfg = reload_config()
            assert cfg.longport_app_key == ""
            assert cfg.longport_app_secret == ""
            assert cfg.longport_access_token == ""


class TestConfigValidate:
    """配置验证测试"""

    def test_validate_missing_tushare(self):
        """缺少 Tushare Token 不再报错（tushare 为可选依赖）"""
        with patch.dict(os.environ, {"TUSHARE_TOKEN": ""}):
            from stock_skill.config import reload_config
            cfg = reload_config()
            issues = cfg.validate()
            assert len(issues) == 0

    def test_validate_valid_config(self):
        """有效配置"""
        env = {
            "TUSHARE_TOKEN": "valid_token",
            "LONGPORT_APP_KEY": "valid_key",
            "LONGPORT_APP_SECRET": "valid_secret",
            "LONGPORT_ACCESS_TOKEN": "valid_token"
        }
        with patch.dict(os.environ, env):
            from stock_skill.config import reload_config
            cfg = reload_config()
            issues = cfg.validate()
            assert len(issues) == 0

    def test_validate_missing_longport(self):
        """缺少长桥配置"""
        env = {
            "TUSHARE_TOKEN": "valid_token",
            "LONGPORT_APP_KEY": "",
            "LONGPORT_APP_SECRET": "",
            "LONGPORT_ACCESS_TOKEN": ""
        }
        with patch.dict(os.environ, env):
            from stock_skill.config import reload_config
            cfg = reload_config()
            issues = cfg.validate_longport()
            assert any("LONGPORT" in i for i in issues)


class TestConfigSingleton:
    """配置单例测试"""

    def test_get_config_singleton(self):
        """get_config 返回单例"""
        from stock_skill.config import get_config, reload_config
        cfg1 = get_config()
        cfg2 = get_config()
        assert cfg1 is cfg2

    def test_reload_config(self):
        """reload_config 创建新实例"""
        from stock_skill.config import get_config, reload_config
        cfg1 = get_config()
        cfg2 = reload_config()
        assert cfg1 is not cfg2


class TestConfigDefaultWatchlist:
    """默认观察列表测试"""

    def test_default_watchlist(self):
        """默认观察列表"""
        with patch.dict(os.environ, {}, clear=True):
            from stock_skill.config import reload_config
            cfg = reload_config()
            assert "600036.SH" in cfg.default_watchlist
            assert "601318.SH" in cfg.default_watchlist

    def test_default_index_codes(self):
        """默认指数代码"""
        with patch.dict(os.environ, {}, clear=True):
            from stock_skill.config import reload_config
            cfg = reload_config()
            assert "000001.SH" in cfg.index_codes
            assert "399001.SZ" in cfg.index_codes


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
