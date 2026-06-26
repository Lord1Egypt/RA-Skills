# Cross-Exchange Funding Rate Arbitrage

跨交易所资金费率套利策略。在费率低的交易所做多永续、费率高的做空，Delta-neutral 赚取 funding spread。

## Features

- **自动扫描**：VarFunding API 实时发现 HL × Binance 套利机会
- **稳定性验证**：多次快照确认费率稳定后才开仓，防止瞬时波动
- **原子开仓**：先 HL 后 Binance，失败自动回滚，无单腿裸露风险
- **健康监控**：Delta 偏差 + Spread 监控 + 双腿一致性检查
- **自动切仓**：Spread 不利时平仓，下一 tick 自动寻找新机会
- **多渠道通知**：Discord embed + Telegram markdown，按 tier 分级推送

## Quick Start

### 1. Install

```bash
npx clawhub install cross-funding-arb --force
pip install -r references/requirements.txt
```

### 2. Configure

```bash
# OpenClaw
cp .env.example ~/.openclaw/skills/cross-funding-arb/references/.env
# 编辑 .env，填入 HL_PRIVATE_KEY, BINANCE_API_KEY, BINANCE_SECRET_KEY

# 可选：调整 references/config.json 中的风控参数
```

### 3. Test

```bash
cd ~/.openclaw/skills/cross-funding-arb/references
set -a && . ./.env && set +a

python3 cross_funding.py status    # 查看当前状态
python3 cross_funding.py tick      # 单次 tick
```

### 4. Deploy

```bash
SKILL_DIR=~/.openclaw/skills/cross-funding-arb/references

# OpenClaw cron
openclaw cron add \
  --name "cross-funding-tick" \
  --cron "*/5 * * * *" \
  --session main \
  --system-event "cd $SKILL_DIR && set -a && . ./.env && set +a && python3 cross_funding.py tick"

# 或系统 crontab
*/5 * * * * cd $SKILL_DIR && set -a && . ./.env && set +a && python3 cross_funding.py tick >> /tmp/cross_funding.log 2>&1
```

## Commands

| Command | Description |
|---|---|
| `tick` | 主循环：扫描 → 验证 → 开仓/维护 |
| `report` | 日报：持仓、PnL、余额、费率 |
| `status` | 当前状态（优先读缓存） |

## Risk Controls

| Control | Description |
|---|---|
| 稳定性验证 | 3+ 快照 + std_ratio < 0.3 |
| 深度验证 | 实时费率 + 价格差 < 0.5% + 净 APR ≥ 10% |
| 保守预算 | min(两所) × 50%，budget=0 自动读取账户余额 |
| 滑点 0.1% | 远低于常规 5%，保护套利利润 |
| HL Margin 重试 | size 减半最多 3 次 |
| 原子回滚 | BN 失败 → 自动平 HL |
| 熔断器 | 连续 5 错 → 冷却 1h |

## Prerequisites

- Python 3.10+
- Hyperliquid 账户 + 私钥
- Binance Futures 账户 + API Key（USDT-M 交易权限）
- 两所均需存入保证金（策略自动检测账户余额）

## License

Apache-2.0
