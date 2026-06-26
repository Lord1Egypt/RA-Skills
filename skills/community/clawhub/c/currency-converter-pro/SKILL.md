---
name: currency-converter-pro
description: 实时汇率换算专家。支持150+货币实时汇率、批量换算、多货币对比、历史汇率查询。零API Key，免费数据源。When user asks about currency exchange, conversion rates, USD to CNY, forex, or money conversion.
---

# Currency Converter Pro
**实时汇率换算专家** | Author: Lin Hui | Version 1.0.0 | MIT License

支持150+货币实时汇率查询、批量换算、历史汇率对比。零API Key，免费数据源。

## 核心功能

- ✅ 实时汇率查询（150+货币）
- ✅ 任意金额多货币换算
- ✅ 多货币横向对比（1000美元能换多少各货币）
- ✅ 历史汇率查询
- ✅ 零API Key，免费数据源
- ✅ 支持主要货币：CNY、USD、EUR、GBP、JPY、KRW、HKD、TWD、SGD、AUD、CAD、CHF、INR等

## 数据来源

- **open.er-api.com** — 免费汇率API，无需注册，无需Key
- 数据更新：每日多次自动更新
- 覆盖范围：150+全球主流货币

## 触发词

> "100美元换多少人民币" / "今日汇率" / "美元兑日元" / "1万港币值多少人民币" / "EUR to USD" / "exchange rate" / "汇率换算" / "人民币贬值了吗" / "1000块能换多少美元" / "历史汇率"

## 使用示例

### 货币换算

**输入：** 100 USD → CNY

**输出：**
```json
{
  "from": "USD",
  "to": "CNY",
  "amount": 100,
  "rate": 6.841274,
  "result": 684.13,
  "timestamp": "Mon, 27 Apr 2026",
  "provider": "open.er-api.com"
}
```

### 多货币横向对比

**输入：** 1000 USD 换所有主流货币

**输出：**
```json
{
  "from": "USD",
  "amount": 1000,
  "conversions": [
    {"currency": "CNY", "amount": 6841.27},
    {"currency": "EUR", "amount": 854.23},
    {"currency": "GBP", "amount": 740.22},
    {"currency": "JPY", "amount": 159540.6},
    ...
  ]
}
```

### 历史汇率

**输入：** 100 USD → CNY，2024-01-01

**输出：** 当天的美元兑人民币汇率（可用于对比汇率变化）

## 技术实现

```bash
# 单币种换算
python3 scripts/currency.py convert <金额> <源货币> <目标货币>

# 汇率列表
python3 scripts/currency.py rates <基准货币>

# 多货币横向对比
python3 scripts/currency.py top <金额> <源货币>

# 历史汇率
python3 scripts/currency.py historical <金额> <源货币> <目标货币> <日期YYYY-MM-DD>
```

## 支持货币（部分）

| 货币代码 | 名称 |
|---------|------|
| CNY | 人民币 |
| USD | 美元 |
| EUR | 欧元 |
| GBP | 英镑 |
| JPY | 日元 |
| KRW | 韩元 |
| HKD | 港币 |
| TWD | 新台币 |
| SGD | 新加坡元 |
| AUD | 澳元 |
| CAD | 加元 |
| CHF | 瑞士法郎 |
| INR | 印度卢比 |
| THB | 泰铢 |
| MYR | 林吉特 |
| PHP | 菲律宾比索 |
| VND | 越南盾 |
| IDR | 印尼盾 |
| AED | 阿联酋迪拉姆 |
| SAR | 沙特里亚尔 |

## 常见场景

| 场景 | 命令 |
|------|------|
| 海淘价格换算 | `convert 100 USD CNY` |
| 出国前准备 | `top 10000 CNY` |
| 汇率对比 | `rates USD` |
| 保值分析 | `historical 1000 USD CNY 2024-01-01` |

## 更新日志

### v1.0.0 (2026-04)
- 首发版本
- 150+货币实时汇率
- 零API Key，免费数据源
- 支持历史汇率查询

## ⚠️ Disclaimer

This tool is provided "as is" for informational purposes only. Data accuracy is not guaranteed. Not financial, legal, or professional advice. Always verify critical information from official sources.

本工具仅供信息参考，不保证数据完全准确，不构成任何金融/法律/专业建议。请以官方来源为准。
