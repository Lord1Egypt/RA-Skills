# # 通达信TQ策略介绍和应用示例

以下是 20250122通达信趋势财经公众号发布文章

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAPCAYAAAA71pVKAAAABmJLR0QA/wD/AP+gvaeTAAAAEUlEQVQokWNgGAWjYBQMIgAAA5MAAdmyLDcAAAAASUVORK5CYII=)

(opens new window) 涉及的策略py文件；
 发送序列数据的TQMA510技术指标在stratexldata.py 下面的注释中。

### # fiststrategy.py

```python
import numpy as np
import pandas as pd
from tqcenter import tq
import time
import json
import os
# 将工作目录切换到当前脚本文件所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# 之后，相对路径就会基于脚本所在目录进行解析


"""
    这里是tq的简单使用示例
    使用时请确保已经启动通达信客户端并登录
    取消对应注释即可运行对应功能
"""

"""
    参数设置
"""
codes = ["688318.SH"] #传入的股票代码格式必须是标准格式：6位数+市场后缀（.SH/.SZ/.JJ等）
startime = "20250620" #传入的时间格式必须是：YYYYMMDD 或 YYYYMMDDHHMMSS
endtime = "20250801"
period = '1d' #K线周期：1d/1w/1m/5m/15m/30m/60m等
dividend_type='none' #复权类型：none-不复权，front-前复权，back-后复权

#初始化
tq.initialize(__file__) #所有策略连接通达信客户端都必须调用此函数进行初始化

'''
    刷新行情缓存 刷新后5分钟内取最新report和k线数据不会触发刷新
'''
# refresh_cache = tq.refresh_cache()
# print(refresh_cache)

'''
    缓存历史K线 目前仅支持1m 5m 1d三种类型数据 不建议一次更新太多，会堵塞策略和客户端
'''
# refresh_kline = tq.refresh_kline(stock_list=['688318.SH'],period='1d')
# print(refresh_kline)

'''
    获取K线数据  获取K线数据需要先在客户端中下载对应盘后数据，调用会触发客户端刷新数据，耗时过长请耐心等待
    field_list可以筛选返回字段，默认返回全部字段 比如 field_list=['Open','Close'] 就是只取开盘价和收盘价
    count可以设置每只股票取的数据量
    暂时不支持获取分笔数据
    开高低收单位为元，成交量单位为手，成交额单位为万元
'''
df = tq.get_market_data(
        field_list=[],
        stock_list=['600519.SH'],
        start_time='20251208',
        end_time='20251210',
        count=-1,
        dividend_type='none',
        period='1d',
        fill_data=False
    )
print(df)
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # strategywarn.py

```python
import numpy as np
import pandas as pd
from tqcenter import tq
import time
import json

"""
    这里是tq的简单使用示例
    使用时请确保已经启动通达信客户端并登录
    取消对应注释即可运行对应功能
"""

"""
    参数设置
"""
codes = ["688318.SH"] #传入的股票代码格式必须是标准格式：6位数+市场后缀（.SH/.SZ/.JJ等）
startime = "20250620" #传入的时间格式必须是：YYYYMMDD 或 YYYYMMDDHHMMSS
endtime = "20250801"
period = '1d' #K线周期：1d/1w/1m/5m/15m/30m/60m等
dividend_type='none' #复权类型：none-不复权，front-前复权，back-后复权

#初始化
tq.initialize(__file__) #所有策略连接通达信客户端都必须调用此函数进行初始化


'''
    发送预警信号给通达信客户端的TQ策略界面
    price_list close_list volum_list bs_flag_list warn_type_list 均要求为纯数字字符串List
    bs_flag_list 0买1卖2未知
    reason_list每个元素有效长度为25个汉字（50个英文）
'''
warn_res = tq.send_warn(stock_list = ['688318.SH','688318.SH','600519.SH','600519.SH'],
             time_list = ['20251215141115','20251215142100','20251215143101','20251215145001'],
             price_list= ['123.45','133.45','1823.45','1853.45'],
             close_list= ['122.50','132.50','1822.50','1822.50'],
             volum_list= ['1000','2000','15000','15000'],
             bs_flag_list= ['0','','2','1'],
             warn_type_list= ['0','','2','1'],
             reason_list= ['价格突破预警线','收盘价突破预警线','成交量突破预警线','价格下破预警线'],
             count=4)
print(warn_res)
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # TQHuiCe.py

```python
import numpy as np
import pandas as pd
from tqcenter import tq
import time
import json
"""
    这里是tq的简单使用示例
    使用时请确保已经启动通达信客户端并登录
    取消对应注释即可运行对应功能
"""
#初始化
tq.initialize(__file__) #所有策略连接通达信客户端都必须调用此函数进行初始化
bt_data = tq.send_bt_data(stock_code = '688318.SH',
                          time_list = ['20260120141100','20260120141400'],
                          data_list = [['1','143.41','200','0','0','0'],['0','0','0','1','143.48','200']],
                          count = 2)
print(bt_data)
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # stratexldata.py

```python
#展示每日持仓量能看数据 验证开仓和手续费的   #用悬挂目录的时候  读不出来
from tqcenter import tq
import pandas as pd
import numpy as np
import math
from datetime import datetime
import sys


# ==================== 技术指标计算函数 ====================
def calculate_ema(series, window):
    """计算指数移动平均"""
    return series.ewm(span=window, adjust=False).mean()

def calculate_sma(series, window):
    """计算简单移动平均"""
    return series.rolling(window=window).mean()

def calculate_llv(series, window):
    """计算周期内最低值"""
    return series.rolling(window=window).min()

def calculate_hhv(series, window):
    """计算周期内最高值"""
    return series.rolling(window=window).max()

def calculate_ma(series, window):
    """计算简单移动平均 (别名，与calculate_sma功能相同)"""
    return calculate_sma(series, window)

def ref(series, periods):
    """引用若干周期前的数据"""
    return series.shift(periods)

def calculate_cross_signal(fast_series, slow_series):
    """
    计算金叉信号序列。
    规则：当快线从下方上穿慢线时，标记为1（金叉），否则为0。
    注意：这是一个简单的信号，未考虑信号持续期。
    """
    # 判断条件：今日快线 > 慢线，且昨日快线 <= 慢线
    cross_up = (fast_series > slow_series) & (ref(fast_series, 1) <= ref(slow_series, 1))
    return cross_up.astype(int)

def get_benchmark_data(benchmark_code='000300.SH', count=60):
    """
    获取基准品种数据
    """
    try:
        # 获取基准市场数据
        benchmark_data = tq.get_market_data(
            field_list=['Open', 'High', 'Low', 'Close'],
            stock_list=[benchmark_code],
            period='1d',
            count=count,
            dividend_type='front'  # 前复权数据
        )

        # 提取收盘价序列
        benchmark_close = benchmark_data['Close'][benchmark_code]

        # 计算基准收益率序列
        benchmark_returns = benchmark_close.pct_change().fillna(0)

        # 计算基准净值（从1开始）
        benchmark_net_value = (1 + benchmark_returns).cumprod()

        # 计算基准年化收益率
        trading_days = len(benchmark_net_value)
        if trading_days > 0:
            benchmark_total_return = benchmark_net_value.iloc[-1] - 1
            benchmark_annual_return = (1 + benchmark_total_return) ** (252 / trading_days) - 1
        else:
            benchmark_total_return = 0
            benchmark_annual_return = 0

        return {
            'close': benchmark_close,
            'returns': benchmark_returns,
            'net_value': benchmark_net_value,
            'total_return': benchmark_total_return,
            'annual_return': benchmark_annual_return
        }

    except Exception as e:
        print(f"获取基准数据时发生错误: {e}")
        # 返回空数据
        return {
            'close': pd.Series(),
            'returns': pd.Series(),
            'net_value': pd.Series(),
            'total_return': 0,
            'annual_return': 0
        }

def calculate_daily_statistics(df, benchmark_data, initial_capital=100000, fee_rate=0.0003):
    """
    计算每日的回测统计指标序列
    输入：
        df: 包含价格数据、买卖信号的DataFrame
        benchmark_data: 基准数据字典
        initial_capital: 初始资金
        fee_rate: 手续费率（双边）
    输出：包含每日统计指标的DataFrame
    """
    # 初始化变量
    capital = initial_capital
    position = 0  # 持仓数量
    rest_cash = capital  # 剩余现金
    hold = False  # 是否持仓

    # 创建结果列表
    daily_stats = []
    open_count = 0  # 累计开仓次数
    close_count = 0  # 累计平仓次数
    win_count = 0  # 累计盈利交易次数
    trade_records = []  # 交易记录

    # 获取基准数据
    benchmark_close = benchmark_data['close']
    benchmark_net_value = benchmark_data['net_value']

    # 确保基准数据与策略数据时间对齐
    if len(benchmark_close) != len(df):
        print(f"警告：基准数据长度({len(benchmark_close)})与策略数据长度({len(df)})不一致")
        # 这里简单处理，取相同长度的数据
        min_len = min(len(benchmark_close), len(df))
        benchmark_close = benchmark_close.iloc[:min_len]
        benchmark_net_value = benchmark_net_value.iloc[:min_len]
        df = df.iloc[:min_len]

    # 遍历数据执行交易
    for i in range(len(df)):
        current_price = df['close'].iloc[i]
        buy_signal = df['buyxh'].iloc[i] if i < len(df) else 0
        sell_signal = df['sellxh'].iloc[i] if i < len(df) else 0

        # 记录交易前的状态
        pre_open_count = open_count
        pre_close_count = close_count
        pre_win_count = win_count

        # 金叉买入信号
        if buy_signal == 1 and not hold:
            # 计算可买整百股数量
            max_shares = int(rest_cash / current_price / 100) * 100
            if max_shares > 0:
                # 计算手续费
                trade_amount = max_shares * current_price
                fee = trade_amount * fee_rate

                # 执行买入
                position = max_shares
                rest_cash = rest_cash - trade_amount - fee
                hold = True
                open_count += 1

                # 记录交易
                trade_records.append({
                    'date': df.index[i],
                    'type': 'buy',
                    'price': current_price,
                    'shares': position,
                    'fee': fee
                })

        # 死叉卖出信号
        elif sell_signal == 1 and hold:
            # 计算卖出金额
            trade_amount = position * current_price
            fee = trade_amount * fee_rate

            # 执行卖出
            rest_cash = rest_cash + trade_amount - fee
            position = 0
            hold = False
            close_count += 1

            # 检查交易是否盈利
            if len(trade_records) > 0 and trade_records[-1]['type'] == 'buy':
                buy_price = trade_records[-1]['price']
                if current_price > buy_price:
                    win_count += 1

            # 记录交易
            trade_records.append({
                'date': df.index[i],
                'type': 'sell',
                'price': current_price,
                'shares': position,
                'fee': fee
            })

        # 计算当日市值和净值
        if hold:
            daily_value = rest_cash + position * current_price
        else:
            daily_value = rest_cash

        daily_net_value = daily_value / initial_capital

        # 计算胜率（到当前日期为止）
        total_trades_to_date = open_count + close_count
        win_rate_to_date = (win_count / total_trades_to_date * 100) if total_trades_to_date > 0 else 0

        # 计算年化收益率（到当前日期为止）
        if i > 0:
            total_return_to_date = daily_net_value - 1
            trading_days_to_date = i + 1
            annual_return_to_date = (1 + total_return_to_date) ** (252 / trading_days_to_date) - 1 if trading_days_to_date > 0 else 0
        else:
            annual_return_to_date = 0

        # 获取基准净值（使用真实的基准数据）
        if i < len(benchmark_net_value):
            current_benchmark_net_value = benchmark_net_value.iloc[i]
        else:
            current_benchmark_net_value = 1.0

        # 计算基准年化收益率（到当前日期为止）
        if i > 0 and i < len(benchmark_net_value):
            benchmark_total_return_to_date = current_benchmark_net_value - 1
            benchmark_annual_return_to_date = (1 + benchmark_total_return_to_date) ** (252 / (i + 1)) - 1 if i > 0 else 0
        else:
            benchmark_annual_return_to_date = 0

        # 计算贝塔值（到当前日期为止）
        if i > 1:
            # 计算策略收益率序列
            strategy_returns = []
            for j in range(i + 1):
                if j == 0:
                    strategy_returns.append(0)
                else:
                    prev_capital = daily_stats[j-1]['capital'] if j > 0 else initial_capital
                    curr_capital = daily_value if j == i else daily_stats[j]['capital']
                    strategy_return = (curr_capital / prev_capital) - 1
                    strategy_returns.append(strategy_return)

            # 计算基准收益率序列
            benchmark_returns_to_date = benchmark_close.iloc[:i+1].pct_change().fillna(0).values

            # 计算协方差和方差
            if len(strategy_returns) > 1 and len(benchmark_returns_to_date) > 1:
                cov_matrix = np.cov(strategy_returns, benchmark_returns_to_date)
                beta = cov_matrix[0, 1] / cov_matrix[1, 1] if cov_matrix[1, 1] != 0 else 1.0
            else:
                beta = 1.0
        else:
            beta = 1.0

        # 收集每日统计数据
        daily_stats.append({
            'date': df.index[i],
            'capital': daily_value,
            'net_value': daily_net_value,
            'open_count': open_count,
            'close_count': close_count,
            'win_rate': win_rate_to_date,
            'annual_return': annual_return_to_date * 100,
            'benchmark_net_value': current_benchmark_net_value,
            'benchmark_annual_return': benchmark_annual_return_to_date * 100,
            'beta': beta,
            'position': position,  # 持仓量
            'hold': hold
        })

    # 转换为DataFrame
    stats_df = pd.DataFrame(daily_stats)
    stats_df.set_index('date', inplace=True)

    # 计算最大回撤序列
    if len(stats_df) > 0:
        stats_df['rolling_max'] = stats_df['net_value'].cummax()
        stats_df['drawdown'] = (stats_df['net_value'] - stats_df['rolling_max']) / stats_df['rolling_max']
        stats_df['max_drawdown'] = stats_df['drawdown'].cummin()

    # 计算夏普比率序列
    if len(stats_df) > 1:
        # 计算策略收益率
        returns_list = []
        for i in range(len(stats_df)):
            if i == 0:
                returns_list.append(0)
            else:
                prev_capital = stats_df['capital'].iloc[i-1]
                curr_capital = stats_df['capital'].iloc[i]
                returns_list.append((curr_capital / prev_capital) - 1)

        stats_df['returns'] = returns_list

        # 计算滚动夏普比率
        sharpe_list = []
        for i in range(len(stats_df)):
            if i == 0:
                sharpe_list.append(0)
            else:
                returns_to_date = stats_df['returns'].iloc[:i+1]
                # 使用2%作为无风险利率
                risk_free_rate = 0.02
                excess_returns = returns_to_date - risk_free_rate/252
                sharpe = excess_returns.mean() * math.sqrt(252) / returns_to_date.std() if returns_to_date.std() != 0 else 0
                sharpe_list.append(sharpe)
        stats_df['sharpe_ratio'] = sharpe_list

    return stats_df, trade_records

# ==================== 主程序 ====================
def main():
    # 初始化TQ
    tq.initialize(__file__)

    # 股票列表（示例）
    stocks = ['688800.SH', '688318.SH', '688981.SH']
    # 基准品种代码
    benchmark_code = '000300.SH'

    # 使用for循环遍历股票列表
    for stock_code in stocks:
        print(f"处理股票: {stock_code}")
        print("-" * 50)

        try:
            # 获取股票市场数据
            market_data = tq.get_market_data(
                field_list=['Open', 'High', 'Low', 'Close'],
                stock_list=[stock_code],
                period='1d',
                count=60,
                dividend_type='front'  # 前复权数据
            )

            # 构建DataFrame
            df = pd.DataFrame({
                'open': market_data['Open'][stock_code],
                'high': market_data['High'][stock_code],
                'low': market_data['Low'][stock_code],
                'close': market_data['Close'][stock_code]
            })

            print("原始K线数据前5行:")
            print(df.head())
            print("-" * 50)

            # 计算技术指标
            df['ma5'] = calculate_ma(df['close'], 5)
            df['ma10'] = calculate_ma(df['close'], 10)

            # 计算金叉信号
            df['buyxh'] = calculate_cross_signal(df['ma5'], df['ma10'])
            df['sellxh'] = calculate_cross_signal(df['ma10'], df['ma5'])

            print("添加技术指标与信号后的数据前15行:")
            print(df[['close', 'ma5', 'ma10', 'buyxh', 'sellxh']].head(15))
            print("-" * 50)

            # 获取基准数据
            print(f"获取基准品种 {benchmark_code} 数据...")
            benchmark_data = get_benchmark_data(benchmark_code, count=len(df))

            if len(benchmark_data['close']) == 0:
                print("警告：未能获取基准数据，使用简化计算")
                # 使用简化基准计算
                benchmark_close = df['close']
                benchmark_returns = benchmark_close.pct_change().fillna(0)
                benchmark_net_value = (1 + benchmark_returns).cumprod()
                benchmark_data = {
                    'close': benchmark_close,
                    'returns': benchmark_returns,
                    'net_value': benchmark_net_value,
                    'total_return': benchmark_net_value.iloc[-1] - 1 if len(benchmark_net_value) > 0 else 0,
                    'annual_return': 0
                }

            print(f"基准数据获取成功，共{len(benchmark_data['close'])}个交易日")
            print(f"基准总收益率: {benchmark_data['total_return']*100:.2f}%")
            print(f"基准年化收益率: {benchmark_data['annual_return']*100:.2f}%")
            print("-" * 50)

            # 计算每日回测统计指标序列
            stats_df, trade_records = calculate_daily_statistics(
                df,
                benchmark_data,
                initial_capital=100000,
                fee_rate=0.0003  # 0.03%手续费
            )

            # 输出最后一天的统计结果
            if len(stats_df) > 0:
                last_stats = stats_df.iloc[-1]
                print("最终回测统计指标:")
                print(f"开仓次数: {last_stats['open_count']}")
                print(f"平仓次数: {last_stats['close_count']}")
                print(f"单位净值: {last_stats['net_value']:.4f}")
                print(f"基准净值: {last_stats['benchmark_net_value']:.4f}")
                print(f"胜率: {last_stats['win_rate']:.2f}%")
                print(f"年化收益率: {last_stats['annual_return']:.2f}%")
                print(f"基准年化收益率: {last_stats['benchmark_annual_return']:.2f}%")
                print(f"贝塔值: {last_stats['beta']:.4f}")
                print(f"最大回撤: {last_stats['max_drawdown']*100:.2f}%")
                print(f"夏普比率: {last_stats['sharpe_ratio']:.4f}")
                print(f"持仓量: {last_stats['position']}股")
                print("-" * 50)

            # 准备发送给TQ的数据
            time_list = df.index.strftime('%Y%m%d').tolist()
            # print(time_list)
            # 扩展data_list，包含所有需要的指标（每日序列）
            data_list = []
            for i, (_, row) in enumerate(df.iterrows()):
                # 基础技术指标
                ma5_value = row['ma5'] if not pd.isna(row['ma5']) else 0.0
                ma10_value = row['ma10'] if not pd.isna(row['ma10']) else 0.0
                buyxh_value = row['buyxh'] if not pd.isna(row['buyxh']) else 0
                sellxh_value = row['sellxh'] if not pd.isna(row['sellxh']) else 0

                # 获取该日期的回测指标
                if i < len(stats_df):
                    daily_stats = stats_df.iloc[i]
                    open_count_val = daily_stats['open_count']
                    close_count_val = daily_stats['close_count']
                    net_value_val = daily_stats['net_value']
                    benchmark_net_val = daily_stats['benchmark_net_value']
                    win_rate_val = daily_stats['win_rate']
                    annual_return_val = daily_stats['annual_return']
                    benchmark_annual_val = daily_stats['benchmark_annual_return']
                    beta_val = daily_stats['beta']
                    max_drawdown_val = daily_stats['max_drawdown'] * 100  # 转换为百分比
                    sharpe_val = daily_stats['sharpe_ratio'] if 'sharpe_ratio' in daily_stats else 0
                    capital_val = daily_stats['capital']
                    position_val = daily_stats['position']  # 持仓量
                else:
                    # 默认值
                    open_count_val = 0
                    close_count_val = 0
                    net_value_val = 1.0
                    benchmark_net_val = 1.0
                    win_rate_val = 0
                    annual_return_val = 0
                    benchmark_annual_val = 0
                    beta_val = 1.0
                    max_drawdown_val = 0
                    sharpe_val = 0
                    capital_val = 100000
                    position_val = 0

                # 构建数据条目
                formatted_entry = [
                    f"{ma5_value:.2f}",                    # ID 1: MA5
                    f"{ma10_value:.2f}",                   # ID 2: MA10
                    str(int(buyxh_value)),                 # ID 3: 买入信号
                    str(int(sellxh_value)),                # ID 4: 卖出信号
                    f"{open_count_val}",                   # ID 5: 开仓次数（累计到当前日期）
                    f"{close_count_val}",                  # ID 6: 平仓次数（累计到当前日期）
                    f"{net_value_val:.4f}",                # ID 7: 单位净值（当前日期）
                    f"{benchmark_net_val:.4f}",            # ID 8: 基准净值（当前日期）
                    f"{win_rate_val:.2f}",                 # ID 9: 胜率（累计到当前日期）
                    f"{annual_return_val:.2f}",            # ID 10: 年化收益率（累计到当前日期）
                    f"{benchmark_annual_val:.2f}",         # ID 11: 基准年化收益率（累计到当前日期）
                    f"{beta_val:.4f}",                     # ID 12: 贝塔值
                    f"{max_drawdown_val:.2f}",             # ID 13: 最大回撤（累计到当前日期）
                    f"{sharpe_val:.4f}",                   # ID 14: 夏普比率（累计到当前日期）
                    f"{capital_val:.2f}",                  # ID 15: 每日资金
                    f"{position_val}"                      # ID 16: 持仓量（每日持仓数量）
                ]
                data_list.append(formatted_entry)

            print(f"准备发送的data_list (前5个周期，共{len(data_list)}个周期):")
            for i in range(min(5, len(data_list))):
                print(f"日期 {time_list[i]}: {data_list[i]}")
            print("-" * 50)

            # 发送回测数据到TQ
            bt_data = tq.send_bt_data(
                stock_code,
                time_list=time_list,
                data_list=data_list,
                count=60
            )
            print("发送回测数据结果:")
            print(bt_data)
            print("-" * 50)

            # 输出交易记录
            if trade_records:
                print("交易记录:")
                for record in trade_records:
                    print(f"{record['date']}: {record['type']} {record['shares']}股 @ {record['price']:.2f}, 手续费: {record['fee']:.2f}")

            print(f"股票 {stock_code} 处理完成！")
            print("=" * 60)

        except Exception as e:
            print(f"处理股票 {stock_code} 时发生错误: {e}")
            print("跳过该股票，继续处理下一个...")
            print("-" * 50)
            continue

    # 关闭TQ连接
    tq.close()
    print("所有股票处理完毕！")
    print("程序执行完毕。")

    # ==================== 通达信公式使用提示 ====================
    print("\n" + "="*60)
    print("通达信公式管理器中使用提示:")
    print("="*60)
    print("""
将数据发送到TQ策略界面后，您可以在通达信公式管理器中创建技术指标公式，
使用 SIGNALS_TQ(ID, TYPE) 函数来引用这些序列数据并在K线上展示。

例如，创建一个名为"TQMA510"的公式，代码可以如下：

MA5:SIGNALS_TQ(1,0);        {引用ID=1的数据(MA5)}
MA10:SIGNALS_TQ(2,0);       {引用ID=2的数据(MA10)}

{交易信号}
BUY_SIGNAL:=SIGNALS_TQ(3,0); {买入信号}
SELL_SIGNAL:=SIGNALS_TQ(4,0);{卖出信号}

{回测指标展示 - 这些指标会随着时间轴移动而动态变化}
开仓次数:SIGNALS_TQ(5,0),COLORRED;
平仓次数:SIGNALS_TQ(6,0),COLORGREEN;
单位净值:SIGNALS_TQ(7,0),COLORWHITE;
基准净值:SIGNALS_TQ(8,0),COLORYELLOW;
胜率:SIGNALS_TQ(9,0),COLORMAGENTA;
年化收益率:SIGNALS_TQ(10,0),COLORCYAN;
基准年化收益率:SIGNALS_TQ(11,0),COLORLIBLUE;
贝塔值:SIGNALS_TQ(12,0),COLORBROWN;
最大回撤:SIGNALS_TQ(13,0),COLORGRAY;
夏普比率:SIGNALS_TQ(14,0),COLORLIMAGENTA;
每日资金:SIGNALS_TQ(15,0),COLORLIGRAY;
持仓量:SIGNALS_TQ(16,0),COLORLIRED;  {显示每日持仓量}

{绘制交易信号图标}
DRAWICON(BUY_SIGNAL, LOW, 1);
DRAWICON(SELL_SIGNAL, HIGH, 2);


函数说明：
SIGNALS_TQ(ID, TYPE)
    ID: TQ数据中的序号 (1-16)，对应data_list子列表中的位置。
    TYPE: 处理方式。
        1 - 平滑处理，没有自定义数据的周期返回上一周期的值。
        0 - 不做平滑处理。
        2 - 没有数据则为0。
    """)
    print("="*60)

if __name__ == "__main__":
    main()
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # sendfile.py

```python
import numpy as np
import pandas as pd
from tqcenter import tq
import time
import json
"""
    这里是tq的简单使用示例
    使用时请确保已经启动通达信客户端并登录
    取消对应注释即可运行对应功能
"""
#初始化
tq.initialize(__file__) #所有策略连接通达信客户端都必须调用此函数进行初始化
file = "513100.txt"
tq.send_file(file)
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # sendfilepdf.py

```python
import numpy as np
import pandas as pd
from tqcenter import tq
import time
import json
"""
    这里是tq的简单使用示例
    使用时请确保已经启动通达信客户端并登录
    取消对应注释即可运行对应功能
"""
#初始化
tq.initialize(__file__) #所有策略连接通达信客户端都必须调用此函数进行初始化
file = "min.pdf"
tq.send_file(file)
```
