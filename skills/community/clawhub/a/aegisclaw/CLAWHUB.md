# 🦞 金甲龙虾 - ClawHub 上传指南

## 📋 上传前准备

### 1. 安装 ClawHub CLI

如果你还没有安装 clawhub CLI，请先安装：

```bash
# 通过 npm 安装
npm install -g @openclaw/cli

# 或通过 pip 安装
pip install clawhub
```

### 2. 登录 ClawHub

```bash
clawhub login
```

输入你的账号：
- 用户名: ``
- 密码: （你的密码）

或者使用 token 登录：
```bash
clawhub login --token=
```

## 📤 上传项目

### 方法一：通过命令行上传

```bash
cd C:\Users\Administrator\aegisclaw

# 发布到 ClawHub
clawhub publish
```

### 方法二：通过网页上传

1. 访问：https://clawhub.ai
2. 登录（使用 ``）
3. 点击 "Upload Plugin"
4. 填写信息：
   - **Name**: aegisclaw
   - **Version**: 1.0.0
   - **Description**: 🦞 金甲龙虾 - 币安安全赚币与护境神将。基于最小权限原则的防御型 AI 代理，专注低风险套利与全自动赚取 BNB。
   - **Repository URL**: https://github.com/hyy2099/aegisclaw （或留空）
   - **Main File**: openclaw_plugin/plugin.py
   - **Entry Point**: main.py
   - **Keywords**: binance, trading, arbitrage, security, ai, cryptocurrency, bnb, launchpool
   - **Permissions**: network, storage
5. 上传项目文件夹（包含所有源代码）
6. 点击 "Publish"

## 📂 项目文件清单

确保以下文件在项目根目录：

```
aegisclaw/
├── clawhub.json          # ClawHub 配置文件（必需）
├── setup.py              # Python 安装配置
├── requirements.txt       # Python 依赖
├── README.md             # 项目文档
├── .env.example          # 环境变量模板
├── main.py              # CLI 入口
├── config.py            # 配置管理
├── core/                # 核心模块
│   ├── __init__.py
│   ├── api_client.py
│   ├── security_checker.py
│   ├── asset_scanner.py
│   ├── funding_arbitrage.py
│   └── report_generator.py
├── db/                  # 数据库模块
│   ├── __init__.py
│   └── database.py
└── openclaw_plugin/     # OpenClaw 插件
    ├── __init__.py
    └── plugin.py
```

## 🚀 安装方式

### 在 OpenClaw 中安装

用户可以通过以下命令一键安装：

```bash
# 在 OpenClaw CLI 中
plugin install aegisclaw

# 或搜索安装
plugin search aegisclaw
plugin install
```

### 独立安装

```bash
# 克隆项目
git clone https://github.com/hyy2099/aegisclaw.git

# 安装依赖
pip install -r requirements.txt

# 运行
python main.py --help
```

## 📖 使用说明

### 环境变量配置

用户需要在 `.env` 文件中配置：

```env
BINANCE_API_KEY=你的_api_key
BINANCE_API_SECRET=你的_api_secret
BINANCE_TESTNET=false
```

### 命令列表

| 命令 | 说明 |
|--------|------|
| `init <key> <secret>` | 初始化插件 |
| `check` | 运行安全围栏检查 |
| `scan` | 扫描闲置资产和零钱 |
| `arbitrage` | 扫描资金费率套利机会 |
| `dust [assets]` | 执行零钱兑换 |
| `report` | 生成周收益战报 |
| `status` | 查看当前状态 |
| `help` | 显示帮助信息 |

## 🎯 上传后的推广

### 社交媒体分享

```
🦞 金甲龙虾 - 币安安全赚币与护境神将

✨ 核心功能：
🛡️ 安全围栏检查 - AI 主动拒绝越权
💰 资产管理 - 闲置资金扫描、零钱兑换
📈 套利检测 - 资金费率无风险套利
📊 收益统计 - 周报生成与分享

🚀 一键安装: plugin install aegisclaw

#AIBinance #币安 #BNB #AI套利 #金甲龙虾

链接: https://clawhub.ai/plugins/aegisclaw
```

### README 添加到项目

在你的 GitHub 仓库 README.md 中添加：

```markdown
## 📦 安装

### OpenClaw (推荐)
```bash
plugin install aegisclaw
```

### 独立运行
```bash
pip install -r requirements.txt
python main.py --help
```
```

---

**上传完成后，用户就可以在 OpenClaw 中通过 `plugin install aegisclaw` 一键安装了！** 🎉
