# # 打通通达信量化任督二脉：公式与Python双向数据互通闭环

以下是[20250122通达信趋势财经公众号发布文章]

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAPCAYAAAA71pVKAAAABmJLR0QA/wD/AP+gvaeTAAAAEUlEQVQokWNgGAWjYBQMIgAAA5MAAdmyLDcAAAAASUVORK5CYII=)

(opens new window) 涉及的策略例子的完整代码。

📄 利用MACD公式筛选金叉信号.py
 用途：批量处理版本，一次计算全市场MACD指标，筛选金叉股票

```python
from tqcenter import tq

'''
    利用此示例需要先在客户端下载全A股盘后数据，不然结果不准确
    通过MACD指标公式选出最新交易日金叉的股票
'''

tq.initialize(__file__)

#先获取A股全部股票
all_stocks = tq.get_stock_list(market='5')

print("正在处理，请等待...")
import time

# 开始计时
start_time = time.time()

macd_stocks = []
mul_zb_result = tq.formula_process_mul_zb(
    formula_name='MACD',
    formula_arg='12,26,9',
    xsflag=6,
    return_count=2,
    return_date=False,
    stock_list=all_stocks,
    # stock_list=['600722.SH'],
    stock_period='1d',
    count=100,
    dividend_type=1)
# print(mul_zb_result)

if mul_zb_result:
    for key in mul_zb_result:
        if key != "ErrorId":
            if len(mul_zb_result[key]['DIF']) >= 2 and len(mul_zb_result[key]['DEA']) >= 2:
                if float(mul_zb_result[key]['DIF'][-2]) < float(mul_zb_result[key]['DEA'][-2]) and float(mul_zb_result[key]['DIF'][-1]) >= float(mul_zb_result[key]['DEA'][-1]):
                    macd_stocks.append(key)


print("今日MACD金叉股票列表：")
print(macd_stocks)
print("符合MACD金叉条件的股票数量：", len(macd_stocks))
# 结束计时
end_time = time.time()

# 计算时间差
execution_time = end_time - start_time
print(f"执行时间: {execution_time:.6f} 秒")  # 保留6位小数
print(f"执行时间: {execution_time * 1000:.2f} 毫秒")  # 转换为毫秒

zxg_result = tq.send_user_block(block_code='', stocks=macd_stocks)
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

📄 利用MACD公式筛选金叉信号for单.py
 用途：for循环版本，逐只股票计算MACD指标，适合小数量测试对比

```python
from tqcenter import tq

'''

    利用此示例需要先在客户端下载全A股盘后数据，不然结果不准确

    通过MACD指标公式选出最新交易日金叉的股票

'''
tq.initialize(__file__)

#先获取A股全部股票

all_stocks = tq.get_stock_list(market='5')

print("正在处理，请等待...")

import time

# 开始计时

start_time = time.time()

macd_stocks = []

for stock in all_stocks:

    try:

        # 1. 设置股票数据

        tq.formula_set_data_info(
            stock_code=stock,
            stock_period='1d',
            count=100,  # 需要足够的数据计算MACD
            dividend_type=1  # 前复权
        )

        # 2. 获取MACD指标

        macd_result = tq.formula_zb(
            formula_name='MACD',
            formula_arg='12,26,9',
            xsflag=6
        )

        # 3. 获取DIF和DEA值，判断金叉

        if macd_result and 'Data' in macd_result:
            dif_values = macd_result['Data']['DIF']
            dea_values = macd_result['Data']['DEA']

            if len(dif_values) >= 2 and len(dea_values) >= 2:
                dif_prev = float(dif_values[-2])  # 前一天的DIF
                dif_now = float(dif_values[-1])   # 今天的DIF
                dea_prev = float(dea_values[-2])  # 前一天的DEA
                dea_now = float(dea_values[-1])   # 今天的DEA

                # MACD金叉信号：昨天DIF<DEA，今天DIF>=DEA
                if dif_prev < dea_prev and dif_now >= dea_now:
                    macd_stocks.append(stock)
                    print(f"MACD金叉信号: {stock}, DIF: {dif_prev:.4f}→{dif_now:.4f}, DEA: {dea_prev:.4f}→{dea_now:.4f}")

    except Exception as e:
        print(f"处理股票 {stock} 时出错: {e}")
        continue

print("今日MACD金叉股票列表：")
print(macd_stocks)
print("符合MACD金叉条件的股票数量：", len(macd_stocks))

# 结束计时

end_time = time.time()

# 计算时间差

execution_time = end_time - start_time

print(f"执行时间: {execution_time:.6f} 秒")  # 保留6位小数
print(f"执行时间: {execution_time * 1000:.2f} 毫秒")  # 转换为毫秒

zxg_result = tq.send_user_block(block_code='', stocks=macd_stocks)
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

📄 订阅Handlebar.py
 用途：订阅方式实时预警，使用subscribe_hq，每6秒运行一次回调（适合100只以内股票）

```python
import datetime

import json

import sys

sys.path.append('C:/new_tdx_test2025/PYPlugins/user')

from tqcenter import tq

tq.initialize('订阅Handlebar.py')

"""

这里是外部运行的初始化模式把tqcenter目录加上，再import它，   initialize参数****.py标准的py文件名就行

"""

# 获取A股全部股票（测试时限制数量）# 订阅不能超过100只

all_stocks = tq.get_stock_list(market='5')[:50]

def get_real_time_data(stock_code):

    """

    获取股票的实时行情数据

    根据通达信TQ接口文档，这里需要调用相应的数据获取函数

    """

    try:

        # 获取最近两天的数据，用于获取前一日收盘价

        market_data = tq.get_market_data(

            field_list=['Close', 'Volume'],

            stock_list=[stock_code],

            count=2,  # 获取2天数据，用于获取前一日收盘价

            period='1d',

            dividend_type='none',

            fill_data=True

        )

        if market_data and 'Close' in market_data:

            close_df = market_data['Close']

            if not close_df.empty:

                # 获取最新收盘价

                last_price = close_df.iloc[-1][stock_code]

                # 获取前一日收盘价

                if len(close_df) >= 2:

                    prev_close = close_df.iloc[-2][stock_code]

                else:

                    prev_close = '0.00'

                # 获取成交量

                if 'Volume' in market_data:

                    volume_df = market_data['Volume']

                    volume = volume_df.iloc[-1][stock_code] if not volume_df.empty else '0'

                else:

                    volume = '0'

                return str(last_price), str(prev_close), str(volume)

    except Exception as e:

        print(f"获取{stock_code}实时数据失败: {e}")

    return '0.00', '0.00', '0'

def my_callback_func(data_str):

    print("Callback received data:", data_str)

    code_json = json.loads(data_str)

    print(f"codes = {code_json.get('Code')}")

    upn_stocks = []  # 用于存放符合UPN公式选股条件的股票列表

    for stock in all_stocks:

        formula_set_res = tq.formula_set_data_info(

            stock_code=stock,

            stock_period='1d',

            count=20,

            dividend_type=1

        )

        if formula_set_res:

            # 使用UPN公式选股，参数'3'表示3日上涨

            formula_xg = tq.formula_xg(formula_name='UPN', formula_arg='3')

            print(f"formula_xg = {formula_xg}")

            if formula_xg and 'Data' in formula_xg and 'UP3' in formula_xg['Data']:

                up3_data = formula_xg['Data']['UP3']

                if up3_data and len(up3_data) > 0 and up3_data[-1] is not None:

                    if up3_data[-1] != '0':  #之前版本是0.00也行 这里要改一下

                        upn_stocks.append(stock)

    print("符合UPN公式选股条件的股票列表：")

    print(upn_stocks)

    print("符合UPN公式选股条件的股票数量：", len(upn_stocks))

    # 为选出的股票发送预警

    if upn_stocks:

        send_warnings_for_stocks(upn_stocks)

    return None

def send_warnings_for_stocks(stock_list):

    """为股票列表发送预警信息"""

    if not stock_list:

        return

    # 获取当前时间，格式化为YYYYMMDDHHMMSS

    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # 准备预警参数列表

    stock_count = len(stock_list)

    # 初始化列表

    time_list = []

    price_list = []

    close_list = []

    volum_list = []

    # 为每只股票获取实时数据

    for stock in stock_list:

        last_price, prev_close, volume = get_real_time_data(stock)

        time_list.append(current_time)

        price_list.append(last_price)

        close_list.append(prev_close)

        volum_list.append(volume)

    # 其他固定参数

    reason_list = ["3天连涨"] * stock_count  # 根据实际选股条件修改

    bs_flag_list = ['0'] * stock_count  # 买卖标志：0

    warn_type_list = ['0'] * stock_count  # 预警类型：0

    # 调用send_warn函数发送预警

    try:

        warn_res = tq.send_warn(

            stock_list=stock_list,

            time_list=time_list,

            price_list=price_list,

            close_list=close_list,

            volum_list=volum_list,

            bs_flag_list=bs_flag_list,

            warn_type_list=warn_type_list,

            reason_list=reason_list,

            count=stock_count

        )

        print("预警发送结果：", warn_res)

        # 根据搜索结果[6](@ref)，预警发送成功后会在TQ策略信号窗口展示

        # 预警图标对应bs_flag_list的每个元素的整数值，0买为红色B，1卖为绿色S，2未知为黄色双叠三角形

        # 双击买卖预警信号记录可以直接打开闪电下单进行买卖操作

    except Exception as e:

        print(f"发送预警失败: {e}")

# 订阅行情

sub_hq = tq.subscribe_hq(stock_list=all_stocks, callback=my_callback_func)

print("订阅结果：", sub_hq)

# 可选：设置定时执行或保持运行

import time

try:

    print("程序运行中，按Ctrl+C停止...")

    while True:

        time.sleep(60)  # 每分钟检查一次

except KeyboardInterrupt:

    print("程序终止")

    # 取消订阅

    if sub_hq:

        tq.unsubscribe_hq(stock_list=all_stocks)

tq.close()
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

📄 定时器实时预警Handlebar效果.py
 用途：定时器方式实时预警，每分钟运行一次（可覆盖全市场几千只股票）

```python
#定时器实时预警

定时器实时预警Handlebar效果.py
```python
#定时器实时预警

import datetime

import json

import sys

import time

sys.path.append('C:/new_tdx_test2025/PYPlugins/user')

from tqcenter import tq

tq.initialize('定时器实时预警Handlebar效果.py')

# 获取A股全部股票（测试时限制数量）

all_stocks = tq.get_stock_list(market='5')[:150]

def get_real_time_data(stock_code):

    """

    获取股票的实时行情数据

    根据通达信TQ接口文档，这里需要调用相应的数据获取函数

    """

    try:

        # 获取最近两天的数据，用于获取前一日收盘价

        market_data = tq.get_market_data(

            field_list=['Close', 'Volume'],

            stock_list=[stock_code],

            count=2,  # 获取2天数据，用于获取前一日收盘价

            period='1d',

            dividend_type='none',

            fill_data=True

        )

        if market_data and 'Close' in market_data:

            close_df = market_data['Close']

            if not close_df.empty:

                # 获取最新收盘价

                last_price = close_df.iloc[-1][stock_code]

                # 获取前一日收盘价

                if len(close_df) >= 2:

                    prev_close = close_df.iloc[-2][stock_code]

                else:

                    prev_close = '0.00'

                # 获取成交量

                if 'Volume' in market_data:

                    volume_df = market_data['Volume']

                    volume = volume_df.iloc[-1][stock_code] if not volume_df.empty else '0'

                else:

                    volume = '0'

                return str(last_price), str(prev_close), str(volume)

    except Exception as e:

        print(f"获取{stock_code}实时数据失败: {e}")

    return '0.00', '0.00', '0'

def run_upn_selection():

    """

    执行UPN公式选股并发送预警

    这个函数将每分钟执行一次

    """

    print(f"\n{'='*50}")

    print(f"执行时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    print(f"{'='*50}")

    upn_stocks = []  # 用于存放符合UPN公式选股条件的股票列表

    for stock in all_stocks:

        formula_set_res = tq.formula_set_data_info(

            stock_code=stock,

            stock_period='1d',

            count=5,

            dividend_type=1

        )

        if formula_set_res:

            # 使用UPN公式选股，参数'3'表示3日上涨

            formula_xg = tq.formula_xg(formula_name='UPN', formula_arg='3')

            if formula_xg and 'Data' in formula_xg and 'UP3' in formula_xg['Data']:

                up3_data = formula_xg['Data']['UP3']

                if up3_data and len(up3_data) > 0 and up3_data[-1] is not None:

                    if up3_data[-1] != '0':

                        upn_stocks.append(stock)

    print("符合UPN公式选股条件的股票列表：")

    print(upn_stocks)

    print("符合UPN公式选股条件的股票数量：", len(upn_stocks))

    # 为选出的股票发送预警

    if upn_stocks:

        send_warnings_for_stocks(upn_stocks)

    else:

        print("本次选股未发现符合条件的股票")

def send_warnings_for_stocks(stock_list):

    """为股票列表发送预警信息"""

    if not stock_list:

        return

    # 获取当前时间，格式化为YYYYMMDDHHMMSS

    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # 准备预警参数列表

    stock_count = len(stock_list)

    # 初始化列表

    time_list = []

    price_list = []

    close_list = []

    volum_list = []

    # 为每只股票获取实时数据

    for stock in stock_list:

        last_price, prev_close, volume = get_real_time_data(stock)

        time_list.append(current_time)

        price_list.append(last_price)

        close_list.append(prev_close)

        volum_list.append(volume)

    # 其他固定参数

    reason_list = ["3天连涨"] * stock_count  # 根据实际选股条件修改

    bs_flag_list = ['0'] * stock_count  # 买卖标志：0

    warn_type_list = ['0'] * stock_count  # 预警类型：0

    # 调用send_warn函数发送预警

    try:

        warn_res = tq.send_warn(

            stock_list=stock_list,

            time_list=time_list,

            price_list=price_list,

            close_list=close_list,

            volum_list=volum_list,

            bs_flag_list=bs_flag_list,

            warn_type_list=warn_type_list,

            reason_list=reason_list,

            count=stock_count

        )

        print("预警发送结果：", warn_res)

        # 根据搜索结果[5](@ref)，预警发送成功后会在TQ策略信号窗口展示

        # 预警图标对应bs_flag_list的每个元素的整数值，0买为红色B，1卖为绿色S，2未知为黄色双叠三角形

        # 双击买卖预警信号记录可以直接打开闪电下单进行买卖操作

    except Exception as e:

        print(f"发送预警失败: {e}")

# 主循环：每分钟执行一次选股

def main_loop():

    """

    主循环函数，每分钟执行一次选股

    使用time.sleep()实现定时执行[6](@ref)

    """

    print("UPN选股预警系统启动")

    print(f"开始时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    print(f"监控股票数量: {len(all_stocks)}")

    print("="*50)

    execution_count = 0

    try:

        while True:

            execution_count += 1

            print(f"\n第{execution_count}次执行选股...")

            # 执行选股逻辑

            run_upn_selection()

            # 计算下次执行时间

            next_time = datetime.datetime.now() + datetime.timedelta(minutes=1)

            print(f"下次执行时间: {next_time.strftime('%Y-%m-%d %H:%M:%S')}")

            # 等待60秒[6](@ref)

            time.sleep(60)

    except KeyboardInterrupt:

        print("\n程序被用户中断")

    except Exception as e:

        print(f"程序运行出错: {e}")

    finally:

        print("UPN选股预警系统已停止")

# 启动主循环

if __name__ == "__main__":

main_loop()
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

📄 利用UPN公式筛选出近期连涨股.py
 用途：批量处理版本，使用UPN公式筛选3日连涨股票

```python
from tqcenter import tq

import time

'''

    利用此示例需要先在客户端下载全A股盘后数据，不然结果不准确

'''

tq.initialize(__file__)

#先获取A股全部股票

all_stocks = tq.get_stock_list(market='5')

print("正在处理，请等待...")

upn_stocks = []

mul_xg_result = tq.formula_process_mul_xg(

    formula_name='UPN',

    formula_arg='3',

    return_count=1,

    return_date=False,

    stock_list=all_stocks,

    stock_period='1d',

    count=5,

    dividend_type=1)

# print(mul_xg_result)

if mul_xg_result:

    for key in mul_xg_result:

        if key != "ErrorId":

            if mul_xg_result[key]['UP3'] and mul_xg_result[key]['UP3'][-1] == '1':

                upn_stocks.append(key)

print("符合UPN公式选股条件的股票列表：")

print(upn_stocks)

print("符合UPN公式选股条件的股票数量：", len(upn_stocks))

zxg_result = tq.send_user_block(block_code='', stocks=upn_stocks)
```
