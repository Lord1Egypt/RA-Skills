# Autonomous Wallet Skill | 自主钱包技能

**English** | [中文](#中文版本)

---

## English Version

Self-healing crypto wallet for AI agents with intent-based execution and social recovery.

### Version

**Current Version**: v0.1.0
**Release Date**: 2026-03-12
**Status**: Early Development (Alpha)

### What is Autonomous Wallet?

A smart crypto wallet that:
- **Understands natural language** - "Send 0.1 ETH to alice.eth"
- **Recovers from errors automatically** - Failed transactions? Auto-retry with adjusted gas
- **Enables social recovery** - Lost access? Your trusted guardians can help
- **Works for AI agents** - Built for autonomous operation

Perfect for:
- 🤖 AI agent treasury management
- 💼 Automated DeFi strategies
- 🔐 Secure multi-sig operations
- 🌐 Cross-chain asset management

### Features

- **Intent-Based Execution**: Natural language → Blockchain operations
- **Self-Healing**: Automatic retry with gas optimization
- **Social Recovery**: Guardian-based wallet recovery (2-of-3, 3-of-5, etc.)
- **Security First**: Hardware wallet support, encrypted storage, rate limiting
- **Multi-Chain**: Ethereum, Polygon, Arbitrum, Optimism, Base, and more

### Quick Start

#### Installation

```bash
# Install globally
npm install -g openclaw-autonomous-wallet

# Verify
autonomous-wallet --version
```

#### Initialize Wallet

```bash
# Create new wallet
autonomous-wallet init

# Import existing wallet
autonomous-wallet import --mnemonic "your twelve word phrase..."
```

#### Execute Intents

```bash
# Simple transfer
autonomous-wallet execute "Send 0.1 ETH to vitalik.eth"

# Token swap
autonomous-wallet execute "Swap 100 USDC to ETH on Uniswap"

# Check balance
autonomous-wallet balance
```

#### Setup Social Recovery

```bash
autonomous-wallet recovery setup \
  --guardian1 0xGuardian1... \
  --guardian2 0xGuardian2... \
  --guardian3 0xGuardian3... \
  --threshold 2 \
  --timelock 7d
```

### Configuration

#### Environment Variables

```bash
# Wallet
export PRIVATE_KEY=0x...          # Your private key
export MNEMONIC="word1 word2..."  # Or mnemonic phrase

# Network
export NETWORK=mainnet            # mainnet, sepolia, polygon, etc.
export RPC_URL=https://...        # Custom RPC (optional)

# Security
export MAX_GAS_PRICE=100          # Max gas in gwei
export DAILY_LIMIT=10             # Daily limit in ETH
export SIMULATION_REQUIRED=true   # Require simulation before execution
```

### Commands

| Command | Description |
|---------|-------------|
| `init` | Initialize new wallet |
| `import` | Import existing wallet |
| `balance` | Check wallet balance |
| `history` | View transaction history |
| `execute "INTENT"` | Execute natural language command |
| `recovery setup` | Setup social recovery guardians |
| `recovery initiate` | Start recovery process (as guardian) |
| `recovery approve` | Approve recovery request (as guardian) |
| `config show` | View current configuration |

### Use Cases

#### 1. AI Agent Treasury

```typescript
import { AutonomousWallet } from 'openclaw-autonomous-wallet';

const wallet = new AutonomousWallet({ network: 'mainnet' });

// AI automatically pays team salaries
await wallet.execute({
  intent: "Pay monthly salaries to team",
  context: { team: addresses }
});
```

#### 2. DeFi Automation

```bash
# Complex DeFi operations
autonomous-wallet execute "Swap 10 ETH to USDC and provide liquidity to Uniswap"
```

#### 3. Portfolio Management

```bash
# Rebalance portfolio
autonomous-wallet execute "Rebalance to 60% ETH, 30% USDC, 10% WBTC"
```

### Output Example

```json
{
  "success": true,
  "txHash": "0x123...",
  "gasUsed": "21000",
  "intent": "Send 0.1 ETH to vitalik.eth",
  "timestamp": 1234567890
}
```

### Performance

| Operation | Time | Gas Cost |
|-----------|------|----------|
| Simple Transfer | ~2s | ~21,000 |
| Token Swap | ~5s | ~150,000 |
| Social Recovery Setup | ~10s | ~200,000 |

### Security

✅ **Your keys, your control** - Private keys stored locally only
✅ **Transaction simulation** - Test before executing
✅ **Rate limiting** - Protect against rapid spending
✅ **Daily limits** - Set maximum daily spending
✅ **Guardian recovery** - Social backup for lost keys

### Troubleshooting

#### Transaction Failed
- ✅ Auto-retry enabled by default
- Check gas price: `autonomous-wallet gas-price`
- Increase max gas: `autonomous-wallet config set-max-gas 150`

#### Network Issues
- Verify RPC: `autonomous-wallet network check`
- Try backup RPC: `export RPC_URL=https://...`

#### Guardian Recovery
- Verify guardian addresses
- Check timelock period (default 7 days)
- Ensure threshold met (e.g., 2 out of 3 approvals)

### Links

- **GitHub**: https://github.com/ZhenRobotics/openclaw-autonomous-wallet
- **npm**: https://www.npmjs.com/package/openclaw-autonomous-wallet
- **Documentation**: https://docs.openclaw.ai/wallet
- **Issues**: https://github.com/ZhenRobotics/openclaw-autonomous-wallet/issues
- **Discord**: https://discord.gg/openclaw

### Support

For help:
1. Check [GitHub Issues](https://github.com/ZhenRobotics/openclaw-autonomous-wallet/issues)
2. Read [full documentation](https://docs.openclaw.ai/wallet)
3. Join [Discord community](https://discord.gg/openclaw)

### License

MIT License - See LICENSE file for details

### Disclaimer

⚠️ **Early Development** - This is alpha software (v0.1.0)
- NOT audited for production use
- Use testnets before mainnet
- Always backup your keys
- Test recovery procedures

---

## 中文版本

**[English](#english-version)** | 中文

AI 代理的自我修复加密钱包，支持意图执行和社交恢复。

### 版本

**当前版本**: v0.1.0
**发布日期**: 2026-03-12
**状态**: 早期开发（Alpha）

### 什么是自主钱包？

一个智能加密钱包：
- **理解自然语言** - "发送 0.1 ETH 给 alice.eth"
- **自动从错误中恢复** - 交易失败？自动调整 gas 重试
- **支持社交恢复** - 丢失访问权限？可信守护者可以帮助
- **为 AI 代理而生** - 专为自主操作构建

适用于：
- 🤖 AI 代理资金管理
- 💼 自动化 DeFi 策略
- 🔐 安全多签操作
- 🌐 跨链资产管理

### 功能特性

- **基于意图的执行**: 自然语言 → 区块链操作
- **自我修复**: 自动重试并优化 gas
- **社交恢复**: 基于守护者的钱包恢复（2/3、3/5 等）
- **安全优先**: 硬件钱包支持、加密存储、速率限制
- **多链支持**: Ethereum、Polygon、Arbitrum、Optimism、Base 等

### 快速开始

#### 安装

```bash
# 全局安装
npm install -g openclaw-autonomous-wallet

# 验证
autonomous-wallet --version
```

#### 初始化钱包

```bash
# 创建新钱包
autonomous-wallet init

# 导入现有钱包
autonomous-wallet import --mnemonic "你的 12 个助记词..."
```

#### 执行意图

```bash
# 简单转账
autonomous-wallet execute "发送 0.1 ETH 给 vitalik.eth"

# 代币兑换
autonomous-wallet execute "在 Uniswap 将 100 USDC 兑换为 ETH"

# 查看余额
autonomous-wallet balance
```

#### 设置社交恢复

```bash
autonomous-wallet recovery setup \
  --guardian1 0x守护者1... \
  --guardian2 0x守护者2... \
  --guardian3 0x守护者3... \
  --threshold 2 \
  --timelock 7d
```

### 配置

#### 环境变量

```bash
# 钱包
export PRIVATE_KEY=0x...          # 你的私钥
export MNEMONIC="词1 词2..."      # 或助记词

# 网络
export NETWORK=mainnet            # mainnet, sepolia, polygon 等
export RPC_URL=https://...        # 自定义 RPC（可选）

# 安全
export MAX_GAS_PRICE=100          # 最大 gas（gwei）
export DAILY_LIMIT=10             # 每日限额（ETH）
export SIMULATION_REQUIRED=true   # 执行前需要模拟
```

### 命令

| 命令 | 描述 |
|------|------|
| `init` | 初始化新钱包 |
| `import` | 导入现有钱包 |
| `balance` | 查看钱包余额 |
| `history` | 查看交易历史 |
| `execute "意图"` | 执行自然语言命令 |
| `recovery setup` | 设置社交恢复守护者 |
| `recovery initiate` | 启动恢复流程（作为守护者） |
| `recovery approve` | 批准恢复请求（作为守护者） |
| `config show` | 查看当前配置 |

### 使用案例

#### 1. AI 代理资金管理

```typescript
import { AutonomousWallet } from 'openclaw-autonomous-wallet';

const wallet = new AutonomousWallet({ network: 'mainnet' });

// AI 自动支付团队工资
await wallet.execute({
  intent: "支付团队月薪",
  context: { team: addresses }
});
```

#### 2. DeFi 自动化

```bash
# 复杂 DeFi 操作
autonomous-wallet execute "将 10 ETH 兑换为 USDC 并提供 Uniswap 流动性"
```

#### 3. 投资组合管理

```bash
# 重新平衡投资组合
autonomous-wallet execute "重新平衡为 60% ETH, 30% USDC, 10% WBTC"
```

### 性能

| 操作 | 时间 | Gas 成本 |
|------|------|---------|
| 简单转账 | ~2秒 | ~21,000 |
| 代币兑换 | ~5秒 | ~150,000 |
| 社交恢复设置 | ~10秒 | ~200,000 |

### 安全

✅ **您的密钥，您的控制** - 私钥仅本地存储
✅ **交易模拟** - 执行前测试
✅ **速率限制** - 防止快速支出
✅ **每日限额** - 设置每日最大支出
✅ **守护者恢复** - 密钥丢失的社交备份

### 故障排除

#### 交易失败
- ✅ 默认启用自动重试
- 检查 gas 价格：`autonomous-wallet gas-price`
- 提高最大 gas：`autonomous-wallet config set-max-gas 150`

#### 网络问题
- 验证 RPC：`autonomous-wallet network check`
- 尝试备用 RPC：`export RPC_URL=https://...`

#### 守护者恢复
- 验证守护者地址
- 检查时间锁定期（默认 7 天）
- 确保达到阈值（例如 3 个中的 2 个批准）

### 链接

- **GitHub**: https://github.com/ZhenRobotics/openclaw-autonomous-wallet
- **npm**: https://www.npmjs.com/package/openclaw-autonomous-wallet
- **文档**: https://docs.openclaw.ai/wallet
- **问题反馈**: https://github.com/ZhenRobotics/openclaw-autonomous-wallet/issues
- **Discord**: https://discord.gg/openclaw

### 支持

获取帮助：
1. 查看 [GitHub Issues](https://github.com/ZhenRobotics/openclaw-autonomous-wallet/issues)
2. 阅读[完整文档](https://docs.openclaw.ai/wallet)
3. 加入 [Discord 社区](https://discord.gg/openclaw)

### 许可证

MIT License - 详见 LICENSE 文件

### 免责声明

⚠️ **早期开发** - 这是 alpha 软件（v0.1.0）
- 未经生产审计
- 先在测试网使用再用于主网
- 始终备份您的密钥
- 测试恢复流程

---

**Version | 版本**: 0.1.0
**Last Updated | 最后更新**: 2026-03-12
**Maintainer | 维护者**: ZhenStaff
