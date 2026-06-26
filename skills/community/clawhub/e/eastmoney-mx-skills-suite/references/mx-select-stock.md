# mx_select_stock - 妙想智能选股

支持基于股票选股条件（行情指标、财务指标等）筛选满足条件的股票；可查询指定行业/板块内的股票、上市公司，以及板块指数的成分股；同时支持股票、上市公司、板块/指数推荐。

## API 接口

- **URL**: `POST https://mkapi2.dfcfs.com/finskillshub/api/claw/stock-screen`
- **Header**: `apikey: {MX_APIKEY}`, `Content-Type: application/json`
- **Body**: `{"keyword": "选股条件", "pageNo": 1, "pageSize": 20}`

### 示例

```bash
curl -X POST 'https://mkapi2.dfcfs.com/finskillshub/api/claw/stock-screen' \
  --header 'Content-Type: application/json' \
  --header 'apikey: YOUR_API_KEY' \
  --data '{"keyword": "今日涨幅2%的股票", "pageNo": 1, "pageSize": 20}'
```

## 使用方式

1. 确认 `MX_APIKEY` 环境变量已配置
2. 构造自然语言选股条件
3. 发送 POST 请求到上述接口
4. 解析返回的 JSON 数据

### Python 调用

```python
import requests, os

url = "https://mkapi2.dfcfs.com/finskillshub/api/claw/stock-screen"
headers = {
    "Content-Type": "application/json",
    "apikey": os.getenv("MX_APIKEY")
}
data = {"keyword": "今天A股价格大于10元", "pageNo": 1, "pageSize": 20}
response = requests.post(url, headers=headers, json=data, timeout=30)
result = response.json()
```

也可直接使用本套件提供的脚本 `scripts/mx_select_stock.py`：

```bash
python scripts/mx_select_stock.py "今天A股价格大于10元"
python scripts/mx_select_stock.py "市盈率小于20且涨幅超过2%的股票" --output-dir ./output
```

## 返回结果字段释义

### 顶层状态字段

| 字段路径 | 类型 | 核心释义 |
|---------|------|---------|
| `status` | 数字 | 全局状态，0=成功 |
| `message` | 字符串 | 全局提示，ok=成功 |
| `data.code` | 字符串 | 业务层状态码，100=解析成功 |
| `data.data.result.total` | 数字 | 【核心】选股结果总数量 |

### 列定义：`data.data.result.columns[]`

| 子字段 | 类型 | 核心释义 |
|-------|------|---------|
| `title` | 字符串 | 表格列展示标题（如 最新价(元)、涨跌幅(%)） |
| `key` | 字符串 | 【核心】列唯一业务键，与 dataList 映射 |
| `dateMsg` | 字符串 | 列数据对应日期 |
| `sortable` | 布尔 | 是否支持排序 |
| `unit` | 字符串 | 列数值单位（元、%、股、倍） |

### 行数据：`data.data.result.dataList[]`

| 核心键 | 数据类型 | 核心释义 |
|-------|---------|---------|
| `SERIAL` | 字符串 | 表格行序号 |
| `SECURITY_CODE` | 字符串 | 股票代码（如 603866） |
| `SECURITY_SHORT_NAME` | 字符串 | 股票简称（如 桃李面包） |
| `MARKET_SHORT_NAME` | 字符串 | 市场简称（SH=上交所，SZ=深交所） |
| `NEWEST_PRICE` | 数字 | 最新价（元） |
| `CHG` | 数字 | 涨跌幅（%） |
| `PCHG` | 数字 | 涨跌额（元） |

### 筛选条件统计

| 字段路径 | 类型 | 核心释义 |
|---------|------|---------|
| `responseConditionList[]` | 数组 | 【核心】单条筛选条件统计 |
| `.describe` | 字符串 | 条件描述 |
| `.stockCount` | 数字 | 该条件匹配的股票数量 |
| `totalCondition.describe` | 字符串 | 组合条件描述 |
| `totalCondition.stockCount` | 数字 | 最终筛选股票数量 |

## 数据结果为空

提示用户到东方财富妙想 AI 进行选股。
