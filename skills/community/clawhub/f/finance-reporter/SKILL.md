---
name: finance-reporter
description: 实时财经数据推送工具。使用Yahoo Finance API获取全球股市、外汇、大宗商品、加密货币实时行情，支持定时推送到钉钉/微信。包含股票代码、货币单位、实时价格、24h前/昨收价格、涨跌幅。支持标的：纳指、道指、美元指数、黄金、比特币、沪指、恒生、日经、人民币/美元汇率、原油。
homepage: https://github.com/openclaw/finance-reporter
version: 1.0.0
author: A哥
license: MIT
metadata:
  {
    "openclaw":
      {
        "emoji": "📈",
        "requires": { "bins": ["python3", "curl"] },
        "triggers": { "scheduled": "generate_finance_report" },
        "install":
          [
            {
              "id": "python",
              "kind": "system",
              "bins": ["python3"],
              "label": "Python 3.8+",
            },
          ],
      },
  }
---

# Finance Reporter - 实时财经数据推送

📈 专业的财经数据获取与推送工具，支持全球主要金融市场实时行情。

## ✨ 功能特性

- **全球覆盖**：美股、A股、港股、日股、外汇、大宗商品、加密货币
- **实时数据**：Yahoo Finance API，数据准确及时
- **智能计算**：自动计算涨跌幅，股票显示"昨收"，加密货币显示"24h前"
- **定时推送**：支持 cron 定时任务，自动推送到钉钉/微信
- **重试机制**：网络失败自动重试3次
- **货币单位**：自动显示 USD/CNY/HKD/JPY 等货币符号

## 📊 支持标的

| 类别 | 标的 | 代码 | 货币 | 市场类型 |
|------|------|------|------|----------|
| 🇺🇸 美股指数 | 纳指 | ^IXIC | USD | 股票 |
| 🇺🇸 美股指数 | 道指 | ^DJI | USD | 股票 |
| 💵 外汇 | 美元指数 | DX-Y.NYB | - | 外汇 |
| 💵 外汇 | 人民币/美元 | CNY=X | - | 外汇 |
| 🪙 加密货币 | 比特币 | BTC-USD | USD | 加密(24h) |
| 🏆 大宗商品 | 黄金 | GC=F | USD | 期货 |
| 🏆 大宗商品 | 原油 | CL=F | USD | 期货 |
| 🇨🇳 A股 | 沪指 | 000001.SS | CNY | 股票 |
| 🇭🇰 港股 | 恒生 | ^HSI | HKD | 股票 |
| 🇯🇵 日股 | 日经 | ^N225 | JPY | 股票 |

## 🚀 快速开始

### 1. 手动获取数据

```bash
# 运行脚本获取实时数据
python3 ~/.openclaw/workspace/skills/finance-reporter/tools/finance_data.py
```

### 2. 钉钉群调用

在钉钉群中 @你的机器人：
```
@finance 获取实时财经数据
```

### 3. 配置定时任务

```bash
# 每天 01:20 自动推送
openclaw cron add \
  --name "finance_daily" \
  --schedule "20 1 * * *" \
  --command "python3 ~/.openclaw/workspace/skills/finance-reporter/tools/finance_data.py"
```

## 📋 输出格式示例

```
📊 实时财经数据 [2026-03-20 01:20]
💡 数据来源: Yahoo Finance API

🇺🇸 美股指数
----------------------------------------
📉 纳指
   代码: ^IXIC
   现价: $21,979.21
   昨收: $22,152.42
   涨跌: -173.21 (-0.78%)

📉 道指
   代码: ^DJI
   现价: $45,884.29
   昨收: $46,225.15
   涨跌: -340.86 (-0.74%)

🪙 加密货币
----------------------------------------
📉 比特币
   代码: BTC-USD
   现价: $69,296.45
   24h前: $71,245.58
   涨跌: -1,949.13 (-2.74%)
```

## ⚙️ 配置说明

### 环境要求
- Python 3.8+
- requests 库

### 安装依赖
```bash
pip3 install requests
```

### 自定义标的

编辑 `tools/finance_data.py` 中的 `SYMBOLS` 字典：

```python
SYMBOLS = {
    "纳指": {"code": "^IXIC", "currency": "USD", "market": "stock"},
    "道指": {"code": "^DJI", "currency": "USD", "market": "stock"},
    # 添加你的标的...
    "特斯拉": {"code": "TSLA", "currency": "USD", "market": "stock"},
}
```

### 市场类型说明
- `stock`：股票/指数，显示"昨收"
- `crypto`：加密货币，显示"24h前"
- `commodity`：大宗商品，显示"昨收"
- `forex`：外汇，显示"昨收"

## 📡 数据来源

- **Primary**: [Yahoo Finance API](https://finance.yahoo.com)（免费，实时）
- **数据更新**: 实时
- **API限制**: 无限制，但请合理使用

## 🔧 故障排除

### 数据获取失败
- 检查网络连接
- 脚本会自动重试3次
- 查看错误日志：`openclaw logs`

### 钉钉推送失败
- 确认钉钉插件已配置
- 检查群ID是否正确
- 查看绑定：`openclaw agents bindings`

## 📝 更新日志

### v1.0.0 (2026-03-20)
- ✅ 支持10个主要标的
- ✅ 智能涨跌幅计算
- ✅ 定时任务推送
- ✅ 钉钉集成
- ✅ 重试机制

## 🤝 贡献

欢迎提交 PR 和 Issue！

## 📄 许可证

MIT License
