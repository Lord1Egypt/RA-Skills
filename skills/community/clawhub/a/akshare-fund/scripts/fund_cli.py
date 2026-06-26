#!/usr/bin/env python3
"""
基金量化工具 - 基于AkShare真实接口
"""
import argparse
import json
import sys
from datetime import datetime, timedelta

try:
    import akshare as ak
    import pandas as pd
except ImportError:
    print("请先安装: pip install akshare pandas")
    sys.exit(1)


def get_fund_list(fund_type=""):
    """获取基金列表"""
    df = ak.fund_name_em()
    if fund_type:
        df = df[df['基金类型'].str.contains(fund_type, na=False)]
    return df.head(50)


def get_fund_info(fund_code):
    """基金基本信息"""
    # 从基金列表中查找
    df = ak.fund_name_em()
    df_filtered = df[df['基金代码'] == fund_code]
    return df_filtered


def get_fund_holdings(fund_code, year=None):
    """基金持仓股票"""
    if year is None:
        year = "2025"  # 默认2025年
    df = ak.fund_portfolio_hold_em(symbol=fund_code, date=year)
    return df


def is_trading_time():
    """判断当前是否在交易时间"""
    now = datetime.now()
    weekday = now.weekday()
    
    # 周末不是交易日
    if weekday >= 5:
        return False
    
    # A股交易时间: 9:30-15:00 (周一至周五)
    hour = now.hour
    minute = now.minute
    current_time = hour * 60 + minute
    
    trading_start = 9 * 60 + 30   # 9:30
    trading_end = 15 * 60         # 15:00
    
    if trading_start <= current_time <= trading_end:
        return True
    return False


def get_fund_valuation():
    """基金净值估算"""
    df = ak.fund_value_estimation_em()
    return df


def get_official_valuation(fund_code):
    """获取官方估值"""
    df = ak.fund_value_estimation_em()
    df_filtered = df[df['基金代码'] == fund_code]
    return df_filtered


def calc_fund_summary(fund_codes, year=None):
    """汇总多个基金的持仓，计算股票占比排行"""
    if year is None:
        year = "2025"
    
    trading = is_trading_time()
    
    print(f"\n{'='*80}")
    print(f"基金列表: {', '.join(fund_codes)}")
    print(f"交易状态: {'交易中' if trading else '非交易时间'}")
    print(f"{'='*80}")
    
    all_holdings = []
    
    # 获取实时股票行情
    df_stocks = None
    if trading:
        try:
            df_stocks = ak.stock_zh_a_spot_em()
        except:
            print("获取实时行情失败，将不显示涨跌幅")
    
    for fund_code in fund_codes:
        try:
            df_hold = ak.fund_portfolio_hold_em(symbol=fund_code, date=year)
            if df_hold is None or df_hold.empty:
                print(f"基金 {fund_code} 无持仓数据")
                continue
            
            # 获取最新一期持仓
            cols = df_hold.columns.tolist()
            date_col = [c for c in cols if '日期' in c][0] if any('日期' in c for c in cols) else cols[-1]
            latest_date = df_hold[date_col].iloc[0]
            df_hold = df_hold[df_hold[date_col] == latest_date].copy()
            
            # 获取列名
            code_col = [c for c in cols if '代码' in c][0]
            name_col = [c for c in cols if '名称' in c][0]
            ratio_col = [c for c in cols if '比例' in c][0]
            
            # 转换数值
            df_hold[ratio_col] = pd.to_numeric(df_hold[ratio_col], errors='coerce')
            
            # 合并实时行情
            if df_stocks is not None:
                df_hold = df_hold.merge(df_stocks, left_on=code_col, right_on='代码', how='left')
            
            for _, row in df_hold.iterrows():
                change = 0
                price = 0
                if df_stocks is not None and '涨跌幅' in row:
                    try:
                        change = float(row['涨跌幅']) if pd.notna(row['涨跌幅']) else 0
                        price = float(row['最新价']) if pd.notna(row['最新价']) else 0
                    except:
                        pass
                
                all_holdings.append({
                    '股票代码': row[code_col],
                    '股票名称': row[name_col],
                    '占净值比例': row[ratio_col],
                    '最新价': price,
                    '涨跌幅': change,
                    '基金代码': fund_code
                })
                
        except Exception as e:
            print(f"基金 {fund_code} 获取失败: {e}")
    
    if not all_holdings:
        print("无持仓数据")
        return
    
    # 汇总
    df_all = pd.DataFrame(all_holdings)
    
    # 按股票代码汇总
    df_summary = df_all.groupby(['股票代码', '股票名称']).agg({
        '占净值比例': 'sum',
        '最新价': 'first',
        '涨跌幅': 'mean',
        '基金代码': 'count'
    }).reset_index()
    df_summary.columns = ['股票代码', '股票名称', '总占比', '最新价', '平均涨跌', '出现次数']
    df_summary = df_summary.sort_values('总占比', ascending=False)
    
    print(f"\n【持仓股票汇总排行】(前20)")
    print("-" * 80)
    print(f"{'代码':<8} {'名称':<10} {'总占比':>8} {'最新价':>8} {'涨跌':>8} {'次数':>4}")
    print("-" * 80)
    for _, row in df_summary.head(20).iterrows():
        price = f"{row['最新价']:.2f}" if row['最新价'] else "---"
        change = f"{row['平均涨跌']:+.2f}%" if row['平均涨跌'] else "---"
        print(f"{row['股票代码']:<8} {row['股票名称']:<10} {row['总占比']:>6.2f}% {price:>8} {change:>8} {row['出现次数']:>4}")
    
    print(f"\n共涉及 {len(df_summary)} 只股票")
    
    return df_summary


def calc_fund_estimate(fund_code, year=None):
    """根据持仓股票实时行情计算基金估值"""
    if year is None:
        year = "2025"  # 默认使用2025年
    
    trading = is_trading_time()
    
    print(f"\n{'='*70}")
    print(f"基金代码: {fund_code}")
    print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"交易状态: {'交易中' if trading else '非交易时间'}")
    print(f"{'='*70}")
    
    # 获取官方估值（总是尝试）
    official_data = None
    try:
        df_official = get_official_valuation(fund_code)
        if not df_official.empty:
            cols = df_official.columns.tolist()
            est_col = [c for c in cols if '估算' in c and '值' in c]
            change_col = [c for c in cols if '估算' in c and '增长' in c]
            nav_col = [c for c in cols if '单位净值' in c]
            
            if est_col:
                official_data = {
                    'estimate_nav': float(df_official.iloc[0][est_col[0]]),
                    'estimate_change': float(df_official.iloc[0][change_col[0]].replace('%', '')) if change_col else 0,
                    'unit_nav': float(df_official.iloc[0][nav_col[0]]) if nav_col else None
                }
    except Exception as e:
        print(f"获取官方估值失败: {e}")
    
    # 获取自定义估值（需要网络）
    custom_data = None
    try:
        # 1. 获取基金持仓
        df_hold = ak.fund_portfolio_hold_em(symbol=fund_code, date=year)
        if df_hold is None or df_hold.empty:
            print(f"未找到 {fund_code} 的持仓数据")
            return
        
        # 获取最新一期持仓
        cols = df_hold.columns.tolist()
        date_col = [c for c in cols if '日期' in c][0] if any('日期' in c for c in cols) else cols[-1]
        latest_date = df_hold[date_col].iloc[0]
        df_hold = df_hold[df_hold[date_col] == latest_date].copy()
        
        # 2. 获取实时股票行情
        df_stocks = ak.stock_zh_a_spot_em()
        
        # 3. 合并数据计算估值
        code_col = [c for c in cols if '代码' in c][0]
        ratio_col = [c for c in cols if '比例' in c][0]
        
        df_hold = df_hold.merge(df_stocks, left_on=code_col, right_on='代码', how='left')
        
        # 转换数值类型
        df_hold[ratio_col] = pd.to_numeric(df_hold[ratio_col], errors='coerce')
        df_hold['最新价'] = pd.to_numeric(df_hold['最新价'], errors='coerce')
        
        # 计算每只股票的估算贡献
        df_hold['估算涨跌幅'] = df_hold[ratio_col] * df_hold['涨跌幅'] / 100
        estimate_change = df_hold['估算涨跌幅'].sum()
        
        # 获取基金最新净值
        try:
            df_nav = ak.fund_etf_hist_em(symbol=fund_code, period="daily", 
                                          start_date="20200101", end_date=datetime.now().strftime('%Y%m%d'))
            if not df_nav.empty:
                latest_nav = df_nav.iloc[-1]['收盘']
            else:
                latest_nav = 1.0
        except:
            latest_nav = 1.0
        
        estimate_nav = latest_nav * (1 + estimate_change / 100)
        
        custom_data = {
            'estimate_nav': estimate_nav,
            'estimate_change': estimate_change,
            'latest_nav': latest_nav,
            'holdings': df_hold,
            'cols': cols
        }
        
    except Exception as e:
        print(f"获取自定义估值失败: {e}")
    
    # 显示结果
    print(f"\n【估值结果】")
    print("-" * 70)
    
    # 官方估值
    if official_data:
        print(f"【官方估值】")
        print(f"  估算净值: {official_data['estimate_nav']:.4f}")
        print(f"  估算涨跌: {official_data['estimate_change']:+.2f}%")
        if official_data.get('unit_nav'):
            print(f"  单位净值: {official_data['unit_nav']:.4f}")
    else:
        print(f"【官方估值】: 获取失败")
    
    print()
    
    # 自定义估值
    if custom_data:
        print(f"【自定义估值】(根据持仓股实时计算)")
        print(f"  最新净值: {custom_data['latest_nav']:.4f}")
        print(f"  估算净值: {custom_data['estimate_nav']:.4f}")
        print(f"  估算涨跌: {custom_data['estimate_change']:+.2f}%")
        
        # 持仓明细
        name_col = [c for c in custom_data['cols'] if '名称' in c][0]
        code_col = [c for c in custom_data['cols'] if '代码' in c][0]
        ratio_col = [c for c in custom_data['cols'] if '比例' in c][0]
        
        print(f"\n【持仓股票明细 TOP10】")
        for _, row in custom_data['holdings'].head(10).iterrows():
            print(f"  {row[code_col]:8s} {row[name_col]:10s} 占比: {row[ratio_col]:5.2f}% 涨跌: {row['涨跌幅']:+.2f}%")
    else:
        print(f"【自定义估值】: 获取失败")
    
    print("-" * 70)
    
    # 根据交易时间给出建议
    if trading:
        print(f"\n当前为交易时间，建议使用【自定义估值】（基于持仓股实时行情）")
    else:
        print(f"\n当前为非交易时间，两种估值均可参考")
    
    return {
        'fund_code': fund_code,
        'official': official_data,
        'custom': custom_data
    }


def get_fund_nav(fund_code, year=None):
    """基金净值（区分交易时间）"""
    trading = is_trading_time()
    
    print(f"\n{'='*70}")
    print(f"基金代码: {fund_code}")
    print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"交易状态: {'交易中' if trading else '非交易时间'}")
    print(f"{'='*70}")
    
    # 非交易时间：显示历史净值
    if not trading:
        try:
            end_date = datetime.now().strftime('%Y%m%d')
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
            df = ak.fund_etf_hist_em(symbol=fund_code, period="daily", 
                                       start_date=start_date, end_date=end_date)
            print(f"\n【历史净值】")
            print(df.tail(10).to_string(index=False))
            return df
        except Exception as e:
            print(f"获取历史净值失败: {e}")
    
    # 交易时间：显示实时估算净值
    if year is None:
        year = "2025"
    
    try:
        # 获取基金持仓
        df_hold = ak.fund_portfolio_hold_em(symbol=fund_code, date=year)
        if df_hold is None or df_hold.empty:
            print(f"未找到持仓数据")
            return
        
        # 获取最新一期持仓
        cols = df_hold.columns.tolist()
        date_col = [c for c in cols if '日期' in c][0] if any('日期' in c for c in cols) else cols[-1]
        latest_date = df_hold[date_col].iloc[0]
        df_hold = df_hold[df_hold[date_col] == latest_date].copy()
        
        # 获取实时股票行情
        df_stocks = ak.stock_zh_a_spot_em()
        
        # 合并计算
        code_col = [c for c in cols if '代码' in c][0]
        ratio_col = [c for c in cols if '比例' in c][0]
        
        df_hold = df_hold.merge(df_stocks, left_on=code_col, right_on='代码', how='left')
        df_hold[ratio_col] = pd.to_numeric(df_hold[ratio_col], errors='coerce')
        df_hold['最新价'] = pd.to_numeric(df_hold['最新价'], errors='coerce')
        
        # 计算实时净值
        df_hold['涨跌幅'] = pd.to_numeric(df_hold['涨跌幅'], errors='coerce')
        df_hold['涨跌幅'] = df_hold['涨跌幅'].fillna(0)
        df_hold['持仓贡献'] = df_hold[ratio_col] * df_hold['涨跌幅'] / 100
        total_change = df_hold['持仓贡献'].sum()
        
        # 获取昨日净值
        try:
            df_hist = ak.fund_etf_hist_em(symbol=fund_code, period="daily", 
                                           start_date="20200101", end_date=datetime.now().strftime('%Y%m%d'))
            if not df_hist.empty:
                last_nav = df_hist.iloc[-1]['收盘']
            else:
                last_nav = 1.0
        except:
            last_nav = 1.0
        
        # 实时净值 = 昨日净值 * (1 + 涨跌幅/100)
        realtime_nav = last_nav * (1 + total_change / 100)
        
        print(f"\n【实时净值估算】")
        print(f"  昨日净值: {last_nav:.4f}")
        print(f"  实时净值: {realtime_nav:.4f}")
        print(f"  估算涨跌: {total_change:+.2f}%")
        
        # 持仓明细
        name_col = [c for c in cols if '名称' in c][0]
        print(f"\n【持仓股票明细 TOP10】")
        for _, row in df_hold.head(10).iterrows():
            print(f"  {row[code_col]:8s} {row[name_col]:10s} 占比: {row[ratio_col]:5.2f}% 涨跌: {row['涨跌幅']:+.2f}%")
        
        return {
            'fund_code': fund_code,
            'last_nav': last_nav,
            'realtime_nav': realtime_nav,
            'change': total_change
        }
        
    except Exception as e:
        print(f"计算实时净值失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    parser = argparse.ArgumentParser(description='基金量化工具')
    parser.add_argument('action', choices=['list', 'info', 'holdings', 'valuation', 'nav', 'estimate', 'summary'],
                        help='操作类型')
    parser.add_argument('--list', nargs='+', help='基金代码列表')
    parser.add_argument('--type', default='', help='基金类型')
    parser.add_argument('--year', help='年份')
    parser.add_argument('--days', type=int, default=30)
    
    args = parser.parse_args()
    
    try:
        if args.action == 'list':
            df = get_fund_list(args.type)
            print(df.to_string())
            
        elif args.action == 'info':
            if not args.list:
                print("错误: 需要 --list 参数")
                sys.exit(1)
            for code in args.list:
                df = get_fund_info(code)
                print(f"\n【{code}】")
                print(df.to_string())
            
        elif args.action == 'holdings':
            if not args.list:
                print("错误: 需要 --list 参数")
                sys.exit(1)
            df = get_fund_holdings(args.list[0], args.year)
            print(df.to_string())
            
        elif args.action == 'valuation':
            df = get_fund_valuation()
            print(df.head(20).to_string())
            
        elif args.action == 'nav':
            if not args.list:
                print("错误: 需要 --list 参数")
                sys.exit(1)
            result = get_fund_nav(args.list[0], args.year)
            
        elif args.action == 'estimate':
            if not args.list:
                print("错误: 需要 --list 参数")
                sys.exit(1)
            calc_fund_estimate(args.list[0], args.year)
            
        elif args.action == 'summary':
            if not args.list:
                print("错误: 需要 --list 参数")
                sys.exit(1)
            calc_fund_summary(args.list, args.year)
            
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
