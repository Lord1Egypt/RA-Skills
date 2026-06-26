# AirdropAlert 🪂

**空投提醒技能 - 追踪潜在空投资格，提醒快照和时间**

## 技能信息

- **名称**: AirdropAlert
- **版本**: 0.1.0
- **作者**: @gztanht
- **许可**: MIT
- **GitHub**: https://github.com/gztanht/airdrop-shark
- **ClawHub**: https://clawhub.com/skills/airdrop-shark

## 产品亮点

- 🪂 **空投项目数据库** - 50+ 潜在空投项目
- ✅ **资格要求检查** - 一键检查是否符合条件
- ⏰ **快照时间提醒** - 重要时间点通知
- 📋 **交互指南** - 逐步操作指南
- 💰 **预期价值评估** - 空投代币估值

## 快速开始

```bash
# 查看所有空投项目
node scripts/airdrop.mjs

# 查看高优先级空投
node scripts/airdrop.mjs --priority high

# 检查特定项目资格
node scripts/eligibility.mjs layerzero

# 设置快照提醒
node scripts/reminder.mjs add --project zksync --date "2026-03-20"
```

## 使用示例

### 查看所有空投项目

```bash
$ node scripts/airdrop.mjs

🪂 AirdropAlert - 潜在空投项目

优先级  项目              链           快照时间    预期价值    难度
─────────────────────────────────────────────────────────────────────
🔴 高    LayerZero       多链         2026-Q2     $2000-5000  中
🔴 高    zkSync Era      Ethereum     2026-Q1     $1000-3000  低
🟡 中    Starknet        Starknet     已完成      $500-2000   低
🟢 低    Scroll          Ethereum     2026-Q3     $300-1000   中

💡 提示：node scripts/airdrop.mjs --priority high
```

### 检查资格

```bash
$ node scripts/eligibility.mjs layerzero

✅ LayerZero 资格检查

地址：0x33f9...5ad9
状态：符合条件

要求:
- ✅ 跨链交易 > 5 次
- ✅ 使用 > 3 条不同链
- ✅ 总交易量 > $1000
- ✅ 最近 30 天活跃

预期空投：$2000-5000 (0.2-0.5% 代币供应)
```

### 设置提醒

```bash
$ node scripts/reminder.mjs add --project zksync --date "2026-03-20"

✅ 提醒已设置

项目：zkSync Era
快照时间：2026-03-20 00:00
提醒时间：2026-03-19 20:00 (提前 4 小时)

💡 查看提醒：node scripts/reminder.mjs --list
```

## 命令参考

| 命令 | 功能 |
|------|------|
| `airdrop.mjs` | 查看所有空投项目 |
| `airdrop.mjs --priority high` | 只看高优先级 |
| `eligibility.mjs <project>` | 检查特定项目资格 |
| `reminder.mjs add --project X --date YYYY-MM-DD` | 设置快照提醒 |
| `reminder.mjs --list` | 查看所有提醒 |
| `reminder.mjs remove <id>` | 删除提醒 |

## 支持的空投项目

| 项目 | 链 | 预期价值 | 优先级 |
|------|-----|---------|--------|
| LayerZero | 多链 | $2000-5000 | 🔴 高 |
| zkSync Era | Ethereum | $1000-3000 | 🔴 高 |
| Starknet | Starknet | $500-2000 | 🟡 中 |
| Scroll | Ethereum | $300-1000 | 🟢 低 |
| Linea | Ethereum | $300-800 | 🟢 低 |
| Base | Base | $200-600 | 🟢 低 |

## 定价

**免费使用**: 5 次查询/天

**赞助解锁**: 0.5 USDT/USDC → 无限查询

**赞助地址**:
- USDT (ERC20): `0x33f943e71c7b7c4e88802a68e62cca91dab65ad9`
- USDC (ERC20): `0xcb5173e3f5c2e32265fbbcaec8d26d49bf290e44`

## 配置

编辑 `config/projects.json` 添加/修改空投项目：

```json
{
  "layerzero": {
    "name": "LayerZero",
    "chain": "多链",
    "priority": "high",
    "snapshot": "2026-Q2",
    "expectedValue": "$2000-5000",
    "difficulty": "中",
    "requirements": [
      "跨链交易 > 5 次",
      "使用 > 3 条不同链",
      "总交易量 > $1000"
    ],
    "guide": "https://layerzero.network"
  }
}
```

## 安全提示

⚠️ **重要提醒**:
- 不要相信私信你的"空投申领"链接
- 官方永远不会要求你提供私钥
- 永远先验证合约地址
- 小额测试后再大额交互

## 支持渠道

- **GitHub Issues**: https://github.com/gztanht/airdrop-shark/issues
- **Telegram**: @gztanht
- **ClawHub**: https://clawhub.com/skills/airdrop-shark

---

**🪂 AirdropAlert v0.1.0 - Never Miss an Airdrop**
