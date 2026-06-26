---
name: clawswarm
description: "Multi-agent swarm prediction with consensus engine. Use when: running multiple AI agents to predict prices, values, or outcomes and aggregating their predictions into a consensus. Supports any LLM provider (Groq, OpenAI, Ollama), configurable agent roles/temperatures, and a statistical consensus pipeline (MAD outlier filtering, adaptive anchoring, bias correction, weighted median aggregation). Triggers: swarm prediction, multi-agent consensus, collective intelligence forecasting, price prediction with multiple agents."
---

# ClawSwarm

Multi-agent collective intelligence framework. Run N agents with different analytical perspectives, aggregate predictions through a statistical consensus engine.

## Quick Start

### 1. Create a config file

```yaml
target:
  name: "Gold"
  current_price: 5023.1
  unit: "USD/troy oz"
  context: "RSI: 40.8 | MA5: 5084 | MA10: 5120"

agents:
  - role: "Macro analyst focusing on geopolitical risk"
    count: 50
    temperature_range: [0.4, 0.7]
  - role: "Technical RSI/MACD momentum trader"
    count: 30
    temperature_range: [0.45, 0.6]
  - role: "Mean reversion auditor"
    count: 20
    temperature_range: [0.35, 0.55]

api:
  provider: groq
  model: llama-3.3-70b-versatile
  api_key_env: GROQ_API_KEY
  delay_ms: 1200

consensus:
  max_deviation: 0.15
```

### 2. Run the swarm

```bash
python3 scripts/swarm_runner.py --config swarm.yaml
```

Output: JSON with `final_price`, `median_price`, `confidence`, `bull_ratio`, and all individual predictions.

### 3. Run consensus standalone

Pipe any predictions array to the consensus engine:

```bash
echo '{"predictions":[{"price":100.5,"confidence":70},{"price":99.8,"confidence":60}],"anchor_price":100.0}' \
  | python3 scripts/consensus.py
```

## Architecture

```
Config (YAML/JSON)
  ↓
Swarm Runner (swarm_runner.py)
  ├─ Agent 1 → LLM API → prediction
  ├─ Agent 2 → LLM API → prediction
  ├─ ...
  └─ Agent N → LLM API → prediction
  ↓
Consensus Engine (consensus.py)
  ├─ Bias correction
  ├─ MAD outlier filtering
  ├─ Anchor-distance filtering
  ├─ Multi-method aggregation (weighted 40% + median 35% + trimmed mean 25%)
  ├─ Adaptive anchoring (dispersion → anchor strength)
  └─ Clamping
  ↓
Final consensus prediction + confidence + bull/bear ratio
```

## Key Concepts

**Agent diversity**: Each agent gets a different role prompt and temperature. More diversity = better consensus.

**Consensus engine**: Not a simple average. Uses MAD (Median Absolute Deviation) to filter outliers, adaptive anchoring to stabilize results when predictions are dispersed, and multi-method aggregation for robustness.

**1 agent or 1000**: Works with any count. Single agent bypasses consensus. 5+ agents get full pipeline.

## Config Reference

See `references/config-reference.md` for full field documentation and example configs.

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/swarm_runner.py` | Orchestrate multi-agent predictions |
| `scripts/consensus.py` | Standalone consensus engine (pipe JSON in) |

## Dependencies

- Python 3.8+
- `numpy` (for consensus engine)
- `requests` or `urllib` (for API calls)
- `pyyaml` (optional, for YAML configs; JSON always works)
