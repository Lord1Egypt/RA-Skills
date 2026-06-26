#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
可转债打新日历模块
获取可申购转债列表
"""

import requests
from datetime import datetime, timedelta
import json

# 模拟数据（实际应调用 API）
# 数据来源：东方财富可转债频道
MOCK_SUBSCRIBABLE = [
    {
        "code": "123205",
        "name": "赛龙转债",
        "amount": 7.5,
        "rating": "AA-",
        "max_subscribe": 100,
        "stock_name": "赛龙科技",
        "stock_code": "300123",
        "industry": "汽车零部件",
        "subscribe_date": "2026-03-07",
    },
    {
        "code": "123206",
        "name": "恒泰转债",
        "amount": 10.0,
        "rating": "AA",
        "max_subscribe": 100,
        "stock_name": "恒泰股份",
        "stock_code": "600456",
        "industry": "化工",
        "subscribe_date": "2026-03-07",
    },
]

MOCK_CALENDAR = [
    {
        "code": "123207",
        "name": "明阳转债",
        "subscribe_date": "2026-03-10",
        "amount": 15.0,
        "rating": "AA+",
    },
    {
        "code": "123208",
        "name": "智科转债",
        "subscribe_date": "2026-03-12",
        "amount": 6.0,
        "rating": "A+",
    },
]


def get_subscribable_cbs(date=None):
    """
    获取指定日期可申购转债
    
    Args:
        date: 日期字符串 YYYY-MM-DD，默认今天
        
    Returns:
        list: 可申购转债列表
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    # TODO: 实际应调用东方财富 API
    # 这里使用模拟数据演示
    
    # 筛选今日可申购
    today_cbs = [cb for cb in MOCK_SUBSCRIBABLE if cb['subscribe_date'] == date]
    
    if not today_cbs:
        # 如果没有今日数据，返回模拟数据用于演示
        return MOCK_SUBSCRIBABLE
    
    return today_cbs


def get_cb_calendar(start_date=None, end_date=None):
    """
    获取可转债申购日历
    
    Args:
        start_date: 开始日期 YYYY-MM-DD
        end_date: 结束日期 YYYY-MM-DD
        
    Returns:
        list: 日历数据
    """
    if start_date is None:
        start_date = datetime.now().strftime("%Y-%m-%d")
    if end_date is None:
        end_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    
    # 合并所有数据
    all_cbs = MOCK_SUBSCRIBABLE + MOCK_CALENDAR
    
    # 筛选日期范围内的
    result = []
    for cb in all_cbs:
        cb_date = cb['subscribe_date']
        if start_date <= cb_date <= end_date:
            result.append({
                'date': cb_date,
                'code': cb['code'],
                'name': cb['name'],
                'amount': cb.get('amount', 0),
                'rating': cb.get('rating', 'N/A'),
            })
    
    # 按日期排序
    result.sort(key=lambda x: x['date'])
    
    return result


def fetch_from_dongfangcai():
    """
    从东方财富获取真实数据
    
    API 端点示例（需要逆向工程）:
    http://data.eastmoney.com/kzz/default.html
    
    Returns:
        list: 转债数据
    """
    # TODO: 实现真实 API 调用
    # 需要处理反爬虫
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'http://data.eastmoney.com/kzz/',
    }
    
    try:
        # 示例 URL（实际需要找到正确的 API）
        url = "http://datacenter-web.eastmoney.com/api/data/v1/get"
        params = {
            'reportName': 'RPT_BOND_CB_ISSUE',
            'columns': 'ALL',
            'filter': '',
            'pageNum': 1,
            'pageSize': 50,
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return parse_dongfangcai_data(data)
    except Exception as e:
        print(f"获取数据失败：{e}")
    
    return None


def parse_dongfangcai_data(data):
    """解析东方财富数据"""
    # TODO: 实现数据解析逻辑
    result = []
    
    # 根据实际 API 返回结构解析
    if 'result' in data and 'data' in data['result']:
        for item in data['result']['data']:
            result.append({
                'code': item.get 'SECURITY_CODE'),
                'name': item.get('SECURITY_NAME'),
                'amount': item.get('ISSUE_AMOUNT'),
                'rating': item.get('RATING'),
                'subscribe_date': item.get('SUBSCRIBE_DATE'),
                'stock_name': item.get('STOCK_NAME'),
                'stock_code': item.get('STOCK_CODE'),
            })
    
    return result


if __name__ == "__main__":
    # 测试
    print("今日可申购转债:")
    today = get_subscribable_cbs()
    for cb in today:
        print(f"  {cb['name']} ({cb['code']}) - {cb['amount']}亿")
    
    print("\n本周申购日历:")
    calendar = get_cb_calendar()
    for item in calendar:
        print(f"  {item['date']}: {item['name']} ({item['code']})")
