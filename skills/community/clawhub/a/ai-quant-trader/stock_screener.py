#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
选股引擎 - 支持复杂条件筛选
"""

import akshare as ak
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import json
import os
from data_provider import DataProvider

class StockScreener:
    """股票筛选器"""
    
    def __init__(self, data_provider=None):
        self.data_provider = data_provider or DataProvider()
        self.cache_dir = os.path.join(os.path.dirname(__file__), "screener_cache")
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # 市场类型映射
        self.market_types = {
            'sh': '上海主板',
            'sz': '深圳主板',
            'bj': '北京交易所',
            'cy': '创业板',
            'kc': '科创板'
        }
        
        print("✅ 选股引擎初始化完成")
    
    def get_all_a_shares(self):
        """获取所有沪深A股"""
        try:
            cache_file = os.path.join(self.cache_dir, "all_a_shares.json")
            
            # 检查缓存（缓存1小时）
            if os.path.exists(cache_file):
                file_mtime = os.path.getmtime(cache_file)
                if (time.time() - file_mtime) < 3600:
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        return pd.DataFrame(json.load(f))
            
            # 从AKShare获取所有A股
            print("📊 正在获取沪深A股列表...")
            
            # 获取沪深京A股实时行情（包含所有股票）
            df = ak.stock_zh_a_spot_em()
            
            if df.empty:
                print("❌ 无法获取A股列表")
                return pd.DataFrame()
            
            # 保存到缓存
            df.to_json(cache_file, orient='records', force_ascii=False)
            
            print(f"✅ 获取到 {len(df)} 只A股")
            return df
            
        except Exception as e:
            print(f"❌ 获取A股列表失败: {e}")
            return pd.DataFrame()
    
    def filter_by_market_type(self, df, exclude_types=None):
        """按市场类型筛选"""
        if df.empty:
            return df
        
        if exclude_types is None:
            exclude_types = ['ST', '创业', '科创', '北交所']
        
        result_df = df.copy()
        
        # 筛选非ST
        if 'ST' in exclude_types:
            result_df = result_df[~result_df['名称'].str.contains('ST')]
            result_df = result_df[~result_df['名称'].str.contains('退市')]
        
        # 筛选非创业板（代码以300开头）
        if '创业' in exclude_types:
            result_df = result_df[~result_df['代码'].astype(str).str.startswith('300')]
        
        # 筛选非科创板（代码以688开头）
        if '科创' in exclude_types:
            result_df = result_df[~result_df['代码'].astype(str).str.startswith('688')]
        
        # 筛选非北交所（代码以8开头）
        if '北交所' in exclude_types:
            result_df = result_df[~result_df['代码'].astype(str).str.startswith('8')]
        
        return result_df
    
    def get_financial_data(self, symbol):
        """获取财务数据（简化版）"""
        try:
            # 这里需要更复杂的财务数据获取
            # 暂时返回模拟数据
            return {
                'ROE': np.random.uniform(-10, 20),  # 模拟ROE
                'current_ratio': np.random.uniform(0.3, 2.0),  # 流动比率
                'market_cap': np.random.uniform(10, 500) * 100000000,  # 市值（元）
            }
        except:
            # 如果获取失败，返回默认值
            return {
                'ROE': 0,
                'current_ratio': 1.0,
                'market_cap': 10000000000,
            }
    
    def calculate_technical_indicators(self, df, symbol, days=5):
        """计算技术指标"""
        try:
            end_date = datetime.now().strftime('%Y%m%d')
            start_date = (datetime.now() - timedelta(days=days+10)).strftime('%Y%m%d')
            
            # 获取历史数据
            hist_data = self.data_provider.get_historical_data(symbol, start_date, end_date)
            
            if hist_data.empty or len(hist_data) < days:
                return {
                    'price_change_2d': 0,
                    'amplitude': 0,
                    'volume_ratio': 1.0,
                    'turnover_rate': 0,
                    'weekly_volume_growth': 0
                }
            
            # 2日涨跌幅
            if len(hist_data) >= 3:
                price_2d_ago = float(hist_data.iloc[-3]['收盘'])
                price_current = float(hist_data.iloc[-1]['收盘'])
                price_change_2d = ((price_current - price_2d_ago) / price_2d_ago) * 100
            else:
                price_change_2d = 0
            
            # 当日涨幅
            if len(hist_data) >= 2:
                price_yesterday = float(hist_data.iloc[-2]['收盘'])
                price_today = float(hist_data.iloc[-1]['收盘'])
                daily_change = ((price_today - price_yesterday) / price_yesterday) * 100
            else:
                daily_change = 0
            
            # 振幅（当日）
            if '最高' in hist_data.columns and '最低' in hist_data.columns:
                high = float(hist_data.iloc[-1]['最高'])
                low = float(hist_data.iloc[-1]['最低'])
                close = float(hist_data.iloc[-1]['收盘'])
                amplitude = ((high - low) / close) * 100
            else:
                amplitude = 0
            
            # 量比（简化：当日成交量/5日均量）
            if '成交量' in hist_data.columns and len(hist_data) >= 6:
                volume_today = float(hist_data.iloc[-1]['成交量'])
                volume_ma5 = hist_data['成交量'].tail(5).mean()
                volume_ratio = volume_today / volume_ma5 if volume_ma5 > 0 else 1.0
            else:
                volume_ratio = 1.0
            
            # 换手率（从实时数据获取）
            turnover_rate = 0
            if '换手率' in df.columns:
                stock_row = df[df['代码'] == symbol]
                if not stock_row.empty:
                    turnover_str = str(stock_row.iloc[0]['换手率'])
                    if '%' in turnover_str:
                        turnover_rate = float(turnover_str.replace('%', ''))
                    else:
                        try:
                            turnover_rate = float(turnover_str)
                        except:
                            turnover_rate = 0
            
            # 周成交量环比增长（本周/上周）
            weekly_volume_growth = 0
            if len(hist_data) >= 10:  # 至少10个交易日
                # 本周成交量（最近5天）
                volume_this_week = hist_data['成交量'].tail(5).sum()
                # 上周成交量（前5天）
                volume_last_week = hist_data['成交量'].iloc[-10:-5].sum()
                
                if volume_last_week > 0:
                    weekly_volume_growth = ((volume_this_week - volume_last_week) / volume_last_week) * 100
            
            return {
                'price_change_2d': price_change_2d,
                'daily_change': daily_change,
                'amplitude': amplitude,
                'volume_ratio': volume_ratio,
                'turnover_rate': turnover_rate,
                'weekly_volume_growth': weekly_volume_growth
            }
            
        except Exception as e:
            print(f"计算技术指标失败 {symbol}: {e}")
            return {
                'price_change_2d': 0,
                'daily_change': 0,
                'amplitude': 0,
                'volume_ratio': 1.0,
                'turnover_rate': 0,
                'weekly_volume_growth': 0
            }
    
    def screen_stocks(self, conditions):
        """
        执行股票筛选
        
        Args:
            conditions: 筛选条件字典
        """
        print("🔍 开始执行选股策略...")
        
        # 获取所有A股
        all_stocks = self.get_all_a_shares()
        if all_stocks.empty:
            return pd.DataFrame()
        
        print(f"📊 初始股票池: {len(all_stocks)} 只")
        
        # 应用市场类型筛选
        filtered_stocks = self.filter_by_market_type(
            all_stocks, 
            exclude_types=['ST', '创业', '科创', '北交所']
        )
        print(f"📊 市场类型筛选后: {len(filtered_stocks)} 只")
        
        # 存储筛选结果
        screened_stocks = []
        
        # 遍历每只股票应用条件
        for idx, stock in filtered_stocks.iterrows():
            symbol = str(stock['代码'])
            
            try:
                # 获取财务数据（模拟）
                financials = self.get_financial_data(symbol)
                
                # 获取技术指标
                technicals = self.calculate_technical_indicators(filtered_stocks, symbol)
                
                # 应用筛选条件
                passed = True
                
                # 1. ROE > -20% 且 < 15%
                roe = financials['ROE']
                if not (-20 < roe < 15):
                    passed = False
                
                # 2. 流动比率 ≥ 0.4
                current_ratio = financials['current_ratio']
                if current_ratio < 0.4:
                    passed = False
                
                # 3. 市值小于100亿元
                market_cap = financials['market_cap']
                if market_cap >= 100 * 100000000:  # 100亿元
                    passed = False
                
                # 4. 2日涨跌幅 < 5% 且 涨幅 < 3%
                price_change_2d = technicals['price_change_2d']
                daily_change = technicals['daily_change']
                if not (abs(price_change_2d) < 5 and daily_change < 3):
                    passed = False
                
                # 5. 振幅小于6%
                amplitude = technicals['amplitude']
                if amplitude >= 6:
                    passed = False
                
                # 6. 量比 > 0.8
                volume_ratio = technicals['volume_ratio']
                if volume_ratio <= 0.8:
                    passed = False
                
                # 7. 换手率大于1%小于10%
                turnover_rate = technicals['turnover_rate']
                if not (1 < turnover_rate < 10):
                    passed = False
                
                if passed:
                    # 收集股票信息
                    stock_info = {
                        '代码': symbol,
                        '名称': stock['名称'],
                        '最新价': float(stock['最新价']) if '最新价' in stock else 0,
                        '涨跌幅': float(stock['涨跌幅'].replace('%', '')) if '涨跌幅' in stock and isinstance(stock['涨跌幅'], str) else 0,
                        'ROE': round(roe, 2),
                        '流动比率': round(current_ratio, 2),
                        '市值(亿元)': round(market_cap / 100000000, 2),
                        '2日涨跌幅(%)': round(price_change_2d, 2),
                        '当日涨幅(%)': round(daily_change, 2),
                        '振幅(%)': round(amplitude, 2),
                        '量比': round(volume_ratio, 2),
                        '换手率(%)': round(turnover_rate, 2),
                        '周成交量环比增长(%)': round(technicals['weekly_volume_growth'], 2)
                    }
                    screened_stocks.append(stock_info)
                    
            except Exception as e:
                # 跳过有错误的股票
                continue
        
        # 转换为DataFrame
        if screened_stocks:
            result_df = pd.DataFrame(screened_stocks)
            
            # 按周成交量环比增长从大到小排序
            result_df = result_df.sort_values('周成交量环比增长(%)', ascending=False)
            
            return result_df
        else:
            return pd.DataFrame()
    
    def screen_by_conditions(self, market_type="沪深a股", exclude_types=None, 
                           roe_min=-20, roe_max=15, current_ratio_min=0.4,
                           market_cap_max=100, price_change_2d_max=5,
                           daily_change_max=3, amplitude_max=6,
                           volume_ratio_min=0.8, turnover_min=1, turnover_max=10):
        """按条件筛选股票"""
        
        conditions = {
            'market_type': market_type,
            'exclude_types': exclude_types or ['ST', '创业', '科创', '北交所'],
            'roe_range': (roe_min, roe_max),
            'current_ratio_min': current_ratio_min,
            'market_cap_max': market_cap_max,  # 亿元
            'price_change_2d_max': price_change_2d_max,  # %
            'daily_change_max': daily_change_max,  # %
            'amplitude_max': amplitude_max,  # %
            'volume_ratio_min': volume_ratio_min,
            'turnover_range': (turnover_min, turnover_max)  # %
        }
        
        return self.screen_stocks(conditions)
    
    def format_results(self, df, limit=20):
        """格式化筛选结果"""
        if df.empty:
            return "❌ 没有找到符合条件的股票"
        
        result_lines = []
        result_lines.append(f"✅ 找到 {len(df)} 只符合条件的股票")
        result_lines.append("=" * 80)
        result_lines.append("排名 | 代码     | 名称       | 最新价 | 涨跌幅% | 市值(亿) | 周成交量增长%")
        result_lines.append("-" * 80)
        
        for idx, row in df.head(limit).iterrows():
            rank = idx + 1
            code = row['代码']
            name = row['名称'][:6] if len(row['名称']) > 6 else row['名称']
            price = f"{row['最新价']:.2f}"
            change = f"{row['涨跌幅']:.2f}"
            market_cap = f"{row['市值(亿元)']:.1f}"
            volume_growth = f"{row['周成交量环比增长(%)']:.1f}"
            
            result_lines.append(f"{rank:4d} | {code:8s} | {name:10s} | {price:>7s} | {change:>7s} | {market_cap:>9s} | {volume_growth:>12s}")
        
        # 添加关键指标统计
        result_lines.append("\n📊 关键指标统计:")
        result_lines.append(f"  • 平均市值: {df['市值(亿元)'].mean():.1f} 亿元")
        result_lines.append(f"  • 平均ROE: {df['ROE'].mean():.1f}%")
        result_lines.append(f"  • 平均换手率: {df['换手率(%)'].mean():.1f}%")
        result_lines.append(f"  • 最高周成交量增长: {df['周成交量环比增长(%)'].max():.1f}%")
        
        return "\n".join(result_lines)

# 测试代码
if __name__ == "__main__":
    screener = StockScreener()
    
    print("🔍 执行选股策略...")
    print("条件: 沪深A股，非ST/创业/科创/北交所")
    print("     ROE: -20% ~ 15%，流动比率≥0.4，市值<100亿")
    print("     2日涨跌幅<5%且涨幅<3%，振幅<6%")
    print("     量比>0.8，换手率1%~10%")
    print("     按周成交量环比增长排序")
    print("-" * 80)
    
    results = screener.screen_by_conditions()
    
    if not results.empty:
        print(screener.format_results(results))
        
        # 保存结果
        output_file = os.path.join(screener.cache_dir, "screening_results.csv")
        results.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\n💾 结果已保存到: {output_file}")
    else:
        print("❌ 没有找到符合条件的股票")