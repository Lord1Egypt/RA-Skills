# BTC Price Tracker

一个比特币实时价格监控和警报系统，支持通过 Telegram 接收价格通知。

## 功能特性

- ✅ 使用 CoinGecko 免费 API 获取比特币实时价格（无需 API Key）
- ✅ 支持多货币显示（USD、CNY、SGD）
- ✅ 设置价格警报（高于/低于某个价位）
- ✅ 通过 Telegram 发送警报通知
- ✅ 命令行交互界面
- ✅ 本地 JSON 存储警报数据
- ✅ 完善的错误处理和网络超时
- ✅ 多语言支持（中文/英文）

## 安装

```bash
# 安装依赖
pip install requests

# 或者使用技能安装器
clawhub install btc-price-tracker
```

## 使用方法

### 查看当前价格

```bash
# 查看比特币价格（默认 USD）
btc-price-tracker price

# 示例输出:
# 💰 比特币当前价格：
#   USD: $67,234.56
#   CNY: ¥486,789.12
#   SGD: S$90,123.45
#   24h 变化：📈 2.34%
```

### 设置价格警报

```bash
# 当价格高于 100,000 USD 时通知
btc-price-tracker alert --name "高价警报" --price 100000 --condition above --currency USD

# 当价格低于 60,000 CNY 时通知
btc-price-tracker alert --name "低价警报" --price 60000 --condition below --currency CNY

# 参数说明:
#   --name, -n        警报名称（必填）
#   --price, -p       目标价格（必填）
#   --condition, -c   触发条件：above(高于) 或 below(低于)
#   --currency, -C    货币单位：USD, CNY, SGD（默认 USD）
```

### 查看警报列表

```bash
btc-price-tracker alerts

# 示例输出:
# 📋 当前警报列表：
# ------------------------------------------------------------
# ✅ #1 高价警报
#    条件：当价格 高于 $100,000.00
#    创建：2026-03-31T11:14:30
# ✅ #2 低价警报
#    条件：当价格 低于 ¥60,000.00
#    创建：2026-03-31T11:15:00
# ------------------------------------------------------------
```

### 删除警报

```bash
# 删除 ID 为 1 的警报
btc-price-tracker delete 1
```

### 检查警报

```bash
# 手动检查是否触发警报
btc-price-tracker check
```

## Telegram 集成

当价格警报触发时，会自动通过 Telegram 发送通知：

```
🚨 警报触发！高价警报：当前价格 $100,234.56 高于 $100,000.00
```

### 配置 Telegram

在 OpenClaw 环境中，Telegram 通知会自动通过主程序发送。确保：

1. OpenClaw Gateway 已启动
2. Telegram 频道已配置
3. 环境变量 `OPENCLAW_TELEGRAM_BOT_TOKEN` 已设置

## 环境变量

```bash
# 设置语言（zh 或 en）
export OPENCLAW_LANG=zh

# Telegram Bot Token（用于发送通知）
export OPENCLAW_TELEGRAM_BOT_TOKEN=your_bot_token
```

## 数据存储

警报数据保存在技能目录下的 `alerts.json` 文件中：

```json
[
  {
    "id": 1,
    "name": "高价警报",
    "price": 100000,
    "condition": "above",
    "currency": "USD",
    "active": true,
    "created_at": "2026-03-31T11:14:30"
  }
]
```

## API 说明

本技能使用 [CoinGecko 免费 API](https://www.coingecko.com/en/api)：

- 无需 API Key
- 免费调用限额：10-50 次/分钟
- 数据包含：USD、CNY、SGD 价格及 24 小时涨跌幅

## 错误处理

技能包含完善的错误处理：

- 🌐 网络超时（10 秒）
- 🔌 连接错误
- 📄 JSON 解析错误
- 💾 文件读写错误

所有错误都会以友好的中文/英文消息显示。

## 技术栈

- Python 3.7+
- requests（HTTP 客户端）
- json（数据持久化）
- argparse（命令行解析）

## 限制

- CoinGecko 免费 API 有调用频率限制（建议不超过 1 次/分钟）
- 警报数据仅保存在本地，不会同步到云端
- 仅支持比特币（BTC），不支持其他加密货币

## 未来计划

- [ ] 支持其他加密货币（ETH、BNB 等）
- [ ] 添加价格历史图表
- [ ] 支持邮件通知
- [ ] 添加价格趋势分析
- [ ] 支持警报组（批量管理）

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

## 作者

OpenClaw Community

---

**提示**: 定期检查价格警报，合理设置触发条件，避免频繁触发。
