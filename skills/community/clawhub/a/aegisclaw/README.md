# 🦞 金甲龙虾 (AegisClaw)

> 币安安全赚币与护境神将 — 既有破浪赚取 Alpha 的双钳，又有绝对守护资产的金甲

**AegisClaw** 是一个基于**最小权限原则**和**币安子账户生态**的防御型 AI 代理，专注于低风险、自动化的资产管理与套利。

## ✨ 核心特性

### 🛡️ 安全围栏
- **子账户沙盒隔离** — 推荐使用独立的子账户进行操作
- **API 权限自检** — 自动检测并警告危险权限配置
- **操作防火墙** — 滑点限制、交易频次控制

### 💰 赚币引擎
- **Launchpool/Megadrop 监控** — 智能扫描新币挖矿机会
- **零钱自动兑换** — 将小额资产自动兑换为 BNB (Dust Sweeper)
- **资金费率套利** — 现货与合约之间的无风险套利机会

### 📊 数据统计
- **余额快照记录** — 自动保存每日资产快照
- **交易历史追踪** — SQLite 数据库持久化存储
- **周收益战报** — 一键生成并分享收益报告

---

## 🚀 快速开始

### 方式一：CLI 命令行

```bash
# 1. 克隆项目
git clone https://github.com/hyy2099/aegisclaw.git
cd aegisclaw

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
# Windows: 复制 .env.example 为 .env 并编辑
# Linux/Mac:
cp .env.example .env
# 编辑 .env 填入你的币安 API Key

# 4. 运行
python main.py --check      # 安全检查
python main.py --scan       # 扫描资产
python main.py --arbitrage  # 套利扫描
python main.py --all        # 运行所有检查
```

### 方式二：OpenClaw 插件

```bash
# 1. 安装 OpenClaw
# 参考: https://clawhub.io

# 2. 安装插件
openclaw plugin install aegisclaw

# 3. 初始化
/aegisclaw init <api_key> <api_secret> [testnet]

# 4. 使用命令
/aegisclaw check       # 安全检查
/aegisclaw scan        # 扫描资产
/aegisclaw arbitrage   # 套利扫描
/aegisclaw dust        # 零钱兑换
/aegisclaw report      # 生成周报
/aegisclaw status      # 查看状态
```

### 方式三：Claude Code

Claude Code 是 Anthropic 的 CLI 工具，可以直接与 AegisClaw 集成：

**安装 Claude Code**
```bash
# macOS/Linux
curl -fsSL https://cdn.anthropic.com/install.sh | sh

# Windows (使用 scoop)
scoop install claude-code
```

**使用方式**

在 Claude Code 中：

```python
# 1. 导入并初始化
from openclaw_plugin.plugin import plugin

# 2. 初始化插件
result = plugin.initialize("your_api_key", "your_api_secret", testnet=False)
print(result["message"])

# 3. 执行命令
result = plugin.handle_command("check")
print(result["message"])

result = plugin.handle_command("scan")
print(result["message"])

result = plugin.handle_command("arbitrage")
print(result["message"])

# 4. 生成报告
result = plugin.handle_command("report")
print(result["message"])
```

**Claude Code 交互式使用**

你也可以让 Claude Code 自动帮你操作：

```
用户: 帮我检查币安账户安全状态
Claude: [自动执行] plugin.handle_command("check")

用户: 扫描一下资产，看看有没有零钱可以兑换
Claude: [自动执行] plugin.handle_command("scan"); plugin.handle_command("dust")

用户: 有没有什么套利机会？
Claude: [自动执行] plugin.handle_command("arbitrage")
```

**高级用法 - 让 AI 自动分析**

```
用户: 每天早上 8 点帮我检查套利机会，如果有大于 0.1% 的机会就告诉我
Claude: [使用 Cron 或循环自动监控]
```

---

## 📋 详细命令说明

### CLI 命令

```bash
python main.py --help                    # 显示帮助
python main.py --testnet                 # 使用测试网
python main.py --key <key> --secret <secret>  # 使用命令行参数
```

### 可用操作

| 命令 | 说明 | 示例 |
|------|------|------|
| `--check` | 运行安全围栏检查 | `python main.py --check` |
| `--scan` | 扫描闲置资产和零钱 | `python main.py --scan` |
| `--arbitrage` | 扫描资金费率套利机会 | `python main.py --arbitrage` |
| `--dust` | 执行零钱兑换 | `python main.py --dust` |
| `--report` | 生成周收益战报 | `python main.py --report` |
| `--status` | 查看当前状态 | `python main.py --status` |
| `--all` | 运行所有检查 | `python main.py --all` |

### OpenClaw 命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `init` | 初始化插件 | `/aegisclaw init <key> <secret>` |
| `check` | 安全检查 | `/aegisclaw check` |
| `scan` | 资产扫描 | `/aegisclaw scan` |
| `arbitrage` | 套利扫描 | `/aegisclaw arbitrage` |
| `dust` | 零钱兑换 | `/aegisclaw dust [BTC,ETH]` |
| `report` | 周报 | `/aegisclaw report` |
| `status` | 状态 | `/aegisclaw status` |
| `help` | 帮助 | `/aegisclaw help` |

---

## 💡 使用案例

### 案例 1：新用户安全检查

```bash
# 首次使用，运行完整检查
python main.py --all
```

**输出示例：**
```
🦞 金甲龙虾 - 币安安全赚币与护境神将
========================================

🛡️ 运行安全围栏检查...

🦞 金甲龙虾 - 安全围栏检查报告
==================================================

✅ API 连接成功

账户类型: ✅ 子账户（推荐配置）

资产摘要:
  • 资产种类: 5 种
  • 稳定币: $500.00
  • BNB: 2.5000

API 权限:
  • 已启用: SPOT
  • 🚨 危险权限: 无 (安全)

🟢 安全评分: 100/100

💡 建议:
  • 建议为 API Key 绑定 IP 白名单
```

### 案例 2：资产扫描与零钱兑换

```bash
# 扫描资产
python main.py --scan

# 兑换零钱
python main.py --dust
```

**输出示例：**
```
📊 资产扫描报告
========================================

💰 闲置资金:
  • USDT: $500.00
  • 总计: $500.00

🧹 零钱资产:
  • ETH: 0.0005 (~$2.50)
  • DOGE: 50.5 (~$7.20)

💡 建议:
  🚀 检测到 $500.00 USDT 闲置，可参与 Launchpool
  🧹 发现 2 种零钱，总价值约 $9.70

🦞 零钱兑换执行中...
✅ 兑换完成! 获得 0.0323 BNB
```

### 案例 3：资金费率套利

```bash
python main.py --arbitrage
```

**输出示例：**
```
📈 资金费率套利机会
==================================================

1. 📈 BTCUSDT
   资金费率: +0.0150%
   现货价格: $65000.00
   标记价格: $65015.00
   价格偏差: +0.02%
   预计收益: 0.0150%
   操作建议: 做多现货，做空合约，收取 0.0150% 资金费

2. 📈 ETHUSDT
   资金费率: +0.0200%
   现货价格: $3500.00
   标记价格: $3508.00
   预计收益: 0.0200%
   操作建议: 做多现货，做空合约，收取 0.0200% 资金费

⚠️ 提醒: 套利有风险，请控制仓位
```

### 案例 4：使用 Claude Code 自动化

让 Claude Code 每天早上 8 点检查并通知：

```
用户: 帮我设置一个定时任务，每天早上8点检查套利机会，如果有大于0.1%的机会就通知我

Claude: [使用 Cron 或其他调度工具设置自动化监控]
```

---

## 🔒 安全建议

### 1. 使用子账户
- 创建仅含 500-1000 USDT 的子账户
- 不要使用主账户进行操作

### 2. 限制 API 权限
```
✅ 启用: 现货交易 (SPOT)
❌ 禁用: 提现 (WITHDRAW)
❌ 禁用: 期货交易 (FUTURES)
```

### 3. 绑定 IP 白名单
- 限制 API 只能从特定 IP 访问
- 定期检查 IP 白名单

### 4. 控制资金规模
- 子账户资金建议在 1000 USDT 以内
- 使用闲置资金，不影响正常生活

---

## 📁 项目结构

```
aegisclaw/
├── main.py                    # CLI 入口
├── config.py                  # 配置文件
├── requirements.txt           # Python 依赖
├── .env.example               # 环境变量示例
├── start.bat                  # Windows 快速启动脚本
├── core/                      # 核心模块
│   ├── api_client.py          # 币安 API 客户端
│   ├── security_checker.py    # 安全检查器
│   ├── asset_scanner.py       # 资产扫描器
│   ├── funding_arbitrage.py    # 资金费率套利
│   └── report_generator.py    # 报告生成器
├── db/                        # 数据库模块
│   └── database.py            # SQLite 数据库
└── openclaw_plugin/           # OpenClaw 插件接口
    └── plugin.py              # 插件入口
```

---

## 🔧 配置说明

### .env 配置

```bash
# 币安 API 配置
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
BINANCE_TESTNET=false

# Telegram 配置（可选）
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=

# 安全配置
MAX_DAILY_TRADES=10          # 每日最大交易次数
MAX_PRICE_SLIPPAGE=0.01      # 最大价格滑点 (1%)

# 策略配置
FUNDING_RATE_THRESHOLD=0.0001  # 资金费率阈值
MIN_ARBITRAGE_PROFIT=0.001     # 最小套利利润 (0.1%)
MIN_LAUNCHPOOL_AMOUNT=10.0      # Launchpool 最小金额
MIN_DUST_THRESHOLD=10.0         # 零钱兑换最小阈值
```

---

## 🎯 项目亮点

本项目为币安「AI 建设加密」活动参赛作品，核心亮点：

1. **将安全短板转化为核心武器** — AI 主动拒绝越权操作
2. **一切收益换成 BNB** — 完美契合币安生态利益
3. **极低的落地门槛** — 使用原生 API，无需复杂模型
4. **多种使用方式** — CLI、OpenClaw、Claude Code

---

## 📜 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

🦞 **金甲龙虾** — 您的币安无风险赚币与护境神将
