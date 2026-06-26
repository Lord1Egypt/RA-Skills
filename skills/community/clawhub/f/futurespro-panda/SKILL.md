---
name: "futurespro-panda"
description: "期货手续费与保证金查询工具。提供期货品种手续费、保证金、特殊品种开户条件、交易公告、交易日历等数据查询。Invoke when user asks about futures fees, margins, special variety conditions, trading announcements, or calendar events. Supports querying by product name, contract code, company margins, and date-based announcements."
---

# FuturesPro Panda Skill

期货手续费与保证金数据查询工具。通过 HTTP API 获取实时期货数据。

## 配置

默认 API 地址：`https://124.221.52.208`

所有接口路径前缀为 `/api/`。如用户指定其他地址，使用用户提供的地址。

## 使用方法

当用户查询期货相关数据时，使用 `curl` 或 `WebFetch` 工具调用对应 API。

### 中文参数编码

URL 中的中文参数需要 URL 编码。常用编码：
- 苹果 = `%E8%8B%B9%E6%9E%9C`
- 原油 = `%E5%8E%9F%E6%B2%B9`
- 黄金 = `%E9%BB%84%E9%87%91`
- 白银 = `%E7%99%BD%E9%93%B6`
- 铜 = `%E9%93%9C`
- 螺纹钢 = `%E8%9E%BA%E7%BA%B9%E9%92%A2`

或使用 `curl --data-urlencode` 自动编码。

---

## API 接口

### 1. 手续费与保证金查询

**端点：** `GET /api/fees`

**参数：**
| 参数 | 类型 | 说明 |
|------|------|------|
| product_name | string | 品种名称模糊匹配，如 "苹果"、"原油" |
| contract_code | string | 合约代码模糊匹配，如 "AP605" |
| max_margin | float | 最大保证金筛选 |
| margin_type | string | "company" 使用公司保证金，否则交易所 |
| company_id | int | 公司 ID，配合 margin_type="company" |

**示例调用：**
```bash
# 查询苹果品种
curl -sk "https://124.221.52.208/api/fees?product_name=%E8%8B%B9%E6%9E%9C"

# 查询原油（特殊品种）
curl -sk "https://124.221.52.208/api/fees?product_name=%E5%8E%9F%E6%B2%B9"

# 查询所有数据
curl -sk "https://124.221.52.208/api/fees"
```

**返回字段：**
- 品种名称、合约代码、product_code
- 1手开仓费用、1手平仓费用、1手平今费用
- 做多1手保证金、做空1手保证金
- 做多保证金率、做空保证金率
- 最新价、合约乘数、最小跳动

---

### 2. 特殊品种检测

**端点：** `GET /api/special-variety`

检测某品种是否为特殊品种（需要特殊开户条件，如原油、铁矿石、PTA等）。

**参数：**
| 参数 | 类型 | 说明 |
|------|------|------|
| product_code | string | 品种代码，如 "SC"、"I" |
| product_name | string | 品种名称，如 "原油"、"铁矿石" |

**示例调用：**
```bash
# 检测原油
curl -sk "https://124.221.52.208/api/special-variety?product_code=SC&product_name=%E5%8E%9F%E6%B2%B9"

# 检测铁矿石
curl -sk "https://124.221.52.208/api/special-variety?product_code=I&product_name=%E9%93%81%E7%9F%BF%E7%9F%B3"
```

**返回：**
```json
{
  "is_special": true,
  "condition_index": "COND_002",
  "content": "资金要求：申请日前连续5个交易日每日结算后账户可用资金余额不低于人民币50万元..."
}
```

---

### 3. 最近交易公告

**端点：** `GET /api/announcements/recent`

获取最近 5 条交易提示公告。

**示例调用：**
```bash
curl -sk "https://124.221.52.208/api/announcements/recent"
```

---

### 4. 交易日历数据

**端点：** `GET /api/announcements/calendar`

获取指定月份的日历事件，按日期分组。

**参数：**
| 参数 | 类型 | 说明 |
|------|------|------|
| year | int | 年份，默认当前年 |
| month | int | 月份，默认当前月 |

**示例调用：**
```bash
# 查询 2026 年 4 月
curl -sk "https://124.221.52.208/api/announcements/calendar?year=2026&month=4"
```

**返回格式：** 按日期分组的对象，如 `{"23": [...], "24": [...]}`

---

### 5. 按日期查询公告

**端点：** `GET /api/announcements/by-date`

**参数：**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| date_str | string | 是 | 日期，格式 "YYYY-MM-DD" |

**示例调用：**
```bash
curl -sk "https://124.221.52.208/api/announcements/by-date?date_str=2026-04-24"
```

---

### 6. 公司列表

**端点：** `GET /api/companies`

获取所有期货公司列表。

**示例调用：**
```bash
curl -sk "https://124.221.52.208/api/companies"
```

---

## 常见用户请求处理流程

### 用户问："查询苹果的手续费"
1. 调用 `GET /api/fees?product_name=%E8%8B%B9%E6%9E%9C`
2. 提取返回数据中的手续费和保证金信息
3. 以表格形式展示给用户

### 用户问："原油是特殊品种吗？开户条件是什么？"
1. 调用 `GET /api/special-variety?product_code=SC&product_name=%E5%8E%9F%E6%B2%B9`
2. 根据 `is_special` 判断是否为特殊品种
3. 如果是，展示 `content` 中的开户条件

### 用户问："最近的交易提示有哪些？"
1. 调用 `GET /api/announcements/recent`
2. 展示最近 5 条公告的标题和日期

### 用户问："4月24日有什么交易安排？"
1. 调用 `GET /api/announcements/by-date?date_str=2026-04-24`
2. 展示该日期的所有公告内容

### 用户问："显示4月的交易日历"
1. 调用 `GET /api/announcements/calendar?year=2026&month=4`
2. 按日期展示有事件的日期及对应内容
