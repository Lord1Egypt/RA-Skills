#!/usr/bin/env python3
"""
BaoStock 测试脚本 - 分析股票日K线走势和财务基本面
"""
import baostock as bs
import pandas as pd
from datetime import datetime, timedelta

# 登录系统
print("=" * 60)
print("BaoStock 金融数据测试")
print("=" * 60)

lg = bs.login()
print(f'登录返回: error_code={lg.error_code}, error_msg={lg.error_msg}')

# ============ 1. 获取日K线数据 ============
print("\n" + "=" * 60)
print("一、日K线走势分析 (最近30个交易日)")
print("=" * 60)

# 获取最近30个交易日的数据
end_date = datetime.now().strftime('%Y-%m-%d')
start_date = (datetime.now() - timedelta(days=45)).strftime('%Y-%m-%d')

rs = bs.query_history_k_data_plus(
    "sh.600000",  # 浦发银行
    "date,code,open,high,low,close,volume,amount,pctChg,turn",
    start_date=start_date,
    end_date=end_date,
    frequency="d",
    adjustflag="3"
)

data_list = []
while (rs.error_code == '0') & rs.next():
    data_list.append(rs.get_row_data())

df = pd.DataFrame(data_list, columns=rs.fields)

# 转换为数值类型
for col in ['open', 'high', 'low', 'close', 'volume', 'pctChg', 'turn']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# 显示最近30个交易日
print(f"\n股票代码: {df['code'].iloc[0]}")
print(f"数据范围: {df['date'].iloc[0]} 至 {df['date'].iloc[-1]}")
print(f"\n最近30个交易日K线数据:")
print(df.tail(30).to_string(index=False))

# 计算技术指标
print("\n--- 技术指标分析 ---")
latest = df.iloc[-1]
prev = df.iloc[-2] if len(df) > 1 else latest

# 涨跌幅
pct_change = latest['pctChg']
print(f"最新收盘价: {latest['close']:.2f}")
print(f"涨跌幅: {pct_change:+.2f}%")

# 成交量变化
vol_change = ((latest['volume'] - prev['volume']) / prev['volume'] * 100) if prev['volume'] > 0 else 0
print(f"成交量: {latest['volume']:,.0f} (较昨日 {vol_change:+.1f}%)")

# 5日/10日均线
if len(df) >= 5:
    ma5 = df['close'].tail(5).mean()
    print(f"5日均线: {ma5:.2f}")
if len(df) >= 10:
    ma10 = df['close'].tail(10).mean()
    print(f"10日均线: {ma10:.2f}")

# 最高/最低
print(f"30日最高: {df['high'].max():.2f}")
print(f"30日最低: {df['low'].min():.2f}")

# ============ 2. 获取财务基本面 ============
print("\n" + "=" * 60)
print("二、财务基本面分析 (最新季度)")
print("=" * 60)

# 获取最新季度财务数据
current_year = datetime.now().year
current_quarter = (datetime.now().month - 1) // 3
if current_quarter == 0:
    current_quarter = 4
    current_year -= 1

print(f"\n查询年份: {current_year}年第{current_quarter}季")

# 盈利能力
print("\---盈利能力---")
rs = bs.query_profit_data(code="sh.600000", year=current_year, quarter=current_quarter)
while rs.next():
    row = rs.get_row_data()
    print(f"净资产收益率(ROE): {row[3]}%")
    print(f"销售净利率: {row[4]}%")
    print(f"销售毛利率: {row[5]}%")
    print(f"净利润: {row[6]}元")
    print(f"每股收益TTM: {row[7]}")

# 成长能力
print("\n---成长能力---")
rs = bs.query_growth_data(code="sh.600000", year=current_year, quarter=current_quarter)
while rs.next():
    row = rs.get_row_data()
    print(f"净资产同比增长率: {row[3]}%")
    print(f"净利润同比增长率: {row[5]}%")
    print(f"基本每股收益同比增长率: {row[6]}%")

# 偿债能力
print("\n---偿债能力---")
rs = bs.query_balance_data(code="sh.600000", year=current_year, quarter=current_quarter)
while rs.next():
    row = rs.get_row_data()
    print(f"流动比率: {row[3]}")
    print(f"速动比率: {row[4]}")
    print(f"现金比率: {row[5]}")
    print(f"资产负债率: {row[8]}%")

# 营运能力
print("\n---营运能力---")
rs = bs.query_operation_data(code="sh.600000", year=current_year, quarter=current_quarter)
while rs.next():
    row = rs.get_row_data()
    print(f"总资产周转率: {row[7]}")

# ============ 3. 证券基本信息 ============
print("\n" + "=" * 60)
print("三、证券基本信息")
print("=" * 60)

rs = bs.query_stock_basic(code="sh.600000")
while rs.next():
    row = rs.get_row_data()
    print(f"证券代码: {row[0]}")
    print(f"证券名称: {row[1]}")
    print(f"上市日期: {row[2]}")
    print(f"退市日期: {row[3]}")
    print(f"证券类型: {row[4]} (1=股票, 2=指数)")
    print(f"上市状态: {row[5]} (1=上市, 0=退市)")

# 登出系统
bs.logout()
print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
