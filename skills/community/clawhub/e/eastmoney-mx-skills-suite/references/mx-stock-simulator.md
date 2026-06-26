# eastmoney_stock_simulator - 妙想模拟组合管理

提供股票模拟组合管理系统，支持持仓查询、买卖操作、撤单、委托查询、历史成交查询和资金查询等功能。通过安全认证的 API 接口实现真实交易体验。

## 前置要求

使用模拟交易功能前，用户需先在妙想平台创建模拟账户并绑定模拟组合：
- 访问 **https://dl.dfcfs.com/m/itc4** 创建模拟账户
- 绑定模拟组合后方可使用交易功能

## 功能概览

| 功能模块 | 接口路径 | 说明 |
|---------|---------|------|
| 持仓查询 | `POST /api/claw/mockTrading/positions` | 获取持仓明细、成本、盈亏 |
| 买入卖出 | `POST /api/claw/mockTrading/trade` | 限价/市价委托 |
| 撤单 | `POST /api/claw/mockTrading/cancel` | 按委托编号撤单或一键撤单 |
| 委托查询 | `POST /api/claw/mockTrading/orders` | 当日/历史委托记录 |
| 资金查询 | `POST /api/claw/mockTrading/balance` | 总资产、可用资金、盈亏 |

## API 基础信息

- **基础 URL**: `https://mkapi2.dfcfs.com/finskillshub`
- **认证**: Header `apikey: {MX_APIKEY}`
- **方法**: 全部 `POST`，`Content-Type: application/json`

## 接口详细说明

### 1. 持仓查询

- **URL**: `${MX_API_URL}/api/claw/mockTrading/positions`
- **Body**: `{}`

```bash
curl -X POST "https://mkapi2.dfcfs.com/finskillshub/api/claw/mockTrading/positions" \
  -H "apikey: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**响应字段**:

| 字段 | 类型 | 说明 |
|------|------|------|
| `totalAssets` | Int64 | 总资产（厘，÷1000=元） |
| `availBalance` | Int64 | 可用余额（厘） |
| `totalPosValue` | Int64 | 总持仓市值（厘） |
| `posCount` | Int32 | 持仓股票数量 |
| `totalProfit` | Int64 | 总盈亏（厘） |

**持仓列表 `posList[]` 字段**:

| 字段 | 类型 | 说明 |
|------|------|------|
| `secCode` | String | 证券代码 |
| `secMkt` | Int32 | 市场号：0=深交所，1=上交所 |
| `secName` | String | 证券名称 |
| `count` | Int64 | 持仓数量（股） |
| `availCount` | Int64 | 可用数量（股） |
| `value` | Int64 | 市值（厘） |
| `costPrice` | Int64 | 成本价（÷10^costPriceDec） |
| `price` | Int64 | 现价（÷10^priceDec） |
| `dayProfit` | Int64 | 当日盈亏（厘） |
| `profit` | Int64 | 持仓盈亏（厘） |
| `profitPct` | Double | 持仓盈亏比例% |

### 2. 买入卖出

- **URL**: `${MX_API_URL}/api/claw/mockTrading/trade`

| 参数 | 必填 | 说明 |
|------|------|------|
| `type` | 是 | buy=买入，sell=卖出 |
| `stockCode` | 是 | 6位股票代码（仅A股） |
| `price` | 条件 | 委托价格（市价时忽略） |
| `quantity` | 是 | 委托数量（100的整数倍） |
| `useMarketPrice` | 否 | true=以行情最新价委托 |

```bash
curl -X POST "https://mkapi2.dfcfs.com/finskillshub/api/claw/mockTrading/trade" \
  -H "apikey: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type":"buy","stockCode":"600519","price":1780.00,"quantity":100,"useMarketPrice":false}'
```

### 3. 撤单

- **URL**: `${MX_API_URL}/api/claw/mockTrading/cancel`

| 参数 | 必填 | 说明 |
|------|------|------|
| `type` | 是 | order=按编号撤单，all=一键撤单 |
| `orderId` | 条件 | type=order 时必填 |
| `stockCode` | 条件 | type=order 时必填 |

### 4. 委托查询

- **URL**: `${MX_API_URL}/api/claw/mockTrading/orders`

| 参数 | 必填 | 说明 |
|------|------|------|
| `fltOrderDrt` | 否 | 0=全部，1=买入，2=卖出 |
| `fltOrderStatus` | 否 | 0=全部，2=已报，4=已成 等 |

**委托状态说明**:

| 状态值 | 含义 | 状态值 | 含义 |
|-------|------|-------|------|
| 1 | 未报 | 6 | 已报待撤 |
| 2 | 已报 | 7 | 部撤 |
| 3 | 部成 | 8 | 已撤 |
| 4 | 已成 | 9 | 废单 |

### 5. 资金查询

- **URL**: `${MX_API_URL}/api/claw/mockTrading/balance`
- **Body**: `{}`

**响应字段**:

| 字段 | 类型 | 说明 |
|------|------|------|
| `totalAssets` | Int64 | 总资产（厘） |
| `availBalance` | Int64 | 可用余额（厘） |
| `frozenMoney` | Int64 | 冻结金额（厘） |
| `totalPosValue` | Int64 | 总持仓市值（厘） |
| `totalPosPct` | Double | 总持仓仓位% |
| `nav` | Double | 单位净值 |
| `oprDays` | Int32 | 运作天数 |

## 脚本使用

```bash
# 查询持仓（默认）
python scripts/mx_stock_simulator.py "查询持仓"

# 查询资金
python scripts/mx_stock_simulator.py "查询资金"

# 买入股票
python scripts/mx_stock_simulator.py "买入600519 100股 价格1780"

# 卖出股票
python scripts/mx_stock_simulator.py "卖出600519 100股"

# 市价买入
python scripts/mx_stock_simulator.py "市价买入600519 100股"

# 一键撤单
python scripts/mx_stock_simulator.py "撤销所有订单"

# 查询委托
python scripts/mx_stock_simulator.py "查询委托"
```

## 错误处理

| 错误码 | 含义 | 处理方式 |
|-------|------|---------|
| 113 | 调用次数达上限 | 等待或更新 Key |
| 114 | API 密钥失效 | 重新获取 Key |
| 115 | 未携带密钥 | 配置 `MX_APIKEY` |
| 116 | 密钥不存在 | 检查 Key |
| 404 | 未绑定模拟组合 | 引导用户创建模拟账户 |
