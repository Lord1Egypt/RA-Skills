#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基金周报Excel数据读取脚本
从Excel中提取各类基金数据
"""

import pandas as pd
from typing import Dict, List, Any
from datetime import datetime


def read_fund_excel(file_path: str) -> Dict[str, pd.DataFrame]:
    """
    读取基金周度收益Excel文件
    
    参数:
        file_path: Excel文件路径
    
    返回:
        字典，key为Sheet名称，value为DataFrame
    """
    excel_file = pd.ExcelFile(file_path)
    data = {}
    
    for sheet_name in excel_file.sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        data[sheet_name] = df
    
    return data


def extract_active_equity_stats(data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    """
    提取主动权益基金统计数据
    
    返回:
        {
            'weekly_return': {
                '普通股票型基金': {'中位数': -0.0059, '最高值': 0.1019, '95%分位': 0.0221},
                '偏股混合型基金': {...},
                ...
            },
            'ytd_return': {...}
        }
    """
    df = data.get('主动权益_周度收益统计')
    if df is None:
        return {}
    
    result = {
        'weekly_return': {},
        'ytd_return': {}
    }
    
    # 提取近一周收益数据
    fund_types = ['普通股票型基金', '偏股混合型基金', '灵活配置型基金', '平衡混合型基金']
    
    for i, fund_type in enumerate(fund_types):
        # 近一周收益
        result['weekly_return'][fund_type] = {
            '最高值': df.iloc[1, i+1] if len(df) > 1 else None,
            '95%分位': df.iloc[2, i+1] if len(df) > 2 else None,
            '75%分位': df.iloc[3, i+1] if len(df) > 3 else None,
            '50%分位': df.iloc[4, i+1] if len(df) > 4 else None,
            '25%分位': df.iloc[5, i+1] if len(df) > 5 else None,
            '5%分位': df.iloc[6, i+1] if len(df) > 6 else None,
            '最低值': df.iloc[7, i+1] if len(df) > 7 else None,
        }
        
        # 年初以来收益
        result['ytd_return'][fund_type] = {
            '最高值': df.iloc[1, i+5] if len(df) > 1 else None,
            '95%分位': df.iloc[2, i+5] if len(df) > 2 else None,
            '75%分位': df.iloc[3, i+5] if len(df) > 3 else None,
            '50%分位': df.iloc[4, i+5] if len(df) > 4 else None,
            '25%分位': df.iloc[5, i+5] if len(df) > 5 else None,
            '5%分位': df.iloc[6, i+5] if len(df) > 6 else None,
            '最低值': df.iloc[7, i+5] if len(df) > 7 else None,
        }
    
    return result


def extract_industry_fund_returns(data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    """
    提取行业主题基金收益数据
    
    返回:
        {
            'weekly': [
                {'行业': '新能源主题', '收益': 0.0127},
                ...
            ],
            'ytd': [...]
        }
    """
    result = {'weekly': [], 'ytd': []}
    
    # 近一周收益
    df_weekly = data.get('行业基金近一周收益')
    if df_weekly is not None:
        for _, row in df_weekly.iterrows():
            if pd.notna(row.get('所属行业板块')) and pd.notna(row.get('近一周收益')):
                result['weekly'].append({
                    '行业': row['所属行业板块'],
                    '收益': row['近一周收益']
                })
    
    # 年初以来收益
    df_ytd = data.get('行业基金年初以来收益')
    if df_ytd is not None:
        for _, row in df_ytd.iterrows():
            if pd.notna(row.get('所属行业板块')) and pd.notna(row.get('年初以来收益')):
                result['ytd'].append({
                    '行业': row['所属行业板块'],
                    '收益': row['年初以来收益']
                })
    
    return result


def extract_top_funds(data: Dict[str, pd.DataFrame], sheet_name: str) -> List[Dict[str, Any]]:
    """
    提取头部绩优基金数据
    
    参数:
        data: Excel数据字典
        sheet_name: Sheet名称
    
    返回:
        [
            {
                '基金代码': '007590.OF',
                '证券简称': '华宝绿色领先',
                '近一周收益': 0.1019,
                '基金经理': '夏林锋',
                ...
            },
            ...
        ]
    """
    df = data.get(sheet_name)
    if df is None:
        return []
    
    top_funds = []
    
    # 根据不同的Sheet调整列名
    for _, row in df.iterrows():
        fund = {}
        
        # 提取基金代码、名称、收益等信息
        if '基金代码' in df.columns:
            fund['基金代码'] = row.get('基金代码')
        if '证券简称' in df.columns:
            fund['证券简称'] = row.get('证券简称')
        if '近一周收益' in df.columns:
            fund['近一周收益'] = row.get('近一周收益')
        if '年初以来收益' in df.columns:
            fund['年初以来收益'] = row.get('年初以来收益')
        if '基金经理' in df.columns:
            fund['基金经理'] = row.get('基金经理')
        
        if fund.get('证券简称'):  # 确保有基金名称
            top_funds.append(fund)
    
    return top_funds[:10]  # 返回前10名


def extract_fixed_income_stats(data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    """
    提取固定收益基金统计数据
    """
    df = data.get('固定收益_周度收益统计')
    if df is None:
        return {}
    
    result = {
        'weekly_return': {},
        'ytd_return': {}
    }
    
    # 提取数据（需要根据实际结构调整）
    # 这里简化处理，实际需要根据Excel结构调整
    
    return result


def extract_index_fund_returns(data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    """
    提取指数基金收益数据
    """
    result = {
        'weekly': [],
        'ytd': [],
        'average': []
    }
    
    # 近一周收益
    df_weekly = data.get('指数基金近一周收益')
    if df_weekly is not None:
        for _, row in df_weekly.iterrows():
            if pd.notna(row.get('四级分类')) and pd.notna(row.get('近一周收益')):
                result['weekly'].append({
                    '类型': row['四级分类'],
                    '收益': row['近一周收益']
                })
    
    # 年初以来收益
    df_ytd = data.get('指数基金年初以来收益')
    if df_ytd is not None:
        for _, row in df_ytd.iterrows():
            if pd.notna(row.get('四级分类')) and pd.notna(row.get('年初以来收益')):
                result['ytd'].append({
                    '类型': row['四级分类'],
                    '收益': row['年初以来收益']
                })
    
    # 平均收益
    df_avg = data.get('指数基金_平均收益')
    if df_avg is not None:
        for _, row in df_avg.iterrows():
            if pd.notna(row.get('四级分类')):
                result['average'].append({
                    '类型': row['四级分类'],
                    '近一周收益': row.get('近一周收益'),
                    '年初以来收益': row.get('年初以来收益')
                })
    
    return result


def extract_fof_returns(data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    """
    提取FOF基金收益数据
    """
    result = {
        'weekly': [],
        'ytd': []
    }
    
    # 近一周收益
    df_weekly = data.get('FOF近一周收益')
    if df_weekly is not None:
        for _, row in df_weekly.iterrows():
            if pd.notna(row.get('投资类型')) and pd.notna(row.get('近一周收益')):
                result['weekly'].append({
                    '类型': row['投资类型'],
                    '收益': row['近一周收益']
                })
    
    # 年初以来收益
    df_ytd = data.get('FOF年初以来收益')
    if df_ytd is not None:
        for _, row in df_ytd.iterrows():
            if pd.notna(row.get('投资类型')) and pd.notna(row.get('年初以来收益')):
                result['ytd'].append({
                    '类型': row['投资类型'],
                    '收益': row['年初以来收益']
                })
    
    return result


def extract_new_funds(data: Dict[str, pd.DataFrame]) -> Dict[str, List[Dict]]:
    """
    提取新成立、新发行、新申报基金数据
    """
    result = {
        'established': [],
        'issued': [],
        'declared': []
    }
    
    # 新成立基金
    df_est = data.get('本周新成立的基金')
    if df_est is not None:
        for _, row in df_est.iterrows():
            fund = {
                '基金代码': row.get('证券代码'),
                '证券简称': row.get('证券简称'),
                '基金成立日': row.get('基金成立日'),
                '投资类型': row.get('投资类型(二级分类)'),
                '发行规模': row.get('发行规模(亿元)'),
                '基金经理': row.get('基金经理')
            }
            if fund.get('证券简称'):
                result['established'].append(fund)
    
    # 新发行基金
    df_issue = data.get('本周新发行的基金')
    if df_issue is not None:
        for _, row in df_issue.iterrows():
            fund = {
                '基金代码': row.get('证券代码'),
                '证券简称': row.get('证券简称'),
                '发行起始日': row.get('发行起始日'),
                '发行终止日': row.get('发行终止日'),
                '投资类型': row.get('投资类型(二级分类)'),
                '基金经理': row.get('基金经理')
            }
            if fund.get('证券简称'):
                result['issued'].append(fund)
    
    # 新申报基金
    df_decl = data.get('本周新申报的基金')
    if df_decl is not None:
        for _, row in df_decl.iterrows():
            fund = {
                '基金管理人': row.get('基金管理人'),
                '基金名称': row.get('基金名称'),
                '基金类型': row.get('基金类型1'),
                '申请日期': row.get('申请材料接收日')
            }
            if fund.get('基金名称'):
                result['declared'].append(fund)
    
    return result


def get_date_range(data: Dict[str, pd.DataFrame]) -> tuple:
    """
    从数据中推断日期范围
    
    返回:
        (start_date, end_date) 格式为 'MMDD'
    """
    # 从新成立基金中获取日期
    df = data.get('本周新成立的基金')
    if df is not None and len(df) > 0:
        dates = df['基金成立日'].dropna()
        if len(dates) > 0:
            # 获取最早和最晚日期
            dates = pd.to_datetime(dates)
            start_date = dates.min().strftime('%m%d')
            end_date = dates.max().strftime('%m%d')
            return (start_date, end_date)
    
    return ('0000', '0000')


def extract_etf_flow_data(etf_file_path: str) -> Dict[str, Any]:
    """
    从ETF资金流动Excel中提取数据
    
    参数:
        etf_file_path: ETF资金流动跟踪Excel文件路径
    
    返回:
        {
            'sector_flow': [...],  # 板块资金流动
            'top_inflow': [...],    # 净申购TOP
            'top_outflow': [...],   # 净赎回TOP
            'core_index_flow': [...], # 核心宽基ETF资金流动
            'hot_theme_flow': [...]  # 热门行业主题资金流动
        }
    """
    result = {
        'sector_flow': [],
        'top_inflow': [],
        'top_outflow': [],
        'core_index_flow': [],
        'hot_theme_flow': []
    }
    
    try:
        # 读取板块结果展示
        df_sector = pd.read_excel(etf_file_path, sheet_name='板块结果展示')
        
        for _, row in df_sector.iterrows():
            if pd.notna(row.get('二级分类')) and pd.notna(row.get('资金流入总额（亿元）')):
                result['sector_flow'].append({
                    '板块': row.get('Unnamed: 5') or row.get('二级分类'),
                    '资金流入总额': row.get('资金流入总额（亿元）'),
                    '基金数量': row.get('基金数量'),
                    '平均涨跌幅': row.get('平均涨跌幅')
                })
        
        # 读取个基结果展示（净申购TOP）
        df_top = pd.read_excel(etf_file_path, sheet_name='个基结果展示')
        
        for _, row in df_top.iterrows():
            if pd.notna(row.get('基金名称')) and pd.notna(row.get('资金流入规模（亿元）')):
                inflow = row.get('资金流入规模（亿元）')
                result['top_inflow'].append({
                    '基金代码': row.get('基金代码'),
                    '基金名称': row.get('基金名称'),
                    '资金流入规模': inflow,
                    '最新规模': row.get('最新规模（亿元）'),
                    '最新涨跌幅': row.get(' 最新涨跌幅')
                })
        
        # 按资金流入规模排序
        result['top_inflow'] = sorted(result['top_inflow'], key=lambda x: x['资金流入规模'] if isinstance(x['资金流入规模'], (int, float)) else 0, reverse=True)
        
        # 从已上市ETF中提取净赎回TOP
        df_etf = pd.read_excel(etf_file_path, sheet_name='已上市ETF')
        
        outflow_list = []
        for _, row in df_etf.iterrows():
            net_flow = row.get('周净申赎额\n[起始交易日期] 2026-03-09\n[截止交易日期] 2026-03-13\n[单位] 亿元')
            if pd.notna(net_flow) and net_flow < 0:
                outflow_list.append({
                    '基金代码': row.get('证券代码'),
                    '基金名称': row.get('证券简称'),
                    '基金公司': row.get('基金管理人简称'),
                    '净申赎额': net_flow,
                    '基金规模': row.get('基金规模\n[报告期] 2026-03-13\n[单位] 亿元')
                })
        
        # 按净赎回额排序（从小到大，即赎回最多的排前面）
        result['top_outflow'] = sorted(outflow_list, key=lambda x: x['净申赎额'] if isinstance(x['净申赎额'], (int, float)) else 0)
        
        # 读取核心宽基赛道
        df_core = pd.read_excel(etf_file_path, sheet_name='核心宽基赛道')
        
        for _, row in df_core.iterrows():
            if pd.notna(row.get('跟踪指数')):
                result['core_index_flow'].append({
                    '跟踪指数': row.get('跟踪指数'),
                    '指数类型': row.get('指数类型'),
                    '基金数量': row.get('基金数量'),
                    '合计规模': row.get('合计规模（亿元）'),
                    '净申购额': row.get('净申购额（亿元）'),
                    '代表产品': row.get('代表产品'),
                    '基金简称': row.get('基金简称'),
                    '代表产品净申购额': row.get('净申购额（亿元）.1')
                })
        
        # 读取热门行业主题
        df_theme = pd.read_excel(etf_file_path, sheet_name='热门行业主题')
        
        for _, row in df_theme.iterrows():
            if pd.notna(row.get('指数简称')):
                result['hot_theme_flow'].append({
                    '指数简称': row.get('指数简称'),
                    'ETF数量': row.get('ETF数量'),
                    '合计规模': row.get('合计规模'),
                    '净申赎额': row.get('净申赎额'),
                    '周收益率': row.get('周收益率'),
                    '代表基金': row.get('代表基金'),
                    '基金简称': row.get('基金简称'),
                    '周申赎额': row.get('周申赎额')
                })
        
    except Exception as e:
        print(f"读取ETF资金流动数据失败: {e}")
    
    return result


if __name__ == '__main__':
    # 测试脚本
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python read_excel.py <excel_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    data = read_fund_excel(file_path)
    
    print(f"读取到 {len(data)} 个Sheet")
    
    # 测试提取主动权益基金数据
    stats = extract_active_equity_stats(data)
    print("\n主动权益基金统计:")
    print(stats)
    
    # 测试提取行业基金数据
    industry = extract_industry_fund_returns(data)
    print("\n行业基金收益:")
    print(industry)
    
    # 测试日期范围
    date_range = get_date_range(data)
    print(f"\n日期范围: {date_range[0]}-{date_range[1]}")
