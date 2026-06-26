"""基本面因子 - PE/PB/ROE/EV/股息率/营收增长"""
from __future__ import annotations

import logging
from typing import Dict, Optional

import numpy as np
import pandas as pd

from .base import Factor, FactorResult, register_factor

logger = logging.getLogger(__name__)


@register_factor
class PEFactor(Factor):
    """市盈率因子（低估值策略）"""
    name = "pe_ttm"
    category = "fundamental"
    description = "市盈率TTM，越低越好"

    def compute(self, df: pd.DataFrame, **kwargs) -> Optional[float]:
        pe = kwargs.get("pe_ttm")
        if pe is not None and pe > 0:
            return 1.0 / pe  # 取倒数，越大越好
        return None


@register_factor
class PBFactor(Factor):
    """市净率因子"""
    name = "pb"
    category = "fundamental"
    description = "市净率，越低越好"

    def compute(self, df: pd.DataFrame, **kwargs) -> Optional[float]:
        pb = kwargs.get("pb")
        if pb is not None and pb > 0:
            return 1.0 / pb
        return None


@register_factor
class ROEFactor(Factor):
    """净资产收益率因子"""
    name = "roe"
    category = "fundamental"
    description = "ROE，越高越好"

    def compute(self, df: pd.DataFrame, **kwargs) -> Optional[float]:
        roe = kwargs.get("roe")
        if roe is not None:
            return roe
        return None


@register_factor
class DividendYieldFactor(Factor):
    """股息率因子"""
    name = "dividend_yield"
    category = "fundamental"
    description = "股息率，越高越好"

    def compute(self, df: pd.DataFrame, **kwargs) -> Optional[float]:
        dv = kwargs.get("dv_ratio")
        if dv is not None:
            return dv
        return None


@register_factor
class RevenueGrowthFactor(Factor):
    """营收增长因子"""
    name = "revenue_growth"
    category = "fundamental"
    description = "营收同比增长率"

    def compute(self, df: pd.DataFrame, **kwargs) -> Optional[float]:
        growth = kwargs.get("revenue_growth")
        if growth is not None:
            return growth
        return None


@register_factor
class ProfitGrowthFactor(Factor):
    """净利润增长因子"""
    name = "profit_growth"
    category = "fundamental"
    description = "净利润同比增长率"

    def compute(self, df: pd.DataFrame, **kwargs) -> Optional[float]:
        growth = kwargs.get("profit_growth")
        if growth is not None:
            return growth
        return None


@register_factor
class EPTTMomentum(Factor):
    """EPS 动量因子"""
    name = "eps_momentum"
    category = "fundamental"
    description = "近4季度 EPS 变化趋势"

    def compute(self, df: pd.DataFrame, **kwargs) -> Optional[float]:
        eps_list = kwargs.get("eps_history")
        if eps_list and len(eps_list) >= 2:
            return (eps_list[-1] - eps_list[0]) / abs(eps_list[0]) if eps_list[0] != 0 else 0
        return None


class FundamentalFactorSet:
    """基本面因子集合"""

    @staticmethod
    def get_factors() -> list:
        return [
            PEFactor(), PBFactor(), ROEFactor(),
            DividendYieldFactor(), RevenueGrowthFactor(),
            ProfitGrowthFactor(), EPTTMomentum(),
        ]

    @staticmethod
    def compute_from_tushare(
        pro_client,
        trade_date: str,
        codes: list,
    ) -> Dict[str, Dict[str, float]]:
        """从 Tushare 获取基本面数据并计算因子

        Returns:
            {code: {factor_name: value}}
        """
        result = {}

        try:
            # 获取每日指标
            df_basic = pro_client.daily_basic(
                trade_date=trade_date,
                fields="ts_code,pe_ttm,pb,dv_ratio,total_mv"
            )
            if df_basic is None or df_basic.empty:
                return {}

            # 获取财务指标
            df_fina = pro_client.fina_indicator(
                fields="ts_code,roe_dt,or_yoy,netprofit_yoy_eps"
            )

            for code in codes:
                factors = {}

                basic_row = df_basic[df_basic["ts_code"] == code]
                if not basic_row.empty:
                    row = basic_row.iloc[0]
                    factors["pe_ttm"] = float(row.get("pe_ttm", 0)) if pd.notna(row.get("pe_ttm")) else None
                    factors["pb"] = float(row.get("pb", 0)) if pd.notna(row.get("pb")) else None
                    factors["dv_ratio"] = float(row.get("dv_ratio", 0)) if pd.notna(row.get("dv_ratio")) else None

                if df_fina is not None and not df_fina.empty:
                    fina_row = df_fina[df_fina["ts_code"] == code]
                    if not fina_row.empty:
                        row = fina_row.iloc[0]
                        factors["roe"] = float(row.get("roe_dt", 0)) if pd.notna(row.get("roe_dt")) else None
                        factors["revenue_growth"] = float(row.get("or_yoy", 0)) if pd.notna(row.get("or_yoy")) else None
                        factors["profit_growth"] = float(row.get("netprofit_yoy_eps", 0)) if pd.notna(row.get("netprofit_yoy_eps")) else None

                result[code] = factors

        except Exception as e:
            logger.warning(f"获取基本面数据失败: {e}")

        return result
