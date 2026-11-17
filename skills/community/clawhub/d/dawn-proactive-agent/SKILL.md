---
name: dawn-proactive-agent
description: Dawn Agent v1.5 self-evolution proactive architecture. P0-P4 framework for autonomous ETF trading agent with self-reflection, state machine, audit trail, multi-dimension scoring, and safety guardrails.
metadata:
  openclaw:
    requires:
      bins: [python]
    runtime: python
    permissions:
      - network: [api.zhangle.com, push2.eastmoney.com, quote.eastmoney.com, www.sina.com.cn]
      - filesystem: [read/write workspace]
      - exec: [python]
---

# Dawn Proactive Agent v1.5

An autonomous, self-evolving ETF trading agent architecture designed for the A-share market.

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│              Dawn Proactive Agent v1.5              │
├─────────────────────────────────────────────────────┤
│  P0: dawn_reflect.py    Hermes-inspired reflection  │
│  P1: dawn_state.py      LangGraph state machine     │
│  P2: dawn_audit.py      RagaAI audit trail          │
│  P3: dawn_analysis.py   ai-berkshire 4D scoring     │
│  P4: dawn_guardrails.py OpenAI Agents safety        │
├─────────────────────────────────────────────────────┤
│       Active in: 华泰柏瑞杯ETF AI交易巅峰赛          │
│       Period: 2026/6/11 - 2026/7/20                 │
│       Portfolio: 8 ETFs, ~¥1M AUM                    │
└─────────────────────────────────────────────────────┘
```

## Components

### P0 - Self-Reflection Engine (`dawn_reflect.py`)
Hermes-inspired post-trade reflection. After every portfolio adjustment, automatically extracts lessons learned and loads them into the next decision cycle.
- Trigger: post-trade callback
- Output: structured learnings with recall scoring
- Integrates with `.learnings/` structured log system

### P1 - State Machine (`dawn_state.py`)
LangGraph-inspired workflow orchestration with checkpoint/resume.
- States: IDLE → ANALYZE → DECIDE → EXECUTE → REFLECT → IDLE
- Checkpoint recovery on timeout/crash
- Timeout downgrade: auto-fallback to safest state

### P2 - Audit Trail (`dawn_audit.py`)
RagaAI-inspired immutable decision logging.
- Every decision recorded: timestamp, reasoning, data sources, signals, outcome
- Queryable by date/strategy/symbol
- Exports as structured JSON for backtesting

### P3 - Multi-Dimension Scoring (`dawn_analysis.py`)
ai-berkshire-inspired composite scoring for ETF selection.
- Technical (30%): momentum, trend, volume
- News Sentiment (25%): real-time financial news analysis
- Capital Flow (25%): sector money flow tracking
- Volume-Price (20%): volume-price divergence detection

### P4 - Safety Guardrails (`dawn_guardrails.py`)
OpenAI Agents SDK-inspired transaction safety checks.
- Blacklist: 科创板(688) and ST stocks blocked
- Position limits: max 40% single ETF
- Daily loss limit: max -5% stop-loss
- Available cash check before execution

## Usage

### Daily Strategy Run (09:28)
```bash
python scripts/dawn_proactive.py --action morning
```

### Post-Market Review (15:05)
```bash
python scripts/dawn_proactive.py --action afternoon
```

### Midday Check (11:30)
```bash
python scripts/dawn_proactive.py --action midday
```

### Manual Trade
```bash
python scripts/dawn_etf_rotator.py --execute
```

## Files

| File | Purpose |
|------|---------|
| `scripts/dawn_proactive.py` | Main orchestrator |
| `scripts/dawn_etf_rotator.py` | ETF rotation strategy |
| `scripts/dawn_reflect.py` | P0: Self-reflection |
| `scripts/dawn_state.py` | P1: State machine |
| `scripts/dawn_audit.py` | P2: Audit trail |
| `scripts/dawn_analysis.py` | P3: 4D scoring |
| `scripts/dawn_guardrails.py` | P4: Safety guardrails |
| `scripts/dawn_memory_sync.py` | L1↔L3 memory sync |
| `scripts/dawn_collector.py` | Market data collection |
| `scripts/dawn_selector.py` | ETF selection logic |
| `scripts/dawn_monitor.py` | Real-time monitoring |

## Results (2026-07-06)

- **Cron jobs**: 10 automated tasks running daily
- **Portfolio**: 8 ETFs, 38.2%仓位, ¥1,003,751
- **Key wins**: 科创板V反守住(+0.69% on 07-03), 全天候自动运行
- **Self-healing**: 收盘复盘cron timeout自动修复 (agentTurn→command模式)
- **Delivery**: 飞书推送自动修复 (delivery.to user:前缀)

See `samples/proactive_demo.md` for a full session trace.

## Changelog

### v1.5 (2026-07-06)
- P0-P4 framework complete
- Cron self-healing: timeout 120s→300s, agentTurn→command mode
- Delivery fix: feishu user: prefix
- Git cleanup: 380K lines of old archive deleted

### v1.0 (2026-06-24)
- Initial dawn agent framework
- LM Studio + DeepSeek-R1 local inference
- Memory sync and knowledge injection
