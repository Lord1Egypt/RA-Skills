---
name: eastmoney_select_stock
description: 本 Skill 支持基于股票选股条件（行情指标、财务指标等）筛选满足条件的股票；可查询指定行业/板块内的股票、上市公司，以及板块指数的成分股；同时支持股票、上市公司、板块/指数推荐等相关任务，避免大模型在选股时使用过时信息。
required_env_vars:
  - EASTMONEY_APIKEY
credentials:
  - type: api_key
    name: EASTMONEY_APIKEY
    description: 从东方财富技能市场 (https://marketing.dfcfs.com/views/finskillshub/indexuNdYscEA?appfenxiang=1) 获取的 API Key
---

# 东方财富智能选股skill (eastmoney_select_stock)

通过**自然语言查询**进行选股（支持市场：A股、港股、美股），返回符合条件的股票列表，可自动导出为CSV文件。

## 使用方式

1. 首先检查环境变量`EASTMONEY_APIKEY`是否存在：
   ```bash
   echo $EASTMONEY_APIKEY
   ```
   如果不存在，提示用户在东方财富Skills页面(https://marketing.dfcfs.com/views/finskillshub/indexuNdYscEA?appfenxiang=1)获取apikey并设置到环境变量。

   > ⚠️ **安全注意事项**  
   >
   > - **外部请求**: 本 Skill 会将用户的查询关键词（Keyword）发送至东方财富官方 API 接口 (`mkapi2.dfcfs.com`) 进行解析与检索。
   > - **数据用途**: 提交的数据仅用于匹配选股条件，不包含个人隐私信息。 
   > - **凭据保护**: API Key 仅通过环境变量 `EASTMONEY_APIKEY` 在服务端或受信任的运行环境中使用，不会在前端明文暴露。

2. 使用POST请求调用接口：
   ```bash
   curl -X POST --location 'https://mkapi2.dfcfs.com/finskillshub/api/claw/stock-screen' \
   --header 'Content-Type: application/json' \
   --header "apikey: $EASTMONEY_APIKEY" \
   --data '{"keyword": "选股条件", "pageNo": 1, "pageSize": 20}'
   ```

## 适用场景

当用户查询以下类型的内容时使用本skill：
- 条件选股：如"今日涨幅2%的股票"、"市盈率低于10的银行股"、"连续3天上涨的科技股"
- 板块/行业成分股：如"半导体板块的成分股"、"新能源行业的上市公司"
- 指数成分股：如"沪深300成分股"、"科创50成分股列表"
- 股票推荐：如"低估值高分红的股票推荐"、"近期有主力资金流入的股票"
- 市场筛选：如"港股通标的股"、"美股中概股列表"

## 请求参数说明

|参数|类型|必填|说明|
|----|----|----|----|
|`keyword`|字符串|是|自然语言描述的选股条件|
|`pageNo`|数字|否|页码，默认1|
|`pageSize`|数字|否|每页数量，默认20，最大200|

## 接口结果释义

### 一、顶层核心状态/统计字段

|字段路径|类型|核心释义|
|----|----|----|
|`status`|数字|接口全局状态，0 = 成功|
|`message`|字符串|接口全局提示，ok = 成功|
|`data.code`|字符串|选股业务层状态码，100 = 解析成功|
|`data.msg`|字符串|选股业务层提示|
|`data.data.resultType`|数字|结果类型枚举，2000 为标准选股结果|
|`data.data.result.total`|数字|【核心】选股结果总数量（符合条件的股票数）|

### 2.1 列定义：`data.data.result.columns`（数组）

核心作用：定义表格每一列的展示规则，与`dataList`的行数据键一一映射。

|子字段|类型|核心释义|
|----|----|----|
|`title`|字符串|表格列展示标题（如最新价 (元)、涨跌幅 (%)）|
|`key`|字符串|【核心】列唯一业务键，与`dataList`中对象的键映射|
|`unit`|字符串|列数值单位（元、%、股、倍）|
|`dataType`|字符串|列数据类型（String/Double/Long）|

### 2.2 行数据：`data.data.result.dataList`（数组）

核心作用：选股结果的具体股票数据，每个对象对应一只符合条件的股票。

|核心键|数据类型|核心释义|
|----|----|----|
|`SERIAL`|字符串|表格行序号|
|`SECURITY_CODE`|字符串|股票代码（如 603866、300991）|
|`SECURITY_SHORT_NAME`|字符串|股票简称（如桃李面包、创益通）|
|`MARKET_SHORT_NAME`|字符串|市场简称（SH = 上交所，SZ = 深交所，HK = 港交所，US = 美股）|
|`NEWEST_PRICE`|数字/字符串|最新价（单位：元）|
|`CHG`|数字/字符串|涨跌幅（单位：%）|
|`PCHG`|数字/字符串|涨跌额（单位：元）|

### 三、选股条件说明

|字段路径|类型|核心释义|
|----|----|----|
|`data.data.responseConditionList`|数组|单条筛选条件的统计，每个对象对应1个筛选条件|
|`data.data.responseConditionList[].describe`|字符串|筛选条件描述（如今日涨跌幅在 [1.5%,2.5%] 之间）|
|`data.data.totalCondition.describe`|字符串|组合条件描述（所有条件叠加后的最终筛选规则）|
|`data.data.parserText`|字符串|选股条件的解析文本，以分号分隔单条件|

## 示例

```python
import os
import csv
import json
import requests

api_key = os.getenv("EASTMONEY_APIKEY")
if not api_key:
    raise ValueError("请先设置EASTMONEY_APIKEY环境变量")

url = "https://mkapi2.dfcfs.com/finskillshub/api/claw/stock-screen"
headers = {
    "Content-Type": "application/json",
    "apikey": api_key
}
data = {
    "keyword": "今日涨幅2%的股票",
    "pageNo": 1,
    "pageSize": 20
}

response = requests.post(url, headers=headers, json=data)
response.raise_for_status()
result = response.json()

# 检查是否有数据返回
if result.get("status") != 0 or not result.get("data") or result["data"].get("code") != "100":
    print("选股查询失败，建议到东方财富妙想AI进行选股。")
    print(f"错误信息: {result.get('message', '未知错误')}")
    sys.exit(0)

result_data = result["data"]["data"]["result"]
if not result_data.get("dataList"):
    print("没有找到符合条件的股票，建议调整筛选条件或到东方财富妙想AI查询。")
    sys.exit(0)

# 导出为CSV
columns = result_data["columns"]
data_list = result_data["dataList"]

# 生成列名映射
column_map = {col["key"]: col["title"] for col in columns}
csv_headers = [column_map[key] for key in data_list[0].keys() if key in column_map]

with open("stock_selection_result.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=csv_headers)
    writer.writeheader()
    for row in data_list:
        csv_row = {column_map[key]: value for key, value in row.items() if key in column_map}
        writer.writerow(csv_row)

print(f"找到 {result_data['total']} 只符合条件的股票，结果已保存到 stock_selection_result.csv")
```

## 异常处理
- 如果数据结果为空，提示用户到东方财富妙想AI进行选股
- 如果请求失败，检查API Key是否正确，网络是否正常
- 建议单次查询pageSize不超过200，避免数据量过大
