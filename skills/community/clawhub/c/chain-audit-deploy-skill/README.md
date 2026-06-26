# Chain Audit & Deploy SKILL

区块链智能合约安全审计与部署 SKILL，支持 Solidity、Sui Move 和 Solana 合约的自动化审计、漏洞扫描及一键部署。

> 核心原则：**先审计，后部署**。默认部署到测试网，主网部署需二次确认。

---

## 项目结构

```
chain-audit-deploy/
├── SKILL.md                  # 技能定义（工作流 & 规则）
├── scripts/
│   ├── audit_solidity.py     # Solidity 自动审计
│   ├── audit_sui_move.py     # Sui Move 自动审计
│   ├── audit_solana.py       # Solana 自动审计
│   └── deploy_helper.py      # 统一部署脚本
├── references/
│   ├── solidity_audit_rules.md
│   ├── sui_move_audit_rules.md
│   ├── solana_audit_rules.md
│   └── deployment_guide.md
├── assets/
│   └── report_template.md    # 审计报告模板
└── examples/
    ├── solidity/              # SimpleStorage 示例
    ├── sui_move/              # SimpleCounter 示例
    └── solana/                # SimpleCounter (Anchor) 示例
```

---

## 前置依赖

根据目标链安装对应工具：

| 链 | 必需工具 | 安装方式 |
|---|---|---|
| Solidity | `forge` (Foundry) | `curl -L https://foundry.paradigm.xyz \| bash && foundryup` |
| Sui Move | `sui` CLI | `cargo install --locked --git https://github.com/MystenLabs/sui.git sui` |
| Solana | `anchor` + `solana` CLI | `cargo install --git https://github.com/coral-xyz/anchor avm && avm install latest` |

---

## 快速使用

### 1. 审计合约

```bash
# Solidity
python3 scripts/audit_solidity.py --path <项目路径>

# Sui Move
python3 scripts/audit_sui_move.py --path <项目路径>

# Solana
python3 scripts/audit_solana.py --path <项目路径>

# 仅检查工具是否安装
python3 scripts/audit_solidity.py --check-tools
```

### 2. 部署合约

```bash
python3 scripts/deploy_helper.py \
  --chain <solidity|sui_move|solana> \
  --path <项目路径> \
  --network <网络名称> \
  [--gas-budget <金额>] \
  [--args <构造函数参数>] \
  [--dry-run]          # 推荐先干跑
```

### 3. 作为 CodeBuddy 技能使用

安装技能后，直接用自然语言与 AI 对话：

- **"审计我的合约"** → 自动识别链类型 → 运行审计脚本 + AI 深度审查 → 输出报告
- **"部署到测试网"** → 完整流程：审计 → 部署
- **"部署到主网"** → 完整流程 + 主网安全确认
- **"跳过审计直接部署"** → 需确认风险后执行
- **"有哪些例子"** → 展示 3 个内置示例项目

---

## 审计门控规则

| 结果 | 条件 | 能否部署 |
|---|---|---|
| **PASS** | 无 Critical / High 级别问题 | ✅ 可以部署 |
| **CONDITIONAL PASS** | 仅有 Medium / Low / Info | ⚠️ 警告后可部署 |
| **FAIL** | 存在 Critical 或 High 问题 | ❌ 阻断，需修复或手动确认风险 |

---

## 内置示例

| 示例 | 语言 | 构建工具 | 位置 |
|---|---|---|---|
| SimpleStorage | Solidity 0.8.20 | Foundry | `examples/solidity/` |
| SimpleCounter | Sui Move 2024.beta | sui CLI | `examples/sui_move/` |
| SimpleCounter | Rust + Anchor 0.30.1 | Anchor | `examples/solana/` |

---

## 支持的网络

- **EVM**: Ethereum, Sepolia, Holesky, BSC, Base, Monad, 0G 及其测试网
- **Sui**: Mainnet, Testnet, Devnet, Localnet
- **Solana**: Mainnet-beta, Testnet, Devnet, Localnet

详见 `references/deployment_guide.md` 获取 RPC 地址、区块浏览器和测试网水龙头链接。

---

## 安全规则

1. **不存储/记录私钥**，仅使用环境变量或 keystore
2. **默认部署到测试网**，未指定网络时自动选择测试网
3. **主网部署需双重确认**
4. **审计在部署前强制执行**（除非用户明确跳过）
