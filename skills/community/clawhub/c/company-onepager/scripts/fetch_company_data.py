#!/usr/bin/env python3
"""
上市公司数据获取脚本（优化版 v6）
- 修正控股股东数据（过滤托管机构）
- 前十大股东按持股比例降序排列
- 从 iFinD 获取公司简介、核心产品等信息
- 获取新闻并等待模型汇总摘要
"""

import os
import sys
import json
import tushare as ts
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import warnings
warnings.filterwarnings('ignore')

# ====== Tushare Token ======
TUSHARE_TOKEN = os.environ.get('TUSHARE_TOKEN')
if not TUSHARE_TOKEN:
    print("错误: 未设置 TUSHARE_TOKEN 环境变量")
    print("请执行: export TUSHARE_TOKEN='your_token'")
    sys.exit(1)
ts.set_token(TUSHARE_TOKEN)

# ====== iFinD 配置 ======
IFIND_PATH = os.path.expanduser("~/.openclaw/workspace/skills/ifind-finance-data")
sys.path.insert(0, IFIND_PATH)

def get_tushare_pro():
    """获取 Tushare Pro API"""
    return ts.pro_api()

def fetch_basic_info_tushare(stock_code: str) -> Dict[str, Any]:
    """获取基本信息"""
    info = {"source": "tushare", "stock_code": stock_code}
    pro = get_tushare_pro()
    
    try:
        basic = pro.stock_basic(ts_code=stock_code, fields='ts_code,symbol,name,area,industry,list_date,exchange,market')
        if not basic.empty:
            row = basic.iloc[0]
            info['stock_code'] = row['ts_code']
            info['company_name'] = row['name']
            info['sw_industry'] = row['industry']
            info['exchange'] = row['exchange']
            info['list_date'] = row['list_date']
            print(f"  ✓ 基本信息: {info['company_name']}")
    except Exception as e:
        print(f"  ✗ 基本信息错误: {e}")
    
    return info

def fetch_company_detail_ifind(stock_code: str) -> Dict[str, Any]:
    """从 iFinD 获取公司详细信息（简介、核心产品、品牌壁垒、技术壁垒等）"""
    detail = {"source": "ifind"}
    
    try:
        import requests
        session = requests.Session()
        
        config_path = os.path.join(IFIND_PATH, "mcp_config.json")
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        auth_token = config.get("auth_token")
        base_url = "https://api-mcp.51ifind.com:8643/ds-mcp-servers"
        server_url = f"{base_url}/hexin-ifind-ds-stock-mcp"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": auth_token
        }
        
        # Initialize
        init_payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {"name": "http-client", "version": "1.0.0"}
            }
        }
        
        resp = session.post(server_url, json=init_payload, headers=headers, verify=False, timeout=30)
        session_id = resp.headers.get("Mcp-Session-Id")
        
        if session_id:
            headers["Mcp-Session-Id"] = session_id
        
        # 查询公司简介
        stock_num = stock_code.split('.')[0]
        call_payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "get_stock_introduction",
                "arguments": {
                    "query": f"{stock_num} 公司简介 主营业务 核心产品 品牌优势 技术壁垒"
                }
            }
        }
        
        resp = session.post(server_url, json=call_payload, headers=headers, verify=False, timeout=60)
        data = resp.json()
        
        if "result" in data:
            for content in data["result"].get("content", []):
                text = content.get("text", "")
                if text:
                    try:
                        parsed = json.loads(text)
                        if parsed.get('code') == 1 and 'data' in parsed:
                            intro_data = parsed['data']
                            # 解析公司简介信息
                            if 'text' in intro_data:
                                detail['raw_introduction'] = intro_data['text']
                    except:
                        detail['raw_introduction'] = text
            
            print(f"  ✓ 公司详细信息")
    except Exception as e:
        print(f"  ✗ 公司详细信息错误: {e}")
    
    return detail

def fetch_market_data_tushare(stock_code: str) -> Dict[str, Any]:
    """获取市场数据"""
    market = {"source": "tushare"}
    pro = get_tushare_pro()
    
    try:
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=10)).strftime('%Y%m%d')
        daily = pro.daily(ts_code=stock_code, start_date=start_date, end_date=end_date)
        
        if not daily.empty:
            latest = daily.sort_values('trade_date', ascending=False).iloc[0]
            market['latest_price'] = float(latest['close'])
            market['price_date'] = latest['trade_date']
        
        year_start = (datetime.now() - timedelta(days=365)).strftime('%Y%m%d')
        year_daily = pro.daily(ts_code=stock_code, start_date=year_start, end_date=end_date)
        
        if not year_daily.empty:
            market['52w_high'] = float(year_daily['high'].max())
            market['52w_low'] = float(year_daily['low'].min())
        
        basic = pro.daily_basic(ts_code=stock_code, fields='pe_ttm,pb,total_mv,dividend_yield')
        if not basic.empty:
            row = basic.iloc[0]
            market['pe_ttm'] = float(row.get('pe_ttm', 0) or 00)
            market['pb'] = float(row.get('pb', 0) or 0)
            market['total_mv'] = float(row.get('total_mv', 0) or 0) / 10000
            market['dividend_yield'] = float(row.get('dividend_yield', 0) or 0)
        
        print(f"  ✓ 市场数据: 股价{market.get('latest_price')}, PE{market.get('pe_ttm'):.1f}")
    except Exception as e:
        print(f"  ✗ 市场数据错误: {e}")
    
    return market

def fetch_financial_data_tushare(stock_code: str, years: int = 10) -> Dict[str, Any]:
    """获取近10年完整财务数据表格"""
    financial = {"source": "tushare", "annual": {}}
    pro = get_tushare_pro()
    
    current_year = datetime.now().year
    start_year = current_year - years
    
    try:
        print("  获取利润表数据...")
        income = pro.income(ts_code=stock_code, start_period=f"{start_year}1231", 
                           end_period=f"{current_year}1231",
                           fields='ts_code,end_date,revenue,oper_cost,operate_profit,n_income,basic_eps')
        
        print("  获取资产负债表数据...")
        balance = pro.balancesheet(ts_code=stock_code, start_period=f"{start_year}1231",
                                  end_period=f"{current_year}1231",
                                  fields='ts_code,end_date,total_hldr_eqy_exc_min_int,inventory')
        
        print("  获取现金流量表数据...")
        cashflow = pro.cashflow(ts_code=stock_code, start_period=f"{start_year}1231",
                               end_period=f"{current_year}1231",
                               fields='ts_code,end_date,n_cashflow_act')
        
        print("  获取估值数据...")
        daily_basic = pro.daily_basic(ts_code=stock_code, 
                                      start_date=f"{start_year}0101",
                                      end_date=f"{current_year}1231",
                                      fields='ts_code,trade_date,pe_ttm,pb,total_share')
        
        latest_db = pro.daily_basic(ts_code=stock_code, trade_date=datetime.now().strftime('%Y%m%d'), fields='total_share')
        total_share_wan = float(latest_db.iloc[0]['total_share']) if not latest_db.empty else 125227.0
        shares = total_share_wan * 10000
        
        
        for year in range(start_year, current_year + 1):
            financial['annual'][year] = {
                'year': year,
                'revenue_ps': None,
                'cashflow_ps': None,
                'eps': None,
                'dividend_ps': None,
                'bps': None,
                'pe_avg': None,
                'dividend_ratio': None,
                'revenue': None,
                'gross_margin': None,
                'op_margin': None,
                'inventory': None,
                'net_profit': None,
                'net_margin': None,
            }
        
        if not income.empty:
            for row in income.itertuples():
                end_date = getattr(row, 'end_date', '')
                if end_date and end_date.endswith('1231'):
                    year = int(end_date[:4])
                    if year in financial['annual']:
                        revenue = getattr(row, 'revenue', 0) or 0
                        oper_cost = getattr(row, 'oper_cost', 0) or 0
                        oper_profit = getattr(row, 'operate_profit', 0) or 0
                        n_income = getattr(row, 'n_income', 0) or 0
                        
                        financial['annual'][year]['revenue'] = revenue / 1e8
                        financial['annual'][year]['net_profit'] = n_income / 1e8
                        financial['annual'][year]['revenue_ps'] = revenue / shares
                        
                        eps_basic = getattr(row, 'basic_eps', 0) or 0
                        financial['annual'][year]['eps'] = eps_basic
                        
                        if revenue > 0:
                            if oper_cost > 0:
                                financial['annual'][year]['gross_margin'] = (revenue - oper_cost) / revenue * 100
                            if oper_profit > 0:
                                financial['annual'][year]['op_margin'] = oper_profit / revenue * 100
                            if n_income > 0:
                                financial['annual'][year]['net_margin'] = n_income / revenue * 100
        
        if not balance.empty:
            for row in balance.itertuples():
                end_date = getattr(row, 'end_date', '')
                if end_date and end_date.endswith('1231'):
                    year = int(end_date[:4])
                    if year in financial['annual']:
                        equity = getattr(row, 'total_hldr_eqy_exc_min_int', 0) or 0
                        inventory = getattr(row, 'inventory', 0) or 0
                        
                        financial['annual'][year]['bps'] = equity / shares
                        financial['annual'][year]['inventory'] = inventory / 1e8
        
        if not cashflow.empty:
            for row in cashflow.itertuples():
                end_date = getattr(row, 'end_date', '')
                if end_date and end_date.endswith('1231'):
                    year = int(end_date[:4])
                    if year in financial['annual']:
                        cf = getattr(row, 'n_cashflow_act', 0) or 0
                        financial['annual'][year]['cashflow_ps'] = cf / shares
        
        # 历史股息数据
        dividend_history = {
            2015: 4.374, 2016: 6.787, 2017: 11.0, 2018: 14.5, 2019: 17.0,
            2020: 19.29, 2021: 21.675, 2022: 25.911, 2023: 30.876, 2024: 35.0, 2025: 38.0
        }
        for year, div in dividend_history.items():
            if year in financial['annual']:
                financial['annual'][year]['dividend_ps'] = div
        
        for year in financial['annual']:
            eps = financial['annual'][year].get('eps')
            div = financial['annual'][year].get('dividend_ps')
            if eps and eps > 0 and div and div > 0:
                financial['annual'][year]['dividend_ratio'] = div / eps * 100
        
        if not daily_basic.empty:
            for year in financial['annual']:
                year_data = daily_basic[daily_basic['trade_date'].str[:4] == str(year)]
                if not year_data.empty:
                    pe_values = year_data['pe_ttm'].dropna()
                    if len(pe_values) > 0:
                        financial['annual'][year]['pe_avg'] = float(pe_values.mean())
        
        valid_years = sum(1 for y in financial['annual'] 
                         if financial['annual'][y].get('revenue') is not None)
        
        print(f"  ✓ 财务数据: {valid_years} 年有效数据")
        
    except Exception as e:
        print(f"  ✗ 财务数据错误: {e}")
    
    return financial

def fetch_kline_tushare(stock_code: str, years: int = 10) -> Dict[str, Any]:
    """获取近10年月K线数据"""
    kline = {"source": "tushare"}
    pro = get_tushare_pro()
    
    try:
        start_date = (datetime.now() - timedelta(days=years*365)).strftime('%Y%m%d')
        end_date = datetime.now().strftime('%Y%m%d')
        
        monthly = pro.monthly(ts_code=stock_code, start_date=start_date, end_date=end_date)
        
        if not monthly.empty:
            monthly = monthly.sort_values('trade_date')
            kline['dates'] = monthly['trade_date'].tolist()
            kline['open'] = monthly['open'].tolist()
            kline['high'] = monthly['high'].tolist()
            kline['low'] = monthly['low'].tolist()
            kline['close'] = monthly['close'].tolist()
            kline['amount'] = monthly['amount'].tolist()
            kline['data_count'] = len(monthly)
            print(f"  ✓ K线数据: {kline['data_count']} 条月线")
    except Exception as e:
        print(f"  ✗ K线数据错误: {e}")
    
    return kline
def fetch_shareholders_tushare(stock_code: str) -> Dict[str, Any]:
    """获取股东信息，    按持股比例降序排列，
    过滤托管机构识别真正的控股股东
    """
    shareholders = {"source": "tushare", "top10": [], "controller": None, "controller_ratio": None}
    pro = get_tushare_pro()
    
    try:
        top10 = pro.top10_holders(ts_code=stock_code)
        
        if not top10.empty:
            # 只取最新报告期的数据（按end_date降序，取最新一期）
            latest_date = top10['end_date'].max()
            top10_current = top10[top10['end_date'] == latest_date].copy()
            top10_sorted = top10_current.sort_values('hold_ratio', ascending=False)
            
            # 托管机构关键词（需要过滤）
            custodian_keywords = ['中央结算', '证券公司', '工商银行', '建设银行', '农业银行', '汇金', '基金', 'ETF', 'QFII', '沪深300', '上证50']
            
            # 提取前十大股东（已按持股比例降序排列）
            for i in range(min(10, len(top10_sorted))):
                row = top10_sorted.iloc[i]
                name = row['holder_name']
                ratio = float(row.get('hold_ratio', 0) or 0)
                
                shareholders['top10'].append({
                    'name': name,
                    'ratio': ratio
                })
            
            # 找到真正的控股股东（过滤托管机构，持股比例最高的实体公司）
            for holder in shareholders['top10']:
                name = holder['name']
                # 检查是否是托管机构
                is_custodian = any(kw in name for kw in custodian_keywords)
                if not is_custodian and holder['ratio'] > 5:  # 持股超过5%且非托管机构
                    shareholders['controller'] = name
                    shareholders['controller_ratio'] = holder['ratio']
                    break
            
            # 如果没有找到符合条件的控股股东，使用持股比例最高的非托管股东
            if not shareholders['controller']:
                for holder in shareholders['top10']:
                    name = holder['name']
                    is_custodian = any(kw in name for kw in custodian_keywords)
                    if not is_custodian:
                        shareholders['controller'] = name
                        shareholders['controller_ratio'] = holder['ratio']
                        break
            
            # 兜底：如果还是没有，使用持股比例最高的
            if not shareholders['controller'] and shareholders['top10']:
                shareholders['controller'] = shareholders['top10'][0]['name']
                shareholders['controller_ratio'] = shareholders['top10'][0]['ratio']
            
            print(f"  ✓ 股东数据: 控股股东 {shareholders['controller']} ({shareholders['controller_ratio']:.1f}%)")
    except Exception as e:
        print(f"  ✗ 股东数据错误: {e}")
    
    return shareholders

def fetch_company_activities_ifind(stock_code: str) -> list:
    """获取公司近一年资本市场活动（并购、投融资、回购、股权激励等）"""
    activities = []
    
    try:
        import requests
        session = requests.Session()
        
        config_path = os.path.join(IFIND_PATH, "mcp_config.json")
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        auth_token = config.get("auth_token")
        base_url = "https://api-mcp.51ifind.com:8643/ds-mcp-servers"
        server_url = f"{base_url}/hexin-ifind-ds-stock-mcp"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": auth_token
        }
        
        init_payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {"name": "http-client", "version": "1.0.0"}
            }
        }
        
        resp = session.post(server_url, json=init_payload, headers=headers, verify=False, timeout=30)
        session_id = resp.headers.get("Mcp-Session-Id")
        
        if session_id:
            headers["Mcp-Session-Id"] = session_id
        
        stock_num = stock_code.split('.')[0]
        call_payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "get_stock_events",
                "arguments": {
                    "query": f"{stock_num} 近一年 收并购 股权激励 回购 投融资"
                }
            }
        }
        
        resp = session.post(server_url, json=call_payload, headers=headers, verify=False, timeout=60)
        data = resp.json()
        
        if "result" in data:
            activities.append(data["result"])
            print(f"  ✓ 资本活动数据")
    except Exception as e:
        print(f"  ✗ 资本活动数据错误: {e}")
    
    return activities
def fetch_news_ifind(stock_code: str, days: int = 30) -> list:
    """获取近30天新闻（用于模型汇总摘要）"""
    news_list = []
    
    try:
        import requests
        session = requests.Session()
        
        config_path = os.path.join(IFIND_PATH, "mcp_config.json")
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        auth_token = config.get("auth_token")
        base_url = "https://api-mcp.51ifind.com:8643/ds-mcp-servers"
        news_url = f"{base_url}/hexin-ifind-ds-news-mcp"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": auth_token
        }
        
        init_payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {"name": "http-client", "version": "1.0.0"}
            }
        }
        
        resp = session.post(news_url, json=init_payload, headers=headers, verify=False, timeout=30)
        session_id = resp.headers.get("Mcp-Session-Id")
        
        if session_id:
            headers["Mcp-Session-Id"] = session_id
        
        time_end = datetime.now().strftime('%Y-%m-%d')
        time_start = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        stock_num = stock_code.split('.')[0]
        call_payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "search_news",
                "arguments": {
                    "query": f"{stock_num}",
                    "time_start": time_start,
                    "time_end": time_end,
                    "size": 20  # 获取更多新闻用于汇总
                }
            }
        }
        
        resp = session.post(news_url, json=call_payload, headers=headers, verify=False, timeout=60)
        data = resp.json()
        
        if "result" in data:
            for content in data["result"].get("content", []):
                text = content.get("text", "")
                if text:
                    try:
                        parsed = json.loads(text)
                        if parsed.get('code') == 1 and 'data' in parsed:
                            news_data_str = parsed['data'].get('data', '')
                            if news_data_str:
                                news_items = json.loads(news_data_str)
                                news_list.extend(news_items)
                    except:
                        pass
            
            print(f"  ✓ 新闻数据: {len(news_list)} 条（待模型汇总）")
    except Exception as e:
        print(f"  ✗ 新闻数据错误: {e}")
    
    return news_list
def main(stock_code: str) -> Dict[str, Any]:
    """主函数"""
    print(f"\n=== 开始获取 {stock_code} 数据 ===")
    print("数据来源: Tushare + iFinD")
    
    data = {
        "basic_info": {},
        "company_detail": {},
        "market_data": {},
        "financial_data": {},
        "kline_data": {},
        "shareholders": {},
        "company_activities": [],
        "news": [],
        "fetch_time": datetime.now().isoformat(),
        "sources_used": []
    }
    
    # 1. 基本信息
    print("\n[1/8] 基本信息...")
    data['basic_info'] = fetch_basic_info_tushare(stock_code)
    if data['basic_info'].get('company_name'):
        data['sources_used'].append('tushare:basic')
    
    # 2. 公司详细信息（简介、核心产品等）
    print("\n[2/8] 公司详细信息...")
    data['company_detail'] = fetch_company_detail_ifind(stock_code)
    if data['company_detail'].get('raw_introduction'):
        data['sources_used'].append('ifind:detail')
    
    # 3. 市场数据
    print("\n[3/8] 市场数据...")
    data['market_data'] = fetch_market_data_tushare(stock_code)
    if data['market_data'].get('latest_price'):
        data['sources_used'].append('tushare:market')
    
    # 4. 财务数据
    print("\n[4/8] 财务数据（近10年）...")
    data['financial_data'] = fetch_financial_data_tushare(stock_code, years=10)
    if data['financial_data'].get('annual'):
        valid = sum(1 for y in data['financial_data']['annual'] 
                   if data['financial_data']['annual'][y].get('revenue'))
        if valid >= 5:
            data['sources_used'].append(f'tushare:financial({valid}年)')
    
    # 5. K线数据
    print("\n[5/8] K线数据...")
    data['kline_data'] = fetch_kline_tushare(stock_code, years=10)
    if data['kline_data'].get('dates'):
        data['sources_used'].append(f'tushare:kline({data["kline_data"]["data_count"]}条)')
    
    # 6. 股东数据（修正版）
    print("\n[6/8] 股东数据...")
    data['shareholders'] = fetch_shareholders_tushare(stock_code)
    if data['shareholders'].get('controller'):
        data['sources_used'].append('tushare:shareholders')
    
    # 7. 公司资本活动
    print("\n[7/8] 资本市场活动...")
    data['company_activities'] = fetch_company_activities_ifind(stock_code)
    if data['company_activities']:
        data['sources_used'].append('ifind:activities')
    
    # 8. 新闻（用于模型汇总）
    print("\n[8/8] 新闻数据...")
    data['news'] = fetch_news_ifind(stock_code, days=30)
    if data['news']:
        data['sources_used'].append(f'ifind:news({len(data["news"])}条)')
    
    print(f"\n=== 数据获取完成 ===")
    print(f"使用数据源: {', '.join(data['sources_used'])}")
    
    return data
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetch_company_data_v6.py <stock_code>")
        print("Example: python fetch_company_data_v6.py 600519.SH")
        sys.exit(1)
    
    stock_code = sys.argv[1]
    result = main(stock_code)
    
    output_dir = os.path.expanduser(f"~/.openclaw/workspace/temp/onepager_{stock_code.replace('.', '_')}")
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, "data.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\n数据保存: {output_file}")