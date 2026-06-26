"""资金面因子 - 北向资金/融资融券/主力资金/机构持仓"""
from __future__ import annotations

import logging
from typing import Dict, Optional

import numpy as np
import pandas as pd
import requests

from .base import Factor, FactorResult, register_factor

logger = logging.getLogger(__name__)

_EASTMONEY_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://data.eastmoney.com/",
}


@register_factor
class MainNetInflowFactor(Factor):
    """主力净流入因子"""
    name = "main_net_inflow"
    category = "capital"
    description = "近5日主力净流入均值（万元）"

    def compute(self, df: pd.DataFrame, **kwargs) -> Optional[float]:
        flows = kwargs.get("money_flow_history")
        if flows and len(flows) >= 3:
            return float(np.mean(flows[-5:]))
        return None


@register_factor
class NorthboundFactor(Factor):
    """北向资金因子"""
    name = "northbound"
    category = "capital"
    description = "北向资金持股比例变化"

    def compute(self, df: pd.DataFrame, **kwargs) -> Optional[float]:
        nb_change = kwargs.get("northbound_change")
        if nb_change is not None:
            return nb_change
        return None


@register_factor
class MarginFactor(Factor):
    """融资融券因子"""
    name = "margin"
    category = "capital"
    description = "融资余额变化率"

    def compute(self, df: pd.DataFrame, **kwargs) -> Optional[float]:
        margin_change = kwargs.get("margin_change")
        if margin_change is not None:
            return margin_change
        return None


@register_factor
class VolumePriceTrendFactor(Factor):
    """量价趋势因子"""
    name = "vpt"
    category = "capital"
    description = "量价趋势指标，量价配合度"

    def compute(self, df: pd.DataFrame, **kwargs) -> Optional[float]:
        if len(df) < 20:
            return None

        close = df["close"].astype(float)
        volume = df["volume"].astype(float)

        # VPT = 前日VPT + 成交量 * (今日收盘-昨日收盘)/昨日收盘
        pct_change = close.pct_change()
        vpt = (volume * pct_change).cumsum()

        # 20日VPT斜率
        vpt_20 = vpt.tail(20)
        if len(vpt_20) < 20:
            return None

        x = np.arange(len(vpt_20))
        slope = np.polyfit(x, vpt_20.values, 1)[0]

        return float(slope) if np.isfinite(slope) else None


@register_factor
class MoneyFlowStrengthFactor(Factor):
    """资金强度因子"""
    name = "mf_strength"
    category = "capital"
    description = "大单净流入 / 总成交额"

    def compute(self, df: pd.DataFrame, **kwargs) -> Optional[float]:
        main_net = kwargs.get("main_net_inflow", 0)
        amount = kwargs.get("amount", 0)
        if amount and amount > 0:
            return main_net / amount
        return None


@register_factor
class InstHoldingFactor(Factor):
    """机构持仓变化因子"""
    name = "inst_holding"
    category = "capital"
    description = "机构持仓比例变化"

    def compute(self, df: pd.DataFrame, **kwargs) -> Optional[float]:
        inst_change = kwargs.get("inst_holding_change")
        if inst_change is not None:
            return inst_change
        return None


class CapitalFactorSet:
    """资金面因子集合"""

    @staticmethod
    def get_factors() -> list:
        return [
            MainNetInflowFactor(), NorthboundFactor(), MarginFactor(),
            VolumePriceTrendFactor(), MoneyFlowStrengthFactor(),
            InstHoldingFactor(),
        ]

    @staticmethod
    def fetch_northbound(codes: list) -> Dict[str, float]:
        """获取北向资金持股变化"""
        result = {}
        try:
            url = "https://push2.eastmoney.com/api/qt/clist/get"
            params = {
                "fid": "f184",
                "po": "1",
                "pz": "500",
                "pn": "1",
                "np": "1",
                "fltt": "2",
                "invt": "2",
                "fs": "b:BK0707+f:!50",
                "fields": "f12,f14,f184",
            }
            resp = requests.get(url, params=params, headers=_EASTMONEY_HEADERS, timeout=10)
            data = resp.json()
            if data.get("data") and data["data"].get("diff"):
                for item in data["data"]["diff"]:
                    code_num = item.get("f12", "")
                    change = item.get("f184", 0)
                    # 匹配代码
                    for c in codes:
                        if c.startswith(code_num):
                            result[c] = float(change) / 100 if change else 0
        except Exception as e:
            logger.warning(f"获取北向资金失败: {e}")
        return result

    @staticmethod
    def fetch_margin(codes: list) -> Dict[str, float]:
        """获取融资融券余额变化

        通过东方财富融资融券接口获取个股融资余额变化率，
        用近5日融资余额变化 / 5日均值作为变化率指标。
        """
        result = {}
        try:
            url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
            params = {
                "sortColumns": "UPDATE_DATE",
                "sortTypes": "-1",
                "pageSize": "500",
                "pageNumber": "1",
                "reportName": "RPTA_WEB_RZRQ_GGMX",
                "columns": "SCODE,UPDATE_DATE,RZYE,RQYE",
                "source": "WEB",
                "client": "WEB",
            }
            resp = requests.get(url, params=params, headers=_EASTMONEY_HEADERS, timeout=15)
            data = resp.json()
            if not data.get("result") or not data["result"].get("data"):
                return result

            margin_data = {}
            for item in data["result"]["data"]:
                code_num = item.get("SCODE", "")
                rzye = item.get("RZYE", 0)
                if code_num and rzye is not None:
                    if code_num not in margin_data:
                        margin_data[code_num] = []
                    margin_data[code_num].append(float(rzye))

            for c in codes:
                code_num = c.split(".")[0]
                if code_num in margin_data and len(margin_data[code_num]) >= 2:
                    vals = margin_data[code_num]
                    latest = vals[0]
                    prev = vals[-1]
                    if prev > 0:
                        result[c] = (latest - prev) / prev
        except Exception as e:
            logger.warning(f"获取融资融券失败: {e}")
        return result
