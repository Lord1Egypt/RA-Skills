---
name: crypto-price
description: 查询虚拟币实时价格和历史数据，支持生成趋势图、周报和邮件推送。当用户询问虚拟币价格、加密货币行情、需要币价分析报告或定时推送时使用此技能。
---

# Crypto Price

查询主流虚拟币实时价格、历史数据，生成趋势图和周报。

## 功能特性

- ✅ 实时价格查询（支持 10+ 主流币种）
- ✅ 历史数据查询（1-365 天）
- ✅ 单币种趋势图生成
- ✅ 多币种对比图生成
- ✅ 7 天周报自动生成
- ✅ 邮件定时推送

## 使用方法

### 1. 查询当前价格

```bash
python3 skills/crypto-price/scripts/crypto_price.py <币种代码>
```

**示例：**
```bash
python3 skills/crypto-price/scripts/crypto_price.py BTC
python3 skills/crypto-price/scripts/crypto_price.py ETH
```

### 2. 查询历史价格

```bash
python3 skills/crypto-price/scripts/crypto_price.py <币种代码> --history <天数>
```

**示例：**
```bash
python3 skills/crypto-price/scripts/crypto_price.py BTC --history 3
python3 skills/crypto-price/scripts/crypto_price.py ETH --history 7
```

### 3. 生成单币种趋势图

```bash
python3 skills/crypto-price/scripts/crypto_price.py <币种代码> --chart <天数>
```

**示例：**
```bash
python3 skills/crypto-price/scripts/crypto_price.py BTC --chart 3
python3 skills/crypto-price/scripts/crypto_price.py ETH --chart 7
```

### 4. 生成多币种对比图

```bash
python3 skills/crypto-price/scripts/crypto_price.py BTC --compare <币种 1,币种 2,...> <天数>
```

**示例：**
```bash
python3 skills/crypto-price/scripts/crypto_price.py BTC --compare BTC,ETH,SOL 3
python3 skills/crypto-price/scripts/crypto_price.py BTC --compare BTC,ETH,BNB,SOL,DOGE 7
```

### 5. 生成周报并发送邮件

```bash
# 配置环境变量（首次使用）
export EMAIL_SENDER="your_email@126.com"
export EMAIL_SENDER_NAME="Your Name"
export EMAIL_PASSWORD="your_smtp_password"
export EMAIL_RECIPIENT="recipient@example.com"

# 生成并发送周报
python3 skills/crypto-price/scripts/crypto_weekly_report.py
```

**永久配置（添加到 ~/.zshrc）：**
```bash
echo 'export EMAIL_SENDER="your_email@126.com"' >> ~/.zshrc
echo 'export EMAIL_SENDER_NAME="Your Name"' >> ~/.zshrc
echo 'export EMAIL_PASSWORD="your_smtp_password"' >> ~/.zshrc
echo 'export EMAIL_RECIPIENT="recipient@example.com"' >> ~/.zshrc
source ~/.zshrc
```

**⚠️ 安全提示：**
- 不要将邮箱密码提交到 Git
- 使用 `.env` 文件或环境变量存储敏感信息
- 定期更换 SMTP 授权码

## 支持的币种

| 代码 | 币种 | 代码 | 币种 |
|------|------|------|------|
| BTC | 比特币 | SOL | Solana |
| ETH | 以太坊 | XRP | 瑞波币 |
| USDT | 泰达币 | ADA | 艾达币 |
| BNB | 币安币 | DOGE | 狗狗币 |
| DOT | 波卡币 | MATIC | Polygon |

## 输出示例

### 当前价格
```
📊 BTC 价格信息
========================================
💵 美元价格: $73,246.00
💴 人民币价格: ¥505,100.00
📈 24h 涨跌: +1.97%
🏦 市值: $1.46T
========================================
```

### 历史价格
```
📈 BTC 3 天历史价格
========================================
  03-14: $70,965.28
  03-15: $71,217.10
  03-16: $72,681.91
========================================
```

## 定时任务配置

### 每天上午 10 点发送周报

```bash
# 添加到 crontab
0 10 * * * cd /Users/admin/.openclaw/workspace && python3 skills/crypto-price/scripts/crypto_weekly_report.py
```

或使用 OpenClaw cron：
```bash
openclaw cron add --schedule "0 10 * * *" --command "python3 skills/crypto-price/scripts/crypto_weekly_report.py"
```

## 注意事项

1. **API 限制**: CoinGecko 免费 API 有速率限制（10-50 次/分钟）
2. **数据延迟**: 价格数据延迟约 1-5 分钟
3. **matplotlib**: 生成图表需要安装 matplotlib
4. **邮箱配置**: 邮件发送需要配置 126 邮箱 SMTP

## 依赖安装

```bash
# 安装 matplotlib（图表生成）
pip3 install matplotlib --break-system-packages --user

# 或
brew install python-matplotlib
```

## 文件结构

```
crypto-price/
├── SKILL.md
└── scripts/
    ├── crypto_price.py           # 主脚本（价格查询、图表生成）
    └── crypto_weekly_report.py   # 周报生成和邮件发送
```

## 数据来源

- **价格数据**: CoinGecko API (https://www.coingecko.com/)
- **免费无需 API Key**: 是
- **更新频率**: 实时（延迟 1-5 分钟）
