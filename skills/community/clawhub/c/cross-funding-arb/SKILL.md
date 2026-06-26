---
name: cross-funding-arb
description: "跨交易所资金费率套利策略。在费率低的交易所做多永续、费率高的交易所做空永续，Delta-neutral 赚取 funding spread。支持 Hyperliquid + Binance，自动扫描机会、稳定性验证、原子开仓、健康检查、自动切仓。适用于资金费率套利、Delta 中性、跨所套利场景。"
license: Apache-2.0
metadata:
  author: SynthThoughts
  version: "2.8.0"
  pattern: "pipeline"
  steps: "5"
  openclaw:
    requires:
      env:
        - HL_PRIVATE_KEY
        - BINANCE_API_KEY
        - BINANCE_SECRET_KEY
      optional_env:
        - HL_VAULT_ADDRESS
        - HL_TESTNET
        - BINANCE_TESTNET
        - DISCORD_CHANNEL_ID
        - DISCORD_BOT_TOKEN
        - TELEGRAM_BOT_TOKEN
        - TELEGRAM_CHAT_ID
        - STATE_DIR
      bins:
        - python3
    primaryEnv: HL_PRIVATE_KEY
    entrypoint: references/cross_funding.py
    os:
      - darwin
      - linux
---

# Cross-Exchange Funding Rate Arbitrage v2

Cron 驱动的跨交易所资金费率套利机器人。核心思路：**在费率低的交易所做多永续合约，在费率高的交易所做空永续合约**，两腿等量 delta-neutral，赚取 funding spread。

数据源：VarFunding API（预计算的跨所套利机会）。执行层：Hyperliquid SDK（EIP-712 私钥签名）+ Binance Futures API（HMAC 签名）。

每个 tick：扫描机会 → 稳定性验证 → 深度验证 → 开仓/维护 → 报告。

## Architecture

```
VarFunding API ──→ Scanner ──→ 稳定性验证 ──→ 深度验证
                                                  │
                        ┌─────────────────────────┘
                        ↓
              CrossFundingEngine
                   /         \
            HLClient       BinanceClient
            (EIP-712)      (HMAC-SHA256)
                |               |
          Hyperliquid       Binance Futures
          (永续合约)        (USDT-M 永续)
```

## Pipeline: Execution Steps

### Step 0: Prerequisites

- Python 3.10+
- `hyperliquid-python-sdk >= 0.21.0`
- `eth-account >= 0.13.7`
- `python-dotenv >= 1.0.0`
- `requests >= 2.31.0`
- Hyperliquid 账户 + 私钥（主账户或 Agent Wallet）
- Binance Futures 账户 + API Key/Secret（需 USDT-M 交易权限）

### Step 1: Price & Rate Scanning

**Goal**: 从 VarFunding API 获取跨所套利机会

**Actions**:
1. 调用 `VarFundingScanner.fetch_opportunities()` 获取 HL × Binance 的套利机会
2. 过滤：估计 APR ≥ `min_apr_pct`，置信度 ≥ `min_confidence`
3. 按 APR 降序排列，取 Top 5

**Gate**:
- [ ] 至少有一个机会满足 APR 和置信度门槛
- [ ] 无机会 → 输出 `action: idle`，等待下一 tick

### Step 2: Stability Verification

**Goal**: 防止瞬时费率波动导致错误开仓

**Actions**:
1. 将 Top 5 机会记录为费率快照（state 中保留最近 20 条）
2. 按币种分组，检查同一币种的快照数 ≥ `stability_snapshots`（默认 3）
3. 计算 spread 的标准差占比 `std/avg`，须 < `stability_max_std_ratio`（默认 0.3）

**Gate**:
- [ ] 存在至少一个币种通过稳定性检查
- [ ] 未通过 → 输出 `action: accumulating`，继续积累快照

### Step 3: Deep Verification

**Goal**: 独立验证两所实际费率 + 价格差 + 往返成本

**Actions**:
1. 分别从 HL 和 Binance 获取实时费率和中间价
2. 计算实际 spread = short_rate − long_rate
3. 计算价格差异 `price_basis_pct = |hl_price − bn_price| / avg_price`
4. 计算净 APR = gross_annual − round_trip_cost_pct

**Gate** (ALL must pass):
- [ ] 实际 spread > 0
- [ ] 价格差异 < `max_price_basis_pct`（默认 0.5%）
- [ ] 净 APR ≥ `min_apr_pct`（默认 10%）
- [ ] 任一失败 → 输出 `action: rejected` + 原因

### Step 4: Atomic Execution

**Goal**: 原子开仓，先 HL 后 Binance，失败自动回滚

**Actions**:
1. 计算 size：`min(hl_budget, bn_budget) × 0.5 × 0.95 × leverage / price`
2. 两所分别 round_size，取较小值
3. 两所设杠杆
4. **先下 HL 单**（分级保证金限制更严，失败代价低）
   - 使用 LIMIT IOC 模拟市价，滑点 0.1%
   - Insufficient margin → 自动减半 size 重试（最多 3 次）
5. **再下 Binance 单**
   - Binance 失败 → 自动回滚 HL 腿（close_position）
6. 保存完整开仓状态 + 两所初始余额

**Gate**:
- [ ] 两腿均成功开仓
- [ ] HL 失败 → 不开 Binance，直接终止
- [ ] Binance 失败 → 回滚 HL 腿，发出 rollback 通知

### Step 5: Health Monitoring & Auto-Switch

**Goal**: 持仓期间持续监控，spread 不利或缺腿时自动处理

**每 tick 检查**:
1. **Delta 检查**：两腿 size 偏差 < 20%
2. **Spread 检查**：当前 spread > `close_spread_threshold`（默认 0.005%）
3. **双腿检查**：两所都有持仓

**自动处理**:
- Spread 不利（< threshold）→ 平仓（先平 short，后平 long）
- 缺腿 → 平仓 + risk_alert 通知
- 健康 → 缓存快照，每小时推送 hourly_pulse

**切仓逻辑**:
- 持仓中发现更好机会：当前 APR vs 新机会 APR 差距 > `switch_threshold_apr` → 平仓 → 下个 tick 自动开新仓

## Tunable Parameters

### Cross Funding Configuration

| Parameter | Default | Description |
|---|---|---|
| `hl_budget_usd` | `0` | Hyperliquid 单边预算 (USDC)，0 = 自动读取账户余额 |
| `bn_budget_usd` | `0` | Binance 单边预算 (USDT)，0 = 自动读取账户余额 |
| `min_apr_pct` | `10.0` | 最低年化收益率门槛 (%) |
| `min_confidence` | `"medium"` | VarFunding 最低置信度 (low/medium/high) |
| `leverage` | `1` | 杠杆倍数（默认无杠杆） |
| `stability_snapshots` | `3` | 稳定性验证所需快照数 |
| `stability_max_std_ratio` | `0.3` | Spread 标准差/均值上限 |
| `close_spread_threshold` | `0.0001` | 平仓 spread 下限（8h 费率差，≈10.95% APR） |
| `switch_threshold_apr` | `5.0` | 切仓 APR 差距门槛 (%) |
| `max_price_basis_pct` | `0.5` | 两所价格差异上限 (%) |
| `round_trip_cost_pct` | `0.12` | 往返成本 (%, 含手续费+滑点) |

### Shared Configuration

| Parameter | Default | Description |
|---|---|---|
| `max_consecutive_errors` | `5` | 连续错误触发熔断 |
| `cooldown_after_errors` | `3600` | 熔断冷却时间 (秒) |
| `min_order_usd` | `10` | 最小下单金额 (USD) |

### Environment Variables

| Variable | Required | Description |
|---|---|---|
| `HL_PRIVATE_KEY` | ✅ | Hyperliquid 私钥（主账户或 Agent Wallet） |
| `HL_VAULT_ADDRESS` | ❌ | Agent Wallet 的 master 地址 |
| `HL_TESTNET` | ❌ | `true` 使用测试网 |
| `BINANCE_API_KEY` | ✅ | Binance Futures API Key |
| `BINANCE_SECRET_KEY` | ✅ | Binance Futures API Secret |
| `BINANCE_TESTNET` | ❌ | `true` 使用测试网 |
| `DISCORD_BOT_TOKEN` | ❌ | Discord 通知 bot token |
| `DISCORD_CHANNEL_ID` | ❌ | Discord 目标频道 ID |
| `TELEGRAM_BOT_TOKEN` | ❌ | Telegram 通知 bot token |
| `TELEGRAM_CHAT_ID` | ❌ | Telegram 目标 chat ID |

## Operational Interface

| Command | Description | Typical Use |
|---|---|---|
| `tick` | 主循环：扫描 → 验证 → 开仓/维护 | Cron 每 5 分钟 |
| `report` | 生成日报（含 PnL、余额、费率） | Cron 每天 00:00 UTC |
| `status` | 当前状态（优先读缓存） | 手动查询 |

```bash
# 单次 tick
cd ~/scripts/cross-funding && set -a && . ./.env && set +a && python3 cross_funding.py tick

# 日报
python3 cross_funding.py report

# 状态查询
python3 cross_funding.py status
```

## Notification Tiers

| Tier | When | Color | Key Fields |
|---|---|---|---|
| `trade_alert` | 开仓/平仓 | 🟢 Green / 🟠 Orange | Long/Short 交易所, Size, Spread, APR |
| `risk_alert` | Spread 不利/缺腿/熔断 | 🔴 Red | 原因, 当前 APR, Delta 偏差 |
| `hourly_pulse` | 每小时（持仓中） | ⚪ Grey | 两所余额, 费率, Spread, PnL |
| `daily_report` | 每日报告 | 🔵 Blue | 持仓详情, 总资产, ROI, 年化 |

通知同时推送 Discord embed + Telegram markdown。凭证解析优先级：环境变量 > OpenClaw `openclaw.json` > ZeroClaw `config.toml`。未配置时静默跳过。

## State Schema

```json
{
  "current_coin": "FET",
  "direction": {
    "long_exchange": "hyperliquid",
    "short_exchange": "binance"
  },
  "entry_time": "2026-03-25T10:00:00+00:00",
  "entry_spread": 0.0006,
  "entry_hl_rate": 0.0000125,
  "entry_bn_rate": 0.0006194,
  "size": 150.0,
  "entry_price": 0.85,
  "budget_hl": 300,
  "budget_bn": 450,
  "entry_hl_balance": 295.5,
  "entry_bn_balance": 445.2,
  "entry_total_balance": 740.7,
  "total_funding_earned": 0.0,
  "rate_snapshots": [],
  "cached_snapshot": {},
  "cached_snapshot_ts": "...",
  "last_tick": "...",
  "last_pulse_ts": "..."
}
```

## Core Algorithm

```
1. 获取进程锁（flock，防止并发 tick）
2. 检查熔断器状态（连续 5 次错误 → 冷却 1h）
3. 加载状态
4. IF 无持仓:
   a. VarFunding API 扫描套利机会
   b. 记录费率快照
   c. 检查稳定性（需 3+ 快照，std_ratio < 0.3）
   d. 深度验证（实时费率 + 价格差 + 净 APR）
   e. 原子开仓（先 HL 后 BN，HL 失败自动减半重试）
5. IF 有持仓:
   a. 健康检查（delta + spread + 双腿）
   b. 不健康 → 自动平仓
   c. 健康 → 缓存快照，每小时推送 pulse
6. 记录成功/错误
7. 释放锁
```

## Risk Control

| Layer | Check | Action |
|---|---|---|
| 稳定性验证 | 费率快照 std_ratio < 0.3 | 阻止开仓，继续积累 |
| 深度验证 | 实际 spread > 0, 价格差 < 0.5%, APR ≥ 门槛 | 拒绝不合格机会 |
| 保守预算 | 只用 min(两所预算) × 50% | 预留安全余量 |
| 滑点控制 | 市价单滑点 0.1%（非常规 5%） | 降低套利成本 |
| HL Margin 重试 | Insufficient margin → size 减半，最多 3 次 | 适应分级保证金 |
| 原子回滚 | BN 失败 → 自动平 HL | 防止单腿裸露 |
| Delta 监控 | 两腿偏差 > 20% → 告警 | 发现脱钩 |
| Spread 监控 | spread < threshold → 自动平仓 | 防止费率反转亏损 |
| 熔断器 | 连续 5 错 → 冷却 1h | 防止连环失败 |

## Failure & Rollback

```
IF tick fails:
  1. 记录错误到熔断器
  2. 连续 5 次 → 进入冷却（1h）
  3. 开仓失败:
     - HL 失败 → 不开 Binance，直接终止
     - Binance 失败 → 回滚 HL 腿（close_position）
     - 发出 risk_alert 通知
  4. 健康检查发现问题:
     - 缺腿 → 平仓
     - Spread 不利 → 平仓
  5. 冷却结束后自动恢复
```

## Anti-Patterns

| Pattern | Problem |
|---|---|
| 不做稳定性验证直接开仓 | 瞬时费率波动导致开仓即亏 |
| 滑点设太大（>1%） | 套利利润被滑点吞噬 |
| 两所预算差太大 | 大腿 size 受限于小腿，资金利用率低 |
| 忽略价格差异 | 两所标记价差异大时 delta 不中性 |
| 不检查双腿一致性 | 单腿被清算另一腿裸露 |
| 杠杆过高 | 小币波动大，保证金不足被强平 |
| 只看 VarFunding 不独立验证 | API 数据可能滞后于实际费率 |
| 熔断后手动重启不排查 | 掩盖系统性问题 |

## Data Source: VarFunding API

```
GET https://varfunding.xyz/api/funding?exchanges=hyperliquid,binance

Response: {
  "markets": [{
    "baseAsset": "FET",
    "variational": { "exchange": "hyperliquid", "rate": 0.0000125 },
    "comparisons": [{ "exchange": "binance", "rate": 0.0006194 }],
    "arbitrageOpportunity": {
      "longExchange": "hyperliquid",
      "shortExchange": "binance",
      "spread": 0.0006,
      "estimatedApr": 66.5,
      "confidence": "medium"
    }
  }]
}
```

## Deployment

安装后脚本位于标准 skill 目录，无需手动拷贝。

```
# OpenClaw 安装路径
~/.openclaw/skills/cross-funding-arb/references/cross_funding.py

# ZeroClaw 安装路径
~/.zeroclaw/skills/cross-funding-arb/references/cross_funding.py
```

**安装后配置**：将 `.env` 放到 `references/` 目录（与 `cross_funding.py` 同级）：

```bash
# OpenClaw
cp .env.example ~/.openclaw/skills/cross-funding-arb/references/.env
# 编辑填入 HL_PRIVATE_KEY, BINANCE_API_KEY, BINANCE_SECRET_KEY

# ZeroClaw
cp .env.example ~/.zeroclaw/skills/cross-funding-arb/references/.env
```

### OpenClaw Cron

```bash
SKILL_DIR=~/.openclaw/skills/cross-funding-arb/references

# tick: 每 5 分钟（主会话执行 shell 命令）
openclaw cron add \
  --name "cross-funding-tick" \
  --cron "*/5 * * * *" \
  --session main \
  --system-event "cd $SKILL_DIR && set -a && . ./.env && set +a && python3 cross_funding.py tick"

# 日报: 每天 00:00 UTC（隔离会话，结果投递到 Discord）
openclaw cron add \
  --name "cross-funding-report" \
  --cron "0 0 * * *" \
  --tz "UTC" \
  --session isolated \
  --message "执行跨交易所资金费率套利日报: cd $SKILL_DIR && set -a && . ./.env && set +a && python3 cross_funding.py report。将完整输出结果总结后回复我。" \
  --announce \
  --channel discord
```

### ZeroClaw Cron

```bash
SKILL_DIR=~/.zeroclaw/skills/cross-funding-arb/references

# tick: 每 5 分钟
zeroclaw cron add --expr "*/5 * * * *" --shell \
  "cd $SKILL_DIR && set -a && . ./.env && set +a && python3 cross_funding.py tick"

# 日报: 每天 00:00 UTC
zeroclaw cron add --expr "0 0 * * *" --agent \
  "执行跨交易所资金费率套利日报: cd $SKILL_DIR && set -a && . ./.env && set +a && python3 cross_funding.py report。将完整输出结果总结后回复我。"
```

### Manual

```bash
cd ~/.openclaw/skills/cross-funding-arb/references
set -a && . ./.env && set +a

python3 cross_funding.py tick      # 单次 tick
python3 cross_funding.py status    # 状态查询
python3 cross_funding.py report    # 日报
```

## Install

```bash
npx clawhub install cross-funding-arb --force
```

## Security Notice

> **安装时可能出现安全扫描告警（需 `--force`），这是误报。**

本技能是交易策略，代码中涉及的"可疑模式"均为正常业务需求：

| 被标记的模式 | 实际用途 | 安全性 |
|---|---|---|
| `private_key` / `secret_key` / `api_key` | 交易所 API 凭证变量名 | 全部通过 `.env` 环境变量注入，**代码中无硬编码密钥** |
| `hmac` + `hashlib.sha256` | Binance Futures API 请求签名 | 标准 HMAC-SHA256 签名，[Binance 官方要求](https://developers.binance.com/docs/binance-spot-api-docs/rest-api/public-api-definitions#signed-trade-and-user_data-endpoint-security) |
| 外部 HTTP 请求 | 调用 Binance / Hyperliquid / VarFunding / Discord / Telegram API | 仅与已知交易所和通知服务通信 |
| `bot_token` / `chat_id` | Discord / Telegram 通知推送凭证 | 可选功能，未配置时静默跳过 |

**代码中不包含**：`eval` / `exec` / `subprocess` / `os.system` / 文件系统扫描 / 动态代码加载 / 数据外泄逻辑。

如需审查，完整源码位于 `references/cross_funding.py`（单文件，约 2400 行）。
