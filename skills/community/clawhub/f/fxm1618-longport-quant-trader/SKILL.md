---
name: longport-quant-trader
description: 长桥证券量化交易集成 - 自动超跌/动量策略 + 飞书推送 + 绩效跟踪。支持港股/美股自动交易，每 5 分钟监控，止盈止损管理。适用于想要自动化交易的个人投资者和量化爱好者。
version: 1.0.0
homepage: https://open.longportapp.com
commands:
  - /quant-start - 启动量化交易监控
  - /quant-status - 查看当前持仓和绩效
  - /quant-config - 配置策略参数
  - /quant-report - 生成交易报告
metadata: {"clawdbot":{"emoji":"💰","requires":{"bins":["python3"],"env":["LONGPORT_APP_KEY","LONGPORT_APP_SECRET","LONGPORT_ACCESS_TOKEN"]},"install":[{"id":"python3","kind":"brew","formula":"python@3.12","bins":["python3"],"label":"Install Python 3.12"}]}}
---

# longport-quant-trader v1.0

长桥证券量化交易集成 - 自动化港股/美股交易

## 核心功能

- 📈 **超跌抄底策略** - 自动检测跌幅>2.5% 的股票并买入
- 🚀 **动量追涨策略** - 自动检测涨幅>1.5% 的股票并跟进
- 🎯 **自动止盈止损** - +15% 止盈 / -8% 止损
- 📱 **飞书推送** - 实时交易通知和绩效报告
- 📊 **绩效跟踪** - 胜率/收益/回撤自动统计
- ⏰ **定时监控** - 每 5 分钟自动扫描市场

## 快速开始

### 1. 安装依赖

```bash
pip install longport python-dotenv
```

### 2. 配置 API 密钥

在 `config.py` 中填写长桥 API 凭证：

```python
LONGPORT_APP_KEY = "your_app_key"
LONGPORT_APP_SECRET = "your_app_secret"
LONGPORT_ACCESS_TOKEN = "your_access_token"
```

从 https://open.longportapp.com/account 获取

### 3. 配置飞书推送（可选）

```python
FEISHU_BOT_WEBHOOK = "your_webhook_url"
```

### 4. 启动监控

```bash
python quant_monitor.py
```

## 策略参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| momentum_threshold | +1.5% | 动量买入阈值 |
| reversion_threshold | -2.5% | 超跌买入阈值 |
| take_profit | +15% | 止盈阈值 |
| stop_loss | -8% | 止损阈值 |
| position_size_pct | 25% | 单笔仓位比例 |
| max_positions | 5 | 最大持仓数 |

## 股票池

**默认港股池：**
- 700.HK 腾讯控股
- 9988.HK 阿里巴巴
- 3690.HK 美团
- 1211.HK 比亚迪
- 9618.HK 京东

**可扩展：** 支持自定义股票池

## 输出示例

```
🔄 监控 - 14:30:00
======================================================================
💰 现金：HKD 51,320 | 净资产：HKD 798,261

📈 持仓 (3)
  9988.HK: 200 股 盈亏 HKD -20 (-0.08%)
  700.HK: 100 股 盈亏 HKD -1,100 (-2.14%)
  1211.HK: 600 股 盈亏 HKD -450 (-0.81%)

🔍 买入机会
  🟢 3690.HK 超跌 -2.8% 买入 200 股 @ HKD 73.50
  ✅ 订单 ID: 1214093530725662720

📊 绩效
  交易：3 笔
  胜率：66.7% (2 胜 1 负)
  收益：+0.52%
✅ 执行 1 笔交易
```

## 安全提示

⚠️ **重要：**
1. 保护 API 密钥，不要提交到 git
2. 模拟盘测试后再实盘
3. 设置合理的止盈止损
4. 定期备份配置文件

## 技术支持

- 邮箱：support@example.com
- 微信：quant_trader
- 文档：https://github.com/yourname/longport-quant-trader

## 更新日志

### v1.0.0 (2026-03-05)
- 🎉 首次发布
- ✅ 超跌/动量策略
- ✅ 飞书推送集成
- ✅ 绩效跟踪系统

---

**免责声明：** 本软件仅供学习研究，不构成投资建议。使用本软件进行交易需自行承担风险。
