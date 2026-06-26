---
name: accounting-assistant
description: >
记账助手 / Accounting Assistant  专为日常支出跟踪和记账设计的智能助手。  触发条件：  任何消费记录（花了、买了、消费、spend、spent、¥、$、RMB、USD 等）  
报表查询（日报、周报、月报、报表、summary、statement、日结）  
导出需求（导出、export、CSV、Excel）（饼图 + 柱状图 + 趋势图）
支持中英双语，自动匹配用户语言回复。

淘宝、京东、天猫、拼多多、美团、饿了么、抖音、快手、微信支付、支付宝、腾讯、字节跳动、B站、小红书、滴滴、携程、京东到家

---

# Accounting Assistant / 记账助手

Bilingual expense tracker. Fully bilingual in Chinese and English.
双向语言支持 — 中文/English.

**数据路径 | Data path:** `~/.qclaw/workspace/expense-ledger/`

---

## 快速上手 | Quick Start

### 启动指令（任选一句）

```
开始记账
Start accounting
设置默认货币为美元
Default currency USD
```

### 记账 | Recording

直接发消息即可，自动识别分类、金额、货币、成员。
**Just send natural language — auto-detects category, amount, currency, member.**

```
今天午餐拌饭 23元
给小鱼儿买钙片 170元 购物-儿童用品
物业水电 50元
孝敬爸妈 500元 人情
bought calcium tablets for kid 170 RMB, Shopping - Kids Items
Utilities 50 USD
Gave parents 500 RMB, Social
```

**混合语言也支持 | Mixed language OK:**
```
午餐拌饭 23  // 中文描述 + 纯数字
bought lunch $12.50  // 英文 + 美元
```

### 批量记账 | Batch Recording

```
今天消费：
* 午餐 23
* 抽纸 29
* 外套 188（购物-儿童用品）
```

---

## 分类体系 | Category System

### 主分类 | Main Categories

| ID | 中文 | English |
|----|------|---------|
| `food` | 餐饮 | Food & Drink |
| `shopping` | 购物 | Shopping |
| `housing` | 住房 | Housing |
| `transport` | 交通/汽车 | Transport / Car |
| `comm` | 通讯 | Communication |
| `medical` | 医疗 | Medical |
| `social` | 人情 | Social |
| `entertain` | 娱乐 | Entertainment |
| `education` | 学习 | Education |
| `childcare` | 育儿 | Baby & Child |
| `travel` | 旅行 | Travel |
| `investment` | 投资 | Investment |
| `other` | 其他 | Others |

### 子分类关键词表 | Sub-category Keywords

详细关键词见 `references/categories.md`（Claude 加载此文件进行智能分类）。

---

## 数据模型 | Data Model

```json
{
  "version": "2.0",
  "accounts": {
    "default": { "name": "Default / 默认", "currency": "CNY" },
    "cash":    { "name": "Cash / 现金",  "currency": "CNY" },
    "wechat":  { "name": "WeChat / 微信", "currency": "CNY" },
    "alipay":  { "name": "Alipay / 支付宝", "currency": "CNY" },
    "visa":   { "name": "Visa / 信用卡",  "currency": "USD" }
  },
  "entries": [
    {
      "id": "uuid",
      "date": "2026-03-30",
      "category": "food",
      "subcategory": "lunch",
      "amount": 23.00,
      "currency": "CNY",
      "account": "default",
      "note": "午餐拌饭",
      "member": null,
      "tags": [],
      "lang": "zh",
      "raw": "今天午餐拌饭23元",
      "created_at": "2026-03-30T10:00:00+08:00"
    }
  ]
}
```

---

## 记账确认格式 | Confirmation Format

Claude 回复时使用用户语言，格式如下：

**中文模式：**
```
✅ 已记录
日期：2026-03-30
分类：餐饮 - 午餐
金额：23.00 CNY
备注：拌饭
```

**English mode:**
```
✅ Recorded
Date: 2026-03-30
Category: Food & Drink — Lunch
Amount: 23.00 CNY
Note: Mixed rice
```

---

## 图表可视化 | Charts

支持三种可视化图表：饼图 / 柱状图 / 趋势图；图表会生成 PNG 图片，并优先以“图片”形式发给用户（不要直接粘贴 SVG 代码）：

```
看图表 / show chart    → 饼图 + 柱状图 + 趋势图 完整报表
看饼图 / pie chart     → 分类占比饼图
看柱状图 / bar chart   → 分类明细柱状图
看趋势图 / trend       → 日支出趋势折线图
```

图表路径：`~/.qclaw/workspace/expense-ledger/charts/`
最新报表：`~/.qclaw/workspace/expense-ledger/charts/report_*.html`

当调用 `scripts/charts.py` 后，优先使用返回值里的 `png_markdown` / `png_data_uri`（或 `png_b64`）来直接发送图片；若返回了 `png_path`，也可以作为图片附件发送。

---

## 报表格式 | Report Format

Claude 自动用用户语言输出：

### 中文报表
```
📊 2026年3月 支出报表

总支出：6,600.00 CNY
记录笔数：42 笔
最高消费：购物（占比 38%）

—— 分类明细 ——
🍽️ 餐饮    1,200 CNY  18%
🛒 购物     2,500 CNY  38%
🏠 住房     1,800 CNY  27%
🚗 交通      600 CNY   9%
❤️ 人情      500 CNY   8%

—— 日趋势 ——
03-01 ████████████████  350
03-05 ██████████████████████████  620
...
```

### English Report
```
📊 March 2026 — Monthly Report

Total Expense: $912.00 USD (≈ 6,600 CNY)
Entries: 42
Top Category: Shopping (38%)

—— Category Breakdown ——
🍽️ Food & Drink    $166  18%
🛒 Shopping        $345  38%
🏠 Housing         $248  27%
🚗 Transport        $83   9%
❤️ Social           $69   8%
```

---

## 报表指令 | Report Commands

| Command | Description |
|---------|-------------|
| `今天报表` / `Daily report` | 日报 |
| `本周报表` / `Weekly report` | 周报 |
| `3月报表` / `March report` / `Monthly report` | 月报 |
| `2026年报` / `2026 report` / `Annual report` | 年报 |
| `餐饮明细` / `Food details` | 分类明细 |
| `预算对比` / `Budget vs actual` | 预算执行 |
| `导出CSV` / `Export CSV` | 导出数据 |
| `导出Excel` / `Export Excel` | Excel 格式 |

---

## 多货币支持 | Multi-Currency

**自动识别：** `¥` `RMB` `CNY` → CNY； `$` `USD` → USD； `€` `EUR` → EUR

**报表汇总规则：** 月报/年报/周期报表会把所有金额按配置的 `default_currency` 统一换算后再汇总与出图（图表符号随 `default_currency` 变化）。

如果缺少对应汇率，系统会在返回结果里带 `warnings`（并按默认币种原样计入），你可以提示用户补充汇率。

**汇率设置：** 用户说 "1美元=7.25元" → 更新 `exchange_rates`。

---

## 成员标签 | Member Tags

```
给小鱼儿买鞋 188元
bought milk $5 for 小鱼儿
```

成员可以是：`小鱼儿` / `baby` / `me` / `family` / `爸妈`

---

## 批量处理 | Batch Processing

Claude 识别消息中所有 `*` 或数字条目，逐条解析并一次性写入 ledger。

---

## Scripts | 脚本

| Script | Purpose |
|--------|---------|
| `scripts/ledger.py` | 核心：add / list / report / balance / config |
| `scripts/export.py` | 导出：CSV / JSON / Excel |
| `scripts/charts.py` | 可视化：pie / bar / line / report-html |

---

## 配置 | Configuration

配置文件：`~/.qclaw/workspace/expense-ledger/config.json`

```json
{
  "default_account": "default",
  "default_currency": "CNY",
  "language": "auto",
  "exchange_rates": { "USD_CNY": 7.25, "EUR_CNY": 7.85 },
  "budgets": {
    "food": 3000,
    "shopping": 2000,
    "housing": 5000
  },
  "tz": "Asia/Shanghai"
}
```

用户说 "设预算" → 引导设置各分类金额。

---

## Notes

- 金额解析：支持 `23` `23.5` `$23.5` `¥23` `USD 23` `RMB 23` `23元` `23块`
- 语言检测：分析消息中中/英文字符比例，自动选择回复语言
- 多语言混杂时：跟随消息中占比更高的语言
- 所有金额存储为 float，保留 2 位小数
- 数据存于 workspace，请定期备份或提交 git
