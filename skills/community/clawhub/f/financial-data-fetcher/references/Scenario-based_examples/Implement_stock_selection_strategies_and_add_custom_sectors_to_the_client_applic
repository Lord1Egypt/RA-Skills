# # 执行选股策略并加入客户端自定义板块

### # 第一步：执行选股策略

```python
import pandas as pd
import numpy as np
from datetime import datetime
from tqcenter import tq

# 初始化tq
tq.initialize(__file__)

# 1. 基础配置（可修改项）
batch_codes = tq.get_stock_list_in_sector('通达信88')    # 目标板块
start_time = "20251025"                                  # 数据起始日期
target_end = datetime.now().strftime("%Y%m%d")           # 数据结束日期（当前日期）
N = 3                                                    # 目标连续上涨天数
block_code = 'LZXG'                                      # 自定义板块简称（必选）
block_name = '连涨选股'                                   # 自定义板块名称（必选）

# 2. 获取并整理收盘价数据
df_real = tq.get_market_data(
    field_list=['Close'],
    stock_list=batch_codes,
    start_time=start_time,
    end_time=target_end,
    dividend_type='front',  # 前复权
    period='1d',            # 日线
    fill_data=True          # 填充缺失数据
)
# 转换为「日期×股票代码」的收盘价宽表
close_df = tq.price_df(df_real, 'Close', column_names=batch_codes)

# 3. 标记每日是否上涨（核心判断逻辑）
is_up = close_df > close_df.shift(1)  # True=当日上涨，False=当日非上涨

# 4. 核心：计算连续上涨天数
# 步骤1：上涨日标记为1，非上涨日标记为NaN
up_mask = np.where(is_up, 1, np.nan)
up_mask_df = pd.DataFrame(up_mask, index=close_df.index, columns=close_df.columns)

# 步骤2：前向填充 → 连续上涨阶段的非上涨日（NaN）会被1填充
filled_df = up_mask_df.ffill()

# 步骤3：累计非NaN值的数量（初步计数）
consec_up_days = filled_df.notna().cumsum()

# 步骤4：非上涨日重置计数（关键步骤，实现“连续”效果）
reset_counts = consec_up_days.where(~is_up).ffill().fillna(0)
consec_up_days = (consec_up_days - reset_counts).astype(int)

# 5. 筛选符合条件的股票（连续上涨≥N天）
latest_date = consec_up_days.index[-1]  # 最新交易日
latest_consec_up = consec_up_days.loc[latest_date]  # 每只股票最新的连续上涨天数
target_stocks = latest_consec_up[latest_consec_up >= N].sort_values(ascending=False)
target_stocks_list = target_stocks.index.tolist()  # 提取符合条件的股票代码列表

# 6. 先创建自定义板块，再执行添加/清空操作
print(f"\n=== 筛选结果（连续上涨≥{N}天）===")
# 第一步：创建自定义板块
try:
    tq.create_sector(block_code=block_code, block_name=block_name)
    print(f"✅ 已成功创建自定义板块「{block_name}（{block_code}）」")
except Exception as e:
    # 板块已存在时可能报错，此处捕获异常不中断流程
    print(f"ℹ️  自定义板块创建提示：{e}（若提示已存在，可忽略此信息）")

# 第二步：处理板块成份股（添加/清空）
if not target_stocks.empty:
    # 打印筛选结果
    print(f"符合条件的股票共 {len(target_stocks)} 只：")
    for stock_code, days in target_stocks.items():
        print(f"{stock_code}：连续上涨 {days} 天")

    # 发送至自定义板块
    try:
        tq.send_user_block(block_code=block_code, stocks=target_stocks_list)
        print(f"\n✅ 已成功将股票添加至自定义板块「{block_name}（{block_code}）」")
    except Exception as e:
        print(f"\n❌ 添加自定义板块失败：{e}")

    # 发送提示消息至TQ策略管理器
    msg = f"MSG,筛选结果：{start_time}至{target_end}，连续上涨≥{N}天的股票共{len(target_stocks)}只，已添加至「{block_name}（{block_code}）」"
    try:
        tq.send_message(msg)
        print("✅ 提示消息发送成功")
    except Exception as e:
        print(f"❌ 消息发送失败：{e}")
else:
    # 无符合条件股票时清空板块
    print("暂无符合条件的股票")
    try:
        tq.send_user_block(block_code=block_code, stocks=[])
        print(f"✅ 已清空自定义板块「{block_name}（{block_code}）」")
    except Exception as e:
        print(f"❌ 清空自定义板块失败：{e}")

    # 发送空结果提示
    msg = f"MSG,筛选结果：{start_time}至{target_end}，连续上涨≥{N}天的股票共0只，已清空「{block_name}（{block_code}）」"
    try:
        tq.send_message(msg)
    except Exception as e:
        print(f"❌ 消息发送失败：{e}")
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 第二步：客户端查看执行效果

![](https://help.tdx.com.cn/quant/uploads/mindoc/images/m_a31e72f1df374561289662d227a3b8c9_r.png)
