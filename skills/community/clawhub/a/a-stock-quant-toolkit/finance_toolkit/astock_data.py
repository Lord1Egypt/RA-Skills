"""
A股数据获取模块 - 基于akshare
支持沪深全市场数据，含缓存机制
"""

import akshare as ak
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import json
import logging

logger = logging.getLogger(__name__)

class AStockDataFetcher:
    """A股数据获取器"""

    def __init__(self, cache_dir="data/cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def get_real_time_quote(self, symbol="sh600519"):
        """获取实时行情"""
        try:
            df = ak.stock_zh_a_spot_em()
            if symbol:
                df = df[df['代码'] == symbol.replace('sh','').replace('sz','')]
            return df
        except Exception as e:
            logger.error(f"获取实时行情失败: {e}")
            return None

    def get_history(self, symbol="600519", start_date=None, end_date=None, period="daily"):
        """获取历史K线数据"""
        try:
            if start_date is None:
                start_date = (datetime.now() - timedelta(days=365)).strftime("%Y%m%d")
            if end_date is None:
                end_date = datetime.now().strftime("%Y%m%d")

            df = ak.stock_zh_a_hist(
                symbol=symbol,
                period=period,
                start_date=start_date,
                end_date=end_date,
                adjust="qfq"  # 前复权
            )
            if df is not None and not df.empty:
                df['代码'] = symbol
            return df
        except Exception as e:
            logger.error(f"获取{symbol}历史数据失败: {e}")
            return None

    def get_index_data(self, symbol="sh000001", start_date=None, end_date=None):
        """获取指数数据"""
        try:
            if start_date is None:
                start_date = (datetime.now() - timedelta(days=365)).strftime("%Y%m%d")
            if end_date is None:
                end_date = datetime.now().strftime("%Y%m%d")

            df = ak.stock_zh_index_daily(symbol=symbol)
            df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
            return df
        except Exception as e:
            logger.error(f"获取指数数据失败: {e}")
            return None

    def get_stock_list(self):
        """获取A股全部股票列表"""
        try:
            df = ak.stock_zh_a_spot_em()
            return df[['代码','名称','最新价','涨跌幅','成交量','成交额','换手率','市盈率-动态','总市值']]
        except Exception as e:
            logger.error(f"获取股票列表失败: {e}")
            return None

    def get_hot_stocks(self, top_n=50):
        """获取热门股票（按成交额排序）"""
        df = self.get_stock_list()
        if df is not None:
            df = df.sort_values('成交额', ascending=False).head(top_n)
        return df

    def get_concept_board(self, board_name=None):
        """获取概念板块"""
        try:
            df = ak.stock_board_concept_name_em()
            if board_name:
                df = df[df['板块名称'].str.contains(board_name)]
            return df
        except Exception as e:
            logger.error(f"获取概念板块失败: {e}")
            return None

if __name__ == "__main__":
    fetcher = AStockDataFetcher()
    print("=== A股数据获取模块测试 ===")

    # 测试实时行情
    hot = fetcher.get_hot_stocks(5)
    if hot is not None:
        print(f"\n📊 热门股票 Top5:")
        print(hot[['代码','名称','最新价','涨跌幅','成交额','换手率']].to_string(index=False))

    # 测试历史数据
    df = fetcher.get_history("600519", start_date="20260101")
    if df is not None:
        print(f"\n📈 贵州茅台历史数据 (最近3行):")
        print(df.tail(3)[['日期','开盘','收盘','最高','最低','成交量','换手率']].to_string(index=False))

    # 测试概念板块
    board = fetcher.get_concept_board()
    if board is not None:
        print(f"\n🏷️ 概念板块总数: {len(board)}")
        print(f"    涨幅前5: {board.sort_values('涨跌幅',ascending=False).head(5)['板块名称'].tolist()}")
