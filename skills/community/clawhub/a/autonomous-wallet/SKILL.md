---
name: autonomous-wallet
description: Self-healing crypto wallet for AI agents with intent-based execution and social recovery | AI 代理的自我修复加密钱包，支持意图执行和社交恢复
tags: [crypto-wallet, ai-agent, web3, ethereum, intent-execution, social-recovery, self-healing, blockchain, defi, smart-wallet, autonomous]
requires:
  env_vars:
    - name: PRIVATE_KEY
      description: Ethereum private key for wallet operations (optional, can use mnemonic) | 以太坊私钥（可选，也可使用助记词）
      optional: true
    - name: MNEMONIC
      description: 12/24-word recovery phrase (alternative to private key) | 12/24 词助记词（私钥的替代方案）
      optional: true
    - name: RPC_URL
      description: Custom RPC endpoint URL (optional, defaults provided) | 自定义 RPC 端点（可选，有默认值）
      optional: true
    - name: NETWORK
      description: Target blockchain network (mainnet, sepolia, polygon, etc.) | 目标区块链网络
      optional: true
    - name: ETHERSCAN_API_KEY
      description: Etherscan API key for transaction verification (optional) | Etherscan API 密钥（可选）
      optional: true
  tools:
    - node>=18
    - npm
  packages:
    - name: openclaw-autonomous-wallet
      source: npm
      version: ">=0.1.0"
      verified_repo: https://github.com/ZhenRobotics/openclaw-autonomous-wallet
---

# 🔐 Autonomous Wallet Skill | 自主钱包技能

**English** | [中文](#中文版本)

---

## English Version

Self-healing crypto wallet for AI agents with intent-based execution and social recovery mechanisms.

### 🔒 Security & Trust

This skill is **safe and verified**:
- ✅ All wallet operations run **locally** on your machine
- ✅ **No proprietary backend** - direct blockchain interaction
- ✅ Source code is **open source** and auditable
- ✅ Uses official **npm package** (openclaw-autonomous-wallet)
- ✅ **Your keys, your control** - private keys never leave your device
- ✅ **No data collection** - complete privacy
- ✅ **Verified repository**: github.com/ZhenRobotics/openclaw-autonomous-wallet

**Required Access**:
- **Local wallet**: Private key or mnemonic phrase (stored locally)
- **Blockchain RPC**: Public RPC endpoints (Infura, Alchemy, or custom)
- **Optional APIs**: Etherscan for transaction verification (your API key)

### ✨ Key Features

#### 🤖 Intent-Based Execution
Transform natural language into blockchain operations:
- "Send 0.1 ETH to vitalik.eth"
- "Swap 100 USDC to ETH on Uniswap"
- "Stake 10 ETH with validator"
- AI-powered intent parsing with context awareness

#### 🔄 Self-Healing Mechanisms
Automatic error recovery and optimization:
- Failed transaction detection and retry
- Dynamic gas price adjustment
- Network congestion handling
- Smart nonce management
- Transaction simulation before execution

#### 👥 Social Recovery
Guardian-based wallet recovery:
- Multi-signature guardian system
- Threshold-based approvals (e.g., 2-of-3)
- Time-locked recovery procedures
- Emergency access protocols
- Zero-knowledge proof options

#### 🛡️ Security First
Built with security as priority:
- Hardware wallet support (Ledger, Trezor)
- Encrypted local key storage
- Transaction simulation and validation
- Rate limiting and anomaly detection
- Daily spending limits

#### 🌐 Multi-Chain Support
Works across major blockchains:
- Ethereum (Mainnet, Sepolia, Goerli)
- Polygon (Mumbai, Mainnet)
- Arbitrum
- Optimism
- Base
- And more...

### 📦 Installation

#### Prerequisites

```bash
# Check Node.js (requires >= 18)
node --version

# Check npm
npm --version
```

#### Install via npm (Recommended)

```bash
# Install globally
npm install -g openclaw-autonomous-wallet

# Verify installation
autonomous-wallet --version
```

#### Install via ClawHub

```bash
# Install skill
clawhub install ZhenStaff/autonomous-wallet

# Then install npm package
npm install -g openclaw-autonomous-wallet
```

### 🚀 Quick Start

#### Step 1: Initialize Wallet

```bash
# Create new wallet
autonomous-wallet init

# Or import existing wallet
autonomous-wallet import --mnemonic "your twelve word mnemonic phrase..."

# Or use private key
export PRIVATE_KEY="0x..."
autonomous-wallet init --from-env
```

#### Step 2: Execute Intents

```bash
# Simple transfer
autonomous-wallet execute "Send 0.1 ETH to 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"

# Token swap
autonomous-wallet execute "Swap 100 USDC to ETH"

# Check balance
autonomous-wallet balance

# View transaction history
autonomous-wallet history
```

#### Step 3: Setup Social Recovery (Recommended)

```bash
# Configure guardians
autonomous-wallet recovery setup \
  --guardian1 0xGuardian1Address \
  --guardian2 0xGuardian2Address \
  --guardian3 0xGuardian3Address \
  --threshold 2 \
  --timelock 7d
```

### 📋 Commands

#### Wallet Management

```bash
# Initialize wallet
autonomous-wallet init

# Import wallet
autonomous-wallet import --mnemonic "..." --private-key "0x..."

# Check balance
autonomous-wallet balance [--token TOKEN_ADDRESS]

# View transaction history
autonomous-wallet history [--limit 10]

# Export wallet info
autonomous-wallet export --encrypted
```

#### Intent Execution

```bash
# Execute natural language command
autonomous-wallet execute "INTENT_STRING"

# Examples:
autonomous-wallet execute "Send 1 ETH to alice.eth"
autonomous-wallet execute "Swap 100 USDC to WETH on Uniswap"
autonomous-wallet execute "Approve Uniswap to spend 1000 USDC"
autonomous-wallet execute "Stake 10 ETH"
```

#### Social Recovery

```bash
# Setup recovery
autonomous-wallet recovery setup --guardians 3 --threshold 2

# Initiate recovery (as guardian)
autonomous-wallet recovery initiate --new-owner 0x...

# Approve recovery (as guardian)
autonomous-wallet recovery approve --request-id REQUEST_ID

# Execute recovery (after timelock)
autonomous-wallet recovery execute --request-id REQUEST_ID

# Cancel recovery
autonomous-wallet recovery cancel --request-id REQUEST_ID
```

#### Security & Configuration

```bash
# Set daily limit
autonomous-wallet config set-limit 10 ETH

# Set max gas price
autonomous-wallet config set-max-gas 100 gwei

# Enable/disable simulation
autonomous-wallet config simulation true

# View current config
autonomous-wallet config show
```

### 🔧 Configuration

#### Environment Variables

```bash
# Network Configuration
export NETWORK=mainnet              # ethereum network
export RPC_URL=https://...          # custom RPC endpoint

# Wallet Configuration
export PRIVATE_KEY=0x...            # private key
export MNEMONIC="word1 word2..."    # or mnemonic

# Security Settings
export MAX_GAS_PRICE=100            # max gas in gwei
export DAILY_LIMIT=10               # daily limit in ETH
export SIMULATION_REQUIRED=true     # require simulation

# Social Recovery
export GUARDIAN_1=0x...
export GUARDIAN_2=0x...
export GUARDIAN_3=0x...
export RECOVERY_THRESHOLD=2

# Optional APIs
export ETHERSCAN_API_KEY=...        # for verification
export ALCHEMY_API_KEY=...          # for enhanced RPC
```

#### Configuration File

Create `~/.autonomous-wallet/config.json`:

```json
{
  "network": "mainnet",
  "rpcUrl": "https://eth-mainnet.alchemyapi.io/v2/YOUR_KEY",
  "security": {
    "maxGasPrice": 100,
    "dailyLimit": "10000000000000000000",
    "simulationRequired": true,
    "rateLimit": {
      "enabled": true,
      "transactionsPerHour": 10
    }
  },
  "recovery": {
    "guardians": [
      "0xGuardian1...",
      "0xGuardian2...",
      "0xGuardian3..."
    ],
    "threshold": 2,
    "timelock": 604800
  }
}
```

### 💡 Use Cases

#### 1. AI Agent Treasury Management

```typescript
import { AutonomousWallet } from 'openclaw-autonomous-wallet';

const wallet = new AutonomousWallet({
  network: 'mainnet',
  privateKey: process.env.PRIVATE_KEY
});

// AI agent manages project funds automatically
await wallet.execute({
  intent: "Pay monthly salaries to team members",
  context: {
    team: [
      { address: '0x...', amount: '5000 USDC' },
      { address: '0x...', amount: '4000 USDC' }
    ]
  }
});
```

#### 2. DeFi Strategy Execution

```typescript
// Complex DeFi operations with automatic retry
await wallet.execute({
  intent: "Swap 10 ETH to USDC and provide liquidity to Uniswap V3",
  options: {
    slippage: 0.5,
    autoRetry: true,
    maxRetries: 3
  }
});
```

#### 3. Automated Portfolio Rebalancing

```typescript
// Monitor and rebalance portfolio
await wallet.execute({
  intent: "Rebalance portfolio to 60% ETH, 30% USDC, 10% WBTC",
  context: {
    currentPortfolio: await wallet.getPortfolio(),
    targetAllocation: { ETH: 0.6, USDC: 0.3, WBTC: 0.1 }
  }
});
```

### 📤 Output

Commands generate structured outputs:

```json
{
  "success": true,
  "txHash": "0x...",
  "gasUsed": "21000",
  "effectiveGasPrice": "20000000000",
  "blockNumber": 12345678,
  "confirmations": 1,
  "intent": "Send 0.1 ETH to vitalik.eth",
  "timestamp": 1234567890
}
```

### 🧪 Testing

```bash
# Test on Sepolia testnet
export NETWORK=sepolia
autonomous-wallet test

# Simulate transaction without executing
autonomous-wallet simulate "Send 1 ETH to 0x..."

# Dry run with detailed output
autonomous-wallet execute "Swap 100 USDC to ETH" --dry-run
```

### 🐛 Troubleshooting

#### Transaction Failed
✅ **Auto-retry enabled** - System automatically retries with adjusted gas

#### Insufficient Gas
- Check gas price with: `autonomous-wallet gas-price`
- Increase max gas: `autonomous-wallet config set-max-gas 150`

#### Network Issues
- Verify RPC endpoint: `autonomous-wallet network check`
- Switch to backup RPC: `export RPC_URL=https://backup-rpc...`

#### Guardian Recovery
- Verify guardian addresses are correct
- Check timelock period hasn't expired
- Ensure threshold is met (e.g., 2-of-3 approvals)

### 📊 Performance

| Operation | Time | Gas Cost |
|-----------|------|----------|
| Simple Transfer | ~2s | ~21,000 |
| Token Swap | ~5s | ~150,000 |
| Social Recovery Setup | ~10s | ~200,000 |
| Intent Parsing | <1s | 0 (off-chain) |

### 🔗 Links

- **GitHub**: https://github.com/ZhenRobotics/openclaw-autonomous-wallet
- **npm**: https://www.npmjs.com/package/openclaw-autonomous-wallet
- **Documentation**: https://docs.openclaw.ai/wallet
- **Issues**: https://github.com/ZhenRobotics/openclaw-autonomous-wallet/issues
- **Discord**: https://discord.gg/openclaw

### 📄 License

MIT License - See LICENSE file for details

---

## 中文版本

**[English](#english-version)** | 中文

---

AI 代理的自我修复加密钱包，支持基于意图的执行和社交恢复机制。

### 🔒 安全与信任

此技能**安全且经过验证**：
- ✅ 所有钱包操作在您的**本地机器**上运行
- ✅ **无自有后端** - 直接与区块链交互
- ✅ 源代码**开源**且可审计
- ✅ 使用官方 **npm 包**（openclaw-autonomous-wallet）
- ✅ **您的密钥，您的控制** - 私钥永不离开您的设备
- ✅ **无数据收集** - 完全隐私
- ✅ **已验证的仓库**: github.com/ZhenRobotics/openclaw-autonomous-wallet

**所需访问**：
- **本地钱包**: 私钥或助记词（本地存储）
- **区块链 RPC**: 公共 RPC 端点（Infura、Alchemy 或自定义）
- **可选 API**: Etherscan 用于交易验证（您的 API 密钥）

### ✨ 核心功能

#### 🤖 基于意图的执行
将自然语言转换为区块链操作：
- "发送 0.1 ETH 给 vitalik.eth"
- "在 Uniswap 将 100 USDC 兑换为 ETH"
- "质押 10 ETH"
- AI 驱动的意图解析，具有上下文感知能力

#### 🔄 自我修复机制
自动错误恢复和优化：
- 失败交易检测和重试
- 动态 gas 价格调整
- 网络拥堵处理
- 智能 nonce 管理
- 执行前交易模拟

#### 👥 社交恢复
基于守护者的钱包恢复：
- 多签名守护者系统
- 基于阈值的批准（如 2/3）
- 时间锁定恢复流程
- 紧急访问协议
- 零知识证明选项

#### 🛡️ 安全优先
以安全为首要考虑构建：
- 硬件钱包支持（Ledger、Trezor）
- 加密本地密钥存储
- 交易模拟和验证
- 速率限制和异常检测
- 每日支出限额

#### 🌐 多链支持
支持主要区块链：
- Ethereum（主网、Sepolia、Goerli）
- Polygon（Mumbai、主网）
- Arbitrum
- Optimism
- Base
- 更多...

### 📦 安装

#### 前置要求

```bash
# 检查 Node.js（需要 >= 18）
node --version

# 检查 npm
npm --version
```

#### 通过 npm 安装（推荐）

```bash
# 全局安装
npm install -g openclaw-autonomous-wallet

# 验证安装
autonomous-wallet --version
```

#### 通过 ClawHub 安装

```bash
# 安装技能
clawhub install ZhenStaff/autonomous-wallet

# 然后安装 npm 包
npm install -g openclaw-autonomous-wallet
```

### 🚀 快速开始

#### 步骤 1: 初始化钱包

```bash
# 创建新钱包
autonomous-wallet init

# 或导入现有钱包
autonomous-wallet import --mnemonic "你的 12 个助记词..."

# 或使用私钥
export PRIVATE_KEY="0x..."
autonomous-wallet init --from-env
```

#### 步骤 2: 执行意图

```bash
# 简单转账
autonomous-wallet execute "发送 0.1 ETH 到 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"

# 代币兑换
autonomous-wallet execute "兑换 100 USDC 为 ETH"

# 查看余额
autonomous-wallet balance

# 查看交易历史
autonomous-wallet history
```

#### 步骤 3: 设置社交恢复（推荐）

```bash
# 配置守护者
autonomous-wallet recovery setup \
  --guardian1 0x守护者1地址 \
  --guardian2 0x守护者2地址 \
  --guardian3 0x守护者3地址 \
  --threshold 2 \
  --timelock 7d
```

### 📋 命令

#### 钱包管理

```bash
# 初始化钱包
autonomous-wallet init

# 导入钱包
autonomous-wallet import --mnemonic "..." --private-key "0x..."

# 查看余额
autonomous-wallet balance [--token 代币地址]

# 查看交易历史
autonomous-wallet history [--limit 10]

# 导出钱包信息
autonomous-wallet export --encrypted
```

#### 意图执行

```bash
# 执行自然语言命令
autonomous-wallet execute "意图字符串"

# 示例：
autonomous-wallet execute "发送 1 ETH 给 alice.eth"
autonomous-wallet execute "在 Uniswap 将 100 USDC 兑换为 WETH"
autonomous-wallet execute "授权 Uniswap 使用 1000 USDC"
autonomous-wallet execute "质押 10 ETH"
```

#### 社交恢复

```bash
# 设置恢复
autonomous-wallet recovery setup --guardians 3 --threshold 2

# 发起恢复（作为守护者）
autonomous-wallet recovery initiate --new-owner 0x...

# 批准恢复（作为守护者）
autonomous-wallet recovery approve --request-id 请求ID

# 执行恢复（时间锁后）
autonomous-wallet recovery execute --request-id 请求ID

# 取消恢复
autonomous-wallet recovery cancel --request-id 请求ID
```

#### 安全与配置

```bash
# 设置每日限额
autonomous-wallet config set-limit 10 ETH

# 设置最大 gas 价格
autonomous-wallet config set-max-gas 100 gwei

# 启用/禁用模拟
autonomous-wallet config simulation true

# 查看当前配置
autonomous-wallet config show
```

### 🔧 配置

#### 环境变量

```bash
# 网络配置
export NETWORK=mainnet              # 以太坊网络
export RPC_URL=https://...          # 自定义 RPC 端点

# 钱包配置
export PRIVATE_KEY=0x...            # 私钥
export MNEMONIC="词1 词2..."        # 或助记词

# 安全设置
export MAX_GAS_PRICE=100            # 最大 gas（gwei）
export DAILY_LIMIT=10               # 每日限额（ETH）
export SIMULATION_REQUIRED=true     # 需要模拟

# 社交恢复
export GUARDIAN_1=0x...
export GUARDIAN_2=0x...
export GUARDIAN_3=0x...
export RECOVERY_THRESHOLD=2

# 可选 API
export ETHERSCAN_API_KEY=...        # 用于验证
export ALCHEMY_API_KEY=...          # 用于增强 RPC
```

### 💡 使用案例

#### 1. AI 代理资金管理

```typescript
import { AutonomousWallet } from 'openclaw-autonomous-wallet';

const wallet = new AutonomousWallet({
  network: 'mainnet',
  privateKey: process.env.PRIVATE_KEY
});

// AI 代理自动管理项目资金
await wallet.execute({
  intent: "支付团队成员月薪",
  context: {
    team: [
      { address: '0x...', amount: '5000 USDC' },
      { address: '0x...', amount: '4000 USDC' }
    ]
  }
});
```

#### 2. DeFi 策略执行

```typescript
// 复杂 DeFi 操作，自动重试
await wallet.execute({
  intent: "将 10 ETH 兑换为 USDC 并提供 Uniswap V3 流动性",
  options: {
    slippage: 0.5,
    autoRetry: true,
    maxRetries: 3
  }
});
```

### 🐛 故障排除

#### 交易失败
✅ **已启用自动重试** - 系统自动调整 gas 后重试

#### Gas 不足
- 检查 gas 价格：`autonomous-wallet gas-price`
- 提高最大 gas：`autonomous-wallet config set-max-gas 150`

#### 网络问题
- 验证 RPC 端点：`autonomous-wallet network check`
- 切换备用 RPC：`export RPC_URL=https://backup-rpc...`

### 🔗 链接

- **GitHub**: https://github.com/ZhenRobotics/openclaw-autonomous-wallet
- **npm**: https://www.npmjs.com/package/openclaw-autonomous-wallet
- **文档**: https://docs.openclaw.ai/wallet
- **问题反馈**: https://github.com/ZhenRobotics/openclaw-autonomous-wallet/issues

### 📄 许可证

MIT License - 详见 LICENSE 文件

---

**Version | 版本**: 0.1.0
**Last Updated | 最后更新**: 2026-03-12
**Maintainer | 维护者**: ZhenStaff
