#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
东方财富股票数据爬虫
"""

import json
import time
from datetime import datetime, timedelta
from typing import Optional, Tuple

import requests
import pandas as pd


def get_security_type(security_code: str) -> str:
    """判断证券代码所属市场类型"""
    code_upper = security_code.upper()
    if security_code.endswith(("SH", "SZ")):
        return code_upper[-2:]
    if not security_code.isdigit() and not code_upper.endswith(("SH", "SZ")):
        return "FUTURES"
    if security_code.startswith(("50", "51", "60", "90", "110", "113", "132", "204")):
        return "SH"
    if security_code.startswith(("00", "13", "18", "15", "16", "20", "30", "39", "115", "1318")):
        return "SZ"
    if security_code.startswith(("5", "6", "9", "7")):
        return "SH"
    return "SZ"


class EastmoneySpider:
    """东方财富股票数据爬虫"""

    def __init__(self):
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        }

    def get_stock_kline(self, security_code: str, period: str = "day", 
                        days: int = 1000) -> pd.DataFrame:
        """
        获取个股的K线数据

        Args:
            security_code: 股票代码 (如 600519)
            period: 周期 day/week/month
            days: 回溯天数

        Returns:
            DataFrame: 包含 date/open/high/low/close/volume 等列
        """
        # 确定市场类型
        security_type = get_security_type(security_code)
        market_type = 1 if security_type == "SH" else 0

        # 计算开始日期
        cur_date = datetime.now()
        if period == "day":
            begin_date = cur_date + timedelta(days=-days)
        elif period == "week":
            begin_date = cur_date + timedelta(days=-days * 7)
        elif period == "month":
            begin_date = cur_date + timedelta(days=-days * 30)
        else:
            raise ValueError(f"不支持周期: {period}")

        beg = begin_date.strftime('%Y%m%d')
        
        # K线类型: 101=日, 102=周, 103=月
        klt = {"day": 101, "week": 102, "month": 103}[period]

        url = (f"https://push2his.eastmoney.com/api/qt/stock/kline/get"
               f"?fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13"
               f"&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61"
               f"&beg={beg}&end=20500101"
               f"&ut=fa5fd1943c7b386f172d6893dbfba10b&rtntype=6"
               f"&secid={market_type}.{security_code}&klt={klt}&fqt=1")

        resp = requests.get(url, headers=self.headers, timeout=10)
        resp.encoding = 'utf8'
        data = resp.json().get('data', {})
        
        if not data:
            return pd.DataFrame()
            
        name = data.get('name', security_code)
        klines = data.get('klines', [])
        
        records = []
        for kline in klines:
            # 日期,开盘,收盘,最高,最低,成交量,成交额,振幅,涨跌幅,涨跌额,换手率
            parts = kline.split(',')
            if len(parts) >= 7:
                records.append({
                    'date': parts[0],
                    'open': float(parts[1]) if parts[1] else 0,
                    'close': float(parts[2]) if parts[2] else 0,
                    'high': float(parts[3]) if parts[3] else 0,
                    'low': float(parts[4]) if parts[4] else 0,
                    'volume': float(parts[6]) if parts[6] else 0,
                    'amount': float(parts[7]) if len(parts) > 7 and parts[7] else 0,
                    'pct_chg': float(parts[9]) if len(parts) > 9 and parts[9] else 0,
                })

        df = pd.DataFrame(records)
        df['code'] = security_code
        df['name'] = name
        return df

    def fetch_capital_flow_rank(self, days: int = 0, limit: int = 100) -> Tuple[datetime, pd.DataFrame]:
        """
        获取资金流向排名

        Args:
            days: 统计天数 (0=今日, 3=3日, 5=5日, 10=10日)
            limit: 返回数量

        Returns:
            (统计日期, DataFrame)
        """
        fid_map = {0: 'f62', 3: 'f267', 5: 'f164', 10: 'f174'}
        if days not in fid_map:
            raise ValueError("days必须是 0, 3, 5, 10 之一")
        
        fid = fid_map[days]
        
        url = (f"https://push2.eastmoney.com/api/qt/clist/get"
               f"?fid={fid}&po=1&pz={limit}&pn=1&np=1&fltt=2&invt=2"
               f"&ut=b2884a393a59ad64002292a3e90d46a5"
               f"&fs=m%3A0%2Bt%3A6%2Cf%3A!2,m%3A0%2Bt%3A13%2Cf%3A!2,m%3A0%2Bt%3A80%2Cf%3A!2,"
               f"m%3A1%2Bt%3A2%2Cf%3A!2,m%3A1%2Bt%3A23%2Cf%3A!2,m%3A0%2Bt%3A7%2Cf%3A!2,m%3A1%2Bt%3A3%2Cf%3A!2"
               f"&fields=f12,f14,f2,f3,f62,f184,f225,f165,f175")

        self.headers['Host'] = "push2.eastmoney.com"
        resp = requests.get(url, headers=self.headers, timeout=10)
        resp.encoding = 'utf8'
        
        diff = resp.json().get('data', {}).get('diff', [])
        if not diff:
            return datetime.now(), pd.DataFrame()
        
        cur_date = datetime.fromtimestamp(diff[0].get('f124', 0))
        
        records = []
        for item in diff:
            records.append({
                'code': item.get('f12', ''),
                'name': item.get('f14', ''),
                'price': item.get('f2', 0),
                'pct_chg': item.get('f3', 0),
                'net_inflow': item.get('f62', 0),
                'net_ratio': item.get('f184', 0),
                'five_day_net': item.get('f165', 0),
                'ten_day_net': item.get('f175', 0),
            })
        
        df = pd.DataFrame(records)
        return cur_date, df


if __name__ == "__main__":
    # 测试
    spider = EastmoneySpider()
    
    # 测试获取K线
    print("=== 测试K线数据 ===")
    df = spider.get_stock_kline("600519", days=30)
    print(df.tail())
    
    # 测试资金流向
    print("\n=== 测试资金流向 ===")
    date, df = spider.fetch_capital_flow_rank(days=5)
    print(f"统计日期: {date}")
    print(df.head(10))