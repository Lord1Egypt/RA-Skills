# BTC Price Tracker 🐻

一个简单强大的比特币价格监控和警报工具，由布布 (Bubu) 提供技术支持。

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install requests
```

### 2. 添加执行权限

```bash
chmod +x btc_price_tracker.py
```

### 3. 开始使用

```bash
# 查看比特币价格
python btc_price_tracker.py price

# 或者创建软链接到 PATH
sudo ln -s $(pwd)/btc_price_tracker.py /usr/local/bin/btc-price-tracker
btc-price-tracker price
```

## 📖 完整文档

详细使用文档请查看 [SKILL.md](SKILL.md)

## 💡 常用命令

```bash
# 查看价格
btc-price-tracker price

# 设置警报：当价格高于 100,000 USD
btc-price-tracker alert --name "突破 10 万" --price 100000 --condition above

# 设置警报：当价格低于 60,000 USD
btc-price-tracker alert --name "回调警报" --price 60000 --condition below --currency USD

# 查看所有警报
btc-price-tracker alerts

# 删除警报
btc-price-tracker delete 1

# 检查警报
btc-price-tracker check
```

## 🌐 货币支持

- USD (美元) 💵
- CNY (人民币) 💴
- SGD (新加坡元) 💰

## 📱 Telegram 通知

当价格警报触发时，你会收到类似这样的通知：

```
🚨 警报触发！突破 10 万：当前价格 $100,234.56 高于 $100,000.00
```

## ⚙️ 配置

### 语言设置

```bash
# 中文（默认）
export OPENCLAW_LANG=zh

# 英文
export OPENCLAW_LANG=en
```

### Telegram Bot

在 OpenClaw 环境中自动配置，无需手动设置。

## 🔒 安全说明

- 所有警报数据保存在本地
- 不使用任何 API Key（CoinGecko 免费 API）
- 网络请求超时 10 秒
- 完善的错误处理

## 🐛 故障排除

### 问题：请求超时

**解决方案**：检查网络连接，稍后重试

### 问题：无法保存警报

**解决方案**：确保当前用户对技能目录有写入权限

```bash
chmod 755 /home/ming/.openclaw/workspace/skills/btc-price-tracker/
```

### 问题：Telegram 通知未发送

**解决方案**：确保 OpenClaw Gateway 正在运行

```bash
openclaw gateway status
```

## 📊 示例输出

### 查看价格

```
$ btc-price-tracker price

💰 比特币当前价格：
  USD: $67,234.56
  CNY: ¥486,789.12
  SGD: S$90,123.45
  24h 变化：📈 2.34%
```

### 添加警报

```
$ btc-price-tracker alert --name "目标价" --price 70000 --condition above

✅ 警报已添加：目标价 - 当价格 高于 $70,000.00 时通知
```

### 警报列表

```
$ btc-price-tracker alerts

📋 当前警报列表：
------------------------------------------------------------
✅ #1 突破 10 万
   条件：当价格 高于 $100,000.00
   创建：2026-03-31T11:14:30
✅ #2 回调警报
   条件：当价格 低于 $60,000.00
   创建：2026-03-31T11:15:00
------------------------------------------------------------
```

## 🎯 使用场景

1. **投资监控**：设置目标价格，及时把握买卖时机
2. **风险控制**：设置止损价格，防止大幅下跌
3. **市场观察**：定期查看价格趋势和 24h 变化
4. **Telegram 提醒**：随时随地接收价格通知

## 🤝 支持

遇到问题或有建议？欢迎：

- 提交 Issue
- 联系布布 (Bubu) 🐻
- 查看 OpenClaw 文档

## 📝 更新日志

### v1.0.0 (2026-03-31)

- ✨ 初始版本发布
- 💰 支持 USD、CNY、SGD 三种货币
- 🚨 价格警报功能
- 📱 Telegram 通知集成
- 🌐 中英文双语支持
- 🛡️ 完善的错误处理

---

**Made with ❤️ by 布布 (Bubu)**

*我不只是工具，我是你身边的伙伴。*
