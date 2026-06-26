#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
云梦A股数据获取工具 - Skill
功能：
1. 获取个股资金流向
2. 查询个股新闻
3. 获取个股筹码分布
4. 获取当天龙虎榜
5. 获取当日涨停板行情
6. 获取昨日涨停板股池
7. 获取盘口异动
8. 获取板块异动
9. 获取单只股票详细信息

Skill 格式支持
"""

import pandas as pd
import datetime
import os
import time
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional, Any



# 今日日期
TODAY = datetime.datetime.now().strftime('%Y%m%d')
TODAY_STR = datetime.datetime.now().strftime('%Y-%m-%d')

# 请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://www.eastmoney.com'
}


class AShareDataSkill:
    """
    云梦A股数据获取 Skill
    用于框架集成
    """
    
    name = "clouddream_a_data"
    description = "获取A股市场各类数据，包括行情、资金流向、龙虎榜等"
    
    @staticmethod
    def retry_request(url, max_retries=3, timeout=10):
        """
        带重试机制的请求
        
        Args:
            url: 请求URL
            max_retries: 最大重试次数
            timeout: 超时时间
            
        Returns:
            response: 响应对象
        """
        for i in range(max_retries):
            try:
                response = requests.get(url, headers=HEADERS, timeout=timeout)
                response.raise_for_status()
                return response
            except Exception as e:
                if i < max_retries - 1:
                    print(f"请求失败，{i+1}秒后重试: {str(e)}")
                    time.sleep(i+1)
                    continue
                raise e
    
    """
    获取个股资金流向
    获取指定股票的资金流向数据，包括主力资金、散户资金等详细资金流动情况
    
    Args:
        symbol: 股票代码，如 "000001"
        
    Returns:
        DataFrame: 资金流向数据，包含日期、主力净流入、超大单净流入、大单净流入、中单净流入、小单净流入等字段
    """
    @staticmethod
    def get_stock_fund_flow(symbol: str) -> Optional[pd.DataFrame]:
        try:
            # 使用东方财富API获取资金流向
            url = f'https://push2.eastmoney.com/api/qt/stock/get?secid=0.{symbol}&fields=f62,f63,f64,f65,f66,f67,f68,f69,f70,f71'
            response = AShareDataSkill.retry_request(url)
            data = response.json()
            
            # 解析数据
            if data.get('data'):
                stock_data = data['data']
                # 构造资金流向数据
                fund_data = {
                    '日期': [TODAY_STR],
                    '主力净流入-净额': [stock_data.get('f62', 0)],
                    '主力净流入-净占比': [stock_data.get('f63', 0)],
                    '超大单净流入-净额': [stock_data.get('f64', 0)],
                    '超大单净流入-净占比': [stock_data.get('f65', 0)],
                    '大单净流入-净额': [stock_data.get('f66', 0)],
                    '大单净流入-净占比': [stock_data.get('f67', 0)],
                    '中单净流入-净额': [stock_data.get('f68', 0)],
                    '中单净流入-净占比': [stock_data.get('f69', 0)],
                    '小单净流入-净额': [stock_data.get('f70', 0)],
                    '小单净流入-净占比': [stock_data.get('f71', 0)]
                }
                return pd.DataFrame(fund_data)
            return None
        except Exception as e:
            print(f"获取个股资金流向失败: {str(e)}")
            return None
    
    """
    查询个股新闻
    获取指定股票的最新新闻信息，包括新闻标题和链接
    
    Args:
        symbol: 股票代码，如 "000001"
        
    Returns:
        DataFrame: 个股新闻数据，包含标题、链接、日期等字段
    """
    @staticmethod
    def get_stock_news(symbol: str) -> Optional[pd.DataFrame]:
        try:
            # 使用新浪财经API获取新闻
            url = f'https://finance.sina.com.cn/realstock/company/{symbol}/nc.shtml'
            response = AShareDataSkill.retry_request(url)
            # 解析HTML获取新闻
            soup = BeautifulSoup(response.text, 'html.parser')
            news_list = []
            
            # 查找新闻元素
            for item in soup.select('.newsList li'):
                a = item.select_one('a')
                if a:
                    title = a.text.strip()
                    href = a.get('href')
                    news_list.append({'标题': title, '链接': href})
            
            if news_list:
                df = pd.DataFrame(news_list)
                df['日期'] = TODAY_STR
                return df
            return None
        except Exception as e:
            print(f"获取个股新闻失败: {str(e)}")
            return None
    
    """
    获取个股筹码分布
    获取指定股票的筹码分布数据，包括获利比例、平均成本、成本区间等信息
    
    Args:
        symbol: 股票代码，如 "000001"
        
    Returns:
        DataFrame: 筹码分布数据，包含日期、获利比例、平均成本、90成本区间、70成本区间等字段
    """
    @staticmethod
    def get_stock_chip_distribution(symbol: str) -> Optional[pd.DataFrame]:
        try:
            # 使用东方财富API获取筹码分布
            url = f'https://push2.eastmoney.com/api/qt/stock/get?secid=0.{symbol}&fields=f187,f188,f189,f190,f191,f192,f193,f194,f195'
            response = AShareDataSkill.retry_request(url)
            data = response.json()
            
            if data.get('data'):
                stock_data = data['data']
                chip_data = {
                    '日期': [TODAY_STR],
                    '获利比例': [stock_data.get('f187', 0)],
                    '平均成本': [stock_data.get('f188', 0)],
                    '90成本-低': [stock_data.get('f189', 0)],
                    '90成本-高': [stock_data.get('f190', 0)],
                    '90集中度': [stock_data.get('f191', 0)],
                    '70成本-低': [stock_data.get('f192', 0)],
                    '70成本-高': [stock_data.get('f193', 0)],
                    '70集中度': [stock_data.get('f194', 0)]
                }
                return pd.DataFrame(chip_data)
            return None
        except Exception as e:
            print(f"获取个股筹码分布失败: {str(e)}")
            return None
    
    """
    获取当天龙虎榜
    获取当日龙虎榜数据，包括买卖席位、交易金额等信息
    
    Returns:
        DataFrame: 龙虎榜数据，包含股票代码、股票名称、交易金额等字段
    """
    @staticmethod
    def get_dragon_tiger_list() -> Optional[pd.DataFrame]:
        try:
            # 使用新浪财经API获取龙虎榜
            url = f'https://vip.stock.finance.sina.com.cn/q/go.php/vLHBData/kind/jgld/type/sh/days/1'
            response = AShareDataSkill.retry_request(url)
            data = response.json()
            
            if data.get('data'):
                df = pd.DataFrame(data['data'])
                return df
            return None
        except Exception as e:
            print(f"获取龙虎榜数据失败: {str(e)}")
            return None
    
    """
    获取当日涨停板行情
    获取当日涨停板股票数据，包括股票代码、名称、涨跌幅等信息
    
    Returns:
        DataFrame: 涨停板数据，包含股票代码、股票名称、最新价、涨跌幅、成交量、成交额等字段
    """
    @staticmethod
    def get_limit_up_stocks() -> Optional[pd.DataFrame]:
        try:
            # 使用东方财富API获取涨停板
            url = f'https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=50&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048&fields=f12,f14,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152'
            response = AShareDataSkill.retry_request(url)
            data = response.json()
            
            if data.get('data', {}).get('diff'):
                df = pd.DataFrame(data['data']['diff'])
                # 重命名列
                df = df.rename(columns={
                    'f12': '股票代码',
                    'f14': '股票名称',
                    'f2': '最新价',
                    'f3': '涨跌幅',
                    'f4': '涨跌额',
                    'f5': '成交量',
                    'f6': '成交额',
                    'f15': '最高',
                    'f16': '最低',
                    'f17': '开盘',
                    'f18': '昨收'
                })
                return df
            return None
        except Exception as e:
            print(f"获取涨停板数据失败: {str(e)}")
            return None
    
    """
    获取昨日涨停板股池
    获取昨日涨停板股票数据，包括股票代码、名称、涨跌幅等信息
    
    Returns:
        DataFrame: 昨日涨停板数据，包含股票代码、股票名称、最新价、涨跌幅、成交量、成交额等字段
    """
    @staticmethod
    def get_yesterday_limit_up_stocks() -> Optional[pd.DataFrame]:
        try:
            # 计算昨日日期
            yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y%m%d')
            # 使用东方财富API获取昨日涨停板
            url = f'https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=50&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048&fields=f12,f14,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152'
            response = AShareDataSkill.retry_request(url)
            data = response.json()
            
            if data.get('data', {}).get('diff'):
                df = pd.DataFrame(data['data']['diff'])
                # 重命名列
                df = df.rename(columns={
                    'f12': '股票代码',
                    'f14': '股票名称',
                    'f2': '最新价',
                    'f3': '涨跌幅',
                    'f4': '涨跌额',
                    'f5': '成交量',
                    'f6': '成交额',
                    'f15': '最高',
                    'f16': '最低',
                    'f17': '开盘',
                    'f18': '昨收'
                })
                return df
            return None
        except Exception as e:
            print(f"获取昨日涨停板数据失败: {str(e)}")
            return None
    
    """
    获取盘口异动
    获取盘口异动数据，包括异常波动的股票信息
    
    Returns:
        DataFrame: 盘口异动数据，包含股票代码、股票名称、最新价、涨跌幅、成交量、成交额等字段
    """
    @staticmethod
    def get_market_anomalies() -> Optional[pd.DataFrame]:
        try:
            # 使用东方财富API获取盘口异动
            url = f'https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=50&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048&fields=f12,f14,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152'
            response = AShareDataSkill.retry_request(url)
            data = response.json()
            
            if data.get('data', {}).get('diff'):
                df = pd.DataFrame(data['data']['diff'])
                # 重命名列
                df = df.rename(columns={
                    'f12': '股票代码',
                    'f14': '股票名称',
                    'f2': '最新价',
                    'f3': '涨跌幅',
                    'f4': '涨跌额',
                    'f5': '成交量',
                    'f6': '成交额',
                    'f15': '最高',
                    'f16': '最低',
                    'f17': '开盘',
                    'f18': '昨收'
                })
                return df
            return None
        except Exception as e:
            print(f"获取盘口异动数据失败: {str(e)}")
            return None
    
    """
    获取板块异动
    获取板块异动数据，包括涨幅居前的板块信息
    
    Returns:
        DataFrame: 板块异动数据，包含板块代码、板块名称、最新价、涨跌幅、成交量、成交额等字段
    """
    @staticmethod
    def get_sector_anomalies() -> Optional[pd.DataFrame]:
        try:
            # 使用东方财富API获取板块异动
            url = f'https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=50&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=b:MK001,b:MK002,b:MK003,b:MK004,b:MK005,b:MK006,b:MK007,b:MK008,b:MK009,b:MK010&fields=f12,f14,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152'
            response = AShareDataSkill.retry_request(url)
            data = response.json()
            
            if data.get('data', {}).get('diff'):
                df = pd.DataFrame(data['data']['diff'])
                # 重命名列
                df = df.rename(columns={
                    'f12': '板块代码',
                    'f14': '板块名称',
                    'f2': '最新价',
                    'f3': '涨跌幅',
                    'f4': '涨跌额',
                    'f5': '成交量',
                    'f6': '成交额',
                    'f15': '最高',
                    'f16': '最低',
                    'f17': '开盘',
                    'f18': '昨收'
                })
                return df
            return None
        except Exception as e:
            print(f"获取板块异动数据失败: {str(e)}")
            return None
    
    """
    直接返回数据（不再保存到CSV文件）
    
    Args:
        df: DataFrame数据
        filename: 文件名（仅作参考）
        
    Returns:
        DataFrame: 原始数据
    """
    @staticmethod
    def save_to_csv(df: pd.DataFrame, filename: str) -> pd.DataFrame:
        return df
    
    """
    获取单只股票详细信息
    获取股票的详细信息，包括基本信息、换手率、成交量、盘口情况、均线情况和上升通道判断
    
    Args:
        symbol: 股票代码，如 "000001"
        
    Returns:
        dict: 包含股票详细信息的字典，包括股票代码、名称、最新价、涨跌幅、成交量、换手率、盘口数据、均线情况和上升通道判断
    """
    @staticmethod
    def get_stock_details(symbol: str) -> Optional[dict]:
        try:
            details = {}
            
            # 1. 获取基本信息
            url = f'https://push2.eastmoney.com/api/qt/stock/get?secid=0.{symbol}&fields=f12,f14,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f62,f128,f136,f115,f152,f187,f188,f189,f190,f191,f192,f193,f194'
            response = AShareDataSkill.retry_request(url)
            data = response.json()
            
            if data.get('data'):
                stock_data = data['data']
                details['股票代码'] = stock_data.get('f12')
                details['股票名称'] = stock_data.get('f14')
                details['最新价'] = stock_data.get('f2')
                details['涨跌幅'] = stock_data.get('f3')
                details['涨跌额'] = stock_data.get('f4')
                details['成交量'] = stock_data.get('f5')
                details['成交额'] = stock_data.get('f6')
                details['换手率'] = stock_data.get('f8')
                details['最高'] = stock_data.get('f15')
                details['最低'] = stock_data.get('f16')
                details['开盘'] = stock_data.get('f17')
                details['昨收'] = stock_data.get('f18')
            
            # 2. 获取盘口数据
            url = f'https://push2.eastmoney.com/api/qt/stock/get?secid=0.{symbol}&fields=f19,f20,f21,f22,f23,f24,f25,f26,f27,f28,f29,f30,f31,f32,f33,f34,f35,f36,f37,f38,f39,f40,f41,f42,f43,f44,f45,f46,f47,f48,f49,f50,f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61'
            response = AShareDataSkill.retry_request(url)
            data = response.json()
            
            if data.get('data'):
                stock_data = data['data']
                details['盘口数据'] = {
                    '买一价': stock_data.get('f19'),
                    '买一量': stock_data.get('f20'),
                    '买二价': stock_data.get('f21'),
                    '买二量': stock_data.get('f22'),
                    '买三价': stock_data.get('f23'),
                    '买三量': stock_data.get('f24'),
                    '买四价': stock_data.get('f25'),
                    '买四量': stock_data.get('f26'),
                    '买五价': stock_data.get('f27'),
                    '买五量': stock_data.get('f28'),
                    '卖一价': stock_data.get('f29'),
                    '卖一量': stock_data.get('f30'),
                    '卖二价': stock_data.get('f31'),
                    '卖二量': stock_data.get('f32'),
                    '卖三价': stock_data.get('f33'),
                    '卖三量': stock_data.get('f34'),
                    '卖四价': stock_data.get('f35'),
                    '卖四量': stock_data.get('f36'),
                    '卖五价': stock_data.get('f37'),
                    '卖五量': stock_data.get('f38')
                }
            
            # 3. 获取K线数据（用于计算均线）
            url = f'https://push2his.eastmoney.com/api/qt/stock/kline/get?secid=0.{symbol}&klt=101&fqt=1&end={TODAY}&lmt=60'
            response = AShareDataSkill.retry_request(url)
            data = response.json()
            
            if data.get('data', {}).get('klines'):
                klines = data['data']['klines']
                close_prices = []
                for kline in klines:
                    parts = kline.split(',')
                    if len(parts) >= 5:
                        close_prices.append(float(parts[2]))
                
                # 计算均线
                if len(close_prices) >= 30:
                    ma5 = sum(close_prices[-5:]) / 5
                    ma10 = sum(close_prices[-10:]) / 10
                    ma20 = sum(close_prices[-20:]) / 20
                    ma30 = sum(close_prices[-30:]) / 30
                    
                    details['均线情况'] = {
                        'MA5': ma5,
                        'MA10': ma10,
                        'MA20': ma20,
                        'MA30': ma30
                    }
                    
                    # 判断是否上升通道
                    details['是否上升通道'] = (ma5 > ma10 > ma20 > ma30)
            
            return details
        except Exception as e:
            print(f"获取个股详细信息失败: {str(e)}")
            return None
    
    """
    运行所有数据获取方法
    一次性获取所有类型的A股市场数据，包括龙虎榜、涨停板、盘口异动和板块异动
    
    Returns:
        Dict[str, Any]: 包含所有数据的字典，键为数据类型，值为对应的数据
    """
    @classmethod
    def run_all(cls) -> Dict[str, Any]:
        results = {}
        
        print("=== A股数据获取工具 ===")
        print(f"日期: {TODAY_STR}")
        print()
        
        # 2. 获取当天龙虎榜
        print("2. 获取当天龙虎榜...")
        try:
            df = cls.get_dragon_tiger_list()
            if df is not None:
                results['dragon_tiger'] = df
                print("✓ 成功获取龙虎榜数据")
        except Exception as e:
            print(f"✗ 失败: {str(e)}")
        
        time.sleep(1)  # 避免请求过快
        
        # 3. 获取当日涨停板行情
        print("3. 获取当日涨停板行情...")
        try:
            df = cls.get_limit_up_stocks()
            if df is not None:
                results['limit_up'] = df
                print("✓ 成功获取涨停板数据")
        except Exception as e:
            print(f"✗ 失败: {str(e)}")
        
        time.sleep(1)  # 避免请求过快
        
        # 4. 获取昨日涨停板股池
        print("4. 获取昨日涨停板股池...")
        try:
            df = cls.get_yesterday_limit_up_stocks()
            if df is not None:
                results['yesterday_limit_up'] = df
                print("✓ 成功获取昨日涨停板数据")
        except Exception as e:
            print(f"✗ 失败: {str(e)}")
        
        time.sleep(1)  # 避免请求过快
        
        # 5. 获取盘口异动
        print("5. 获取盘口异动...")
        try:
            df = cls.get_market_anomalies()
            if df is not None:
                results['market_anomalies'] = df
                print("✓ 成功获取盘口异动数据")
        except Exception as e:
            print(f"✗ 失败: {str(e)}")
        
        time.sleep(1)  # 避免请求过快
        
        # 6. 获取板块异动
        print("6. 获取板块异动...")
        try:
            df = cls.get_sector_anomalies()
            if df is not None:
                results['sector_anomalies'] = df
                print("✓ 成功获取板块异动数据")
        except Exception as e:
            print(f"✗ 失败: {str(e)}")
        
        print()
        print("=== 数据获取完成 ===")
        
        return results


# Skill 接口函数
def get_stock_fund_flow(symbol: str) -> dict:
    """
    获取个股资金流向
    
    Args:
        symbol: 股票代码，如 "000001"
        
    Returns:
        dict: 资金流向数据
    """
    try:
        result = AShareDataSkill.get_stock_fund_flow(symbol)
        if result is not None:
            return {
                "success": True,
                "data": result.to_dict('records') if hasattr(result, 'to_dict') else result
            }
        return {"success": False, "message": "获取数据失败"}
    except Exception as e:
        return {"success": False, "message": str(e)}

def get_stock_news(symbol: str) -> dict:
    """
    查询个股新闻
    
    Args:
        symbol: 股票代码，如 "000001"
        
    Returns:
        dict: 个股新闻数据
    """
    try:
        result = AShareDataSkill.get_stock_news(symbol)
        if result is not None:
            return {
                "success": True,
                "data": result.to_dict('records') if hasattr(result, 'to_dict') else result
            }
        return {"success": False, "message": "获取数据失败"}
    except Exception as e:
        return {"success": False, "message": str(e)}

def get_stock_chip_distribution(symbol: str) -> dict:
    """
    获取个股筹码分布
    
    Args:
        symbol: 股票代码，如 "000001"
        
    Returns:
        dict: 筹码分布数据
    """
    try:
        result = AShareDataSkill.get_stock_chip_distribution(symbol)
        if result is not None:
            return {
                "success": True,
                "data": result.to_dict('records') if hasattr(result, 'to_dict') else result
            }
        return {"success": False, "message": "获取数据失败"}
    except Exception as e:
        return {"success": False, "message": str(e)}

def get_dragon_tiger_list() -> dict:
    """
    获取当天龙虎榜
    
    Returns:
        dict: 龙虎榜数据
    """
    try:
        result = AShareDataSkill.get_dragon_tiger_list()
        if result is not None:
            return {
                "success": True,
                "data": result.to_dict('records') if hasattr(result, 'to_dict') else result
            }
        return {"success": False, "message": "获取数据失败"}
    except Exception as e:
        return {"success": False, "message": str(e)}

def get_limit_up_stocks() -> dict:
    """
    获取当日涨停板行情
    
    Returns:
        dict: 涨停板数据
    """
    try:
        result = AShareDataSkill.get_limit_up_stocks()
        if result is not None:
            return {
                "success": True,
                "data": result.to_dict('records') if hasattr(result, 'to_dict') else result
            }
        return {"success": False, "message": "获取数据失败"}
    except Exception as e:
        return {"success": False, "message": str(e)}

def get_yesterday_limit_up_stocks() -> dict:
    """
    获取昨日涨停板股池
    
    Returns:
        dict: 昨日涨停板数据
    """
    try:
        result = AShareDataSkill.get_yesterday_limit_up_stocks()
        if result is not None:
            return {
                "success": True,
                "data": result.to_dict('records') if hasattr(result, 'to_dict') else result
            }
        return {"success": False, "message": "获取数据失败"}
    except Exception as e:
        return {"success": False, "message": str(e)}

def get_market_anomalies() -> dict:
    """
    获取盘口异动
    
    Returns:
        dict: 盘口异动数据
    """
    try:
        result = AShareDataSkill.get_market_anomalies()
        if result is not None:
            return {
                "success": True,
                "data": result.to_dict('records') if hasattr(result, 'to_dict') else result
            }
        return {"success": False, "message": "获取数据失败"}
    except Exception as e:
        return {"success": False, "message": str(e)}

def get_sector_anomalies() -> dict:
    """
    获取板块异动
    
    Returns:
        dict: 板块异动数据
    """
    try:
        result = AShareDataSkill.get_sector_anomalies()
        if result is not None:
            return {
                "success": True,
                "data": result.to_dict('records') if hasattr(result, 'to_dict') else result
            }
        return {"success": False, "message": "获取数据失败"}
    except Exception as e:
        return {"success": False, "message": str(e)}

def get_stock_details(symbol: str) -> dict:
    """
    获取单只股票详细信息
    
    Args:
        symbol: 股票代码，如 "000001"
        
    Returns:
        dict: 股票详细信息
    """
    try:
        result = AShareDataSkill.get_stock_details(symbol)
        if result is not None:
            return {"success": True, "data": result}
        return {"success": False, "message": "获取数据失败"}
    except Exception as e:
        return {"success": False, "message": str(e)}

def run_all() -> dict:
    """
    运行所有数据获取方法
    
    Returns:
        dict: 包含所有数据的字典
    """
    try:
        result = AShareDataSkill.run_all()
        # 转换所有DataFrame为字典格式
        formatted_result = {}
        for key, value in result.items():
            if hasattr(value, 'to_dict'):
                formatted_result[key] = value.to_dict('records')
            else:
                formatted_result[key] = value
        return {"success": True, "data": formatted_result}
    except Exception as e:
        return {"success": False, "message": str(e)}


