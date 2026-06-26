## # 什么是量化交易

量化交易是指利用计算机科技并采用一定的数学模型去实现投资理念、实现投资策略的过程。简单的说，量化交易主要是做这样的事：

一个简单的投资想法 =&gt; 可执行的交易策略 =&gt; 可执行的代码程序 =&gt; 检验交易策略效果 =&gt; 实盘交易验证改进

### # Step 1：从一个简单的投资想法开始

投资想法即我们认为可能会盈利的投资方法、理念，比如熊市时期银行股是潜力股、复制基金经理的增强指数、金叉买入死叉卖出等等。这些想法通常以网络、书本和讲座等为载体，来源于投顾、同行以及自己的经验总结等等。

以一个简单的投资想法为例：

```python
如果遇到股价金叉，则买入
如果遇到股价死叉，则卖出
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # Step 2：完善这个想法，形成明确的可执行的交易策略

简单的投资想法通常比较模糊，我们需要将其细化成明确的可执行的策略，目的是为了能得到确定的信号进行交易操作。

一个可执行的交易策略至少需要明确以下几点:

1. Security：确定投资品种或范围
2. Condition：确定触发买/卖的具体条件
3. Quantity：确定买卖的数量/金额等

明确的可执行的交易策略的判断基准：根据交易策略的描述，不同的人在相同情形下，都能做出相同的交易操作。

上述关于金叉死叉的投资想法，显然它是不够明确的（可度量/可计算）。所以我们进一步细化：

```python
监测沪深300指数的所有成分股的收盘价
如果收盘价上穿收盘价的5日简单移动平均，则用全部可用资金买入该股票
如果收盘价的5日简单移动平均上穿收盘价，则卖出该股票所有持仓
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

现在，我们基本已经把之前的想法细化成了明确的可执行的交易策略。当然，可能还有些地方不够明确或者参数需要改动，这些可以随时想到随时修正，不必一次做到完美。

现在，我们想知道这样操作究竟会不会赚钱？

### # Step 3：编写一段代码，把交易策略转成可执行的代码程序

为了验证这个策略是否赚钱，我们需要把明确后的交易策略通过编程转成程序，计算机能根据历史数据/实时数据执行该策略产生模拟交易，或者根据实时数据执行该策略产生实盘交易。

把上述策略翻译成计算机可以识别的代码语言，即类似这样的代码：

```python
import pandas as pd
import vectorbt as vbt
from tqcenter import tq

tq.initialize(__file__)

# 解决 pandas future warning
pd.set_option('future.no_silent_downcasting', True)

# ========================= 核心配置（用户可直接修改这里）=========================
target_start = '20240930'  # 【目标回测开始时间】（真正想回测的起始日）
target_end = '20250930'    # 【目标回测结束时间】
stock_code_list = ['688318.SH']     # 股票代码
window = 5         # MA指标周期（如MA5、MA10、MA20，改这里自动适配历史数据）
# ================================================================================

start_time = (pd.to_datetime(target_start) - pd.Timedelta(days=window + 10)).strftime('%Y%m%d')

# 1.获取价格数据
df_real = tq.get_market_data(
    field_list=['Close', 'Open'],
    stock_list=stock_code_list,
    start_time=start_time,
    end_time=target_end,
    dividend_type='front',
    period='1d',
    fill_data=True
)
close_df = tq.price_df(df_real, 'Close', column_names=stock_code_list)
open_df = tq.price_df(df_real, 'Open', column_names=stock_code_list)


# 2.买卖信号计算与生成
ma5_dynamic = vbt.MA.run(close_df, window=window).ma
ma5_dynamic.columns = close_df.columns

entries_raw = close_df.vbt.crossed_above(ma5_dynamic)
exits_raw = close_df.vbt.crossed_below(ma5_dynamic)

# 信号移位+1
entries_df = entries_raw.shift(1).fillna(False).astype(bool)
exits_df = exits_raw.shift(1).fillna(False).astype(bool)


# 3. 执行回测
portfolio = vbt.Portfolio.from_signals(
    close=close_df,             # 净值计算用未复权收盘价
    entries=entries_df,              # 延迟后的买入信号
    exits=exits_df,                  # 延迟后的卖出信号
    price=open_df,                # 含滑点的成交价格
    init_cash=100000,            #  初始资金10万元
    fees=0.0003,                  # 手续费0.03%（双边）
    freq='D',                     # 日线频率
    size_granularity=100          # A股最小交易单位100股
)


# 4. 输出回测结果
print(f"\n======投资组合回测表现=====")
print(portfolio.stats())
print(f"\n======投资组合回测记录======")
print(portfolio.trades.records_readable)
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

这样一来，刚才细化好的策略转成了代码，计算机就能理解并执行了。

### # Step 4：回测或者模拟交易，检验策略效果

基本的检验策略方法有回测和模拟交易两种方法。核心区别是：回测是用历史数据模拟执行策略，模拟交易是用未来的实际数据模拟执行策略。。

**回测是让计算机能根据一段时间区间内的历史的数据来模拟执行该策略，根据结果评价并改进策略。**如果结果不好，则需要分析原因并改进。如果结果不错，则可以考虑用模拟交易进一步验证。

**模拟交易是让计算机能根据未来的实际数据模拟执行该策略一段时间区间，根据结果评价并改进策略。**如果策略在回测与模拟交易的表现都非常好，我们可以考虑进行完全真金白银的实盘交易。

回测举例说明：

1. 策略环境：设定初始虚拟资产100万元；选择一段历史时间区间：20100101到20200101；把该时间区间的各种数据如收盘股价行情等发给计算机。
2. 策略执行：计算机利用这些数据模仿历史真实的市场，执行我们编写的策略程序。
3. 策略评估：计算机会出具一份报告，根据这个报告我们知道，在20100101期初的100万元，按照我们的策略交易到期末20200101，会怎样？一般包括盈亏情况，下单情况，持仓变化，以及一些统计指标等，根据此评估交易策略的好坏。

模拟交易举例说明：

1. 策略环境：设定初始的虚拟资产比如100万元，选择开始执行模拟交易的时间点，比如下周一。那么从下周一开始，股市开始交易，真实的行情数据就会实时地发送到计算机。
2. 策略执行：计算机利用真实的数据模仿真实的市场，执行你的策略代码输出买卖队列，模拟系统会记录每一笔买卖记录。
3. 策略评估：我们可以得到一份实时更新的策略评估报告，这报告类似于回测得到的报告，不同的是会根据实际行情变化更新；同样我们能据此评估交易策略的好坏。

### # Step 5：实盘执行交易策略，并持续优化改进策略

实盘交易就是让计算机能根据实际行情，用真实资金账号来自动下单交易。注意，这时不再是用虚拟资产进行模拟交易，实盘交易账户上的盈亏都是真金白银。
 实盘交易一般也会给出一份类似模拟交易的投资分析报告，通过实时观察策略的实盘表现、根据投资理念的变化、市场状况的变化及时修正、改善和优化策略，使之保持持续盈利能力。
