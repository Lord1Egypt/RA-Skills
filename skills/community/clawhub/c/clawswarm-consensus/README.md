# 🦞 ClawSwarm

Multi-agent collective intelligence framework for prediction consensus.

Run N AI agents with different analytical perspectives. Aggregate their predictions through a statistical consensus engine. Get a single, robust forecast.

## What It Does

```
Your question (e.g. "What will gold close at tomorrow?")
  ↓
N agents analyze independently (different roles, temperatures, models)
  ↓
Consensus engine filters noise and fuses predictions
  (MAD outlier removal → adaptive anchoring → multi-method aggregation)
  ↓
One consensus prediction + confidence score + bull/bear ratio
```

Works with 1 agent or 1,000. Any LLM provider (Groq, OpenAI, Ollama, etc.).

## Quick Start

### 1. Create a config

```yaml
# swarm.yaml
target:
  name: "Gold"
  current_price: 5023.1
  unit: "USD/troy oz"
  context: "RSI: 40.8 | MA5: 5084 | MA10: 5120"

agents:
  - role: "Macro analyst focusing on geopolitical risk"
    count: 50
    temperature_range: [0.4, 0.7]
  - role: "Technical momentum trader"
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

### 2. Run

```bash
export GROQ_API_KEY=your_key_here
python3 scripts/swarm_runner.py --config swarm.yaml
```

### 3. Or use the consensus engine standalone

```bash
echo '{"predictions":[{"price":100.5,"confidence":70},{"price":99.8,"confidence":60}],"anchor_price":100.0}' \
  | python3 scripts/consensus.py
```

## Consensus Engine

Not a simple average. The pipeline:

1. **Bias correction** — subtract known systematic bias
2. **MAD outlier filtering** — Median Absolute Deviation, more robust than IQR
3. **Anchor-distance filtering** — remove predictions too far from reference price
4. **Multi-method aggregation** — weighted (40%) + median (35%) + trimmed mean (25%)
5. **Adaptive anchoring** — dispersed predictions anchor more to reference price
6. **Clamping** — enforce max deviation bounds

## Agent Design

Each agent gets a unique combination of:
- **Role prompt** — analytical perspective (geopolitical, technical, fundamental, etc.)
- **Temperature** — controls creativity/randomness
- **Model** — can mix providers within one swarm

More agents with more diverse perspectives = better consensus. The engine's outlier filtering ensures bad predictions don't pollute the result.

## Config Reference

See [references/config-reference.md](references/config-reference.md) for full field documentation.

## Dependencies

- Python 3.8+
- `numpy`
- `requests` or `urllib` (stdlib fallback)
- `pyyaml` (optional, for YAML configs)

```bash
pip install numpy pyyaml requests
```

## As an OpenClaw Skill

ClawSwarm is available as an [OpenClaw](https://github.com/openclaw/openclaw) skill:

```bash
clawhub install clawswarm
```

## Origin

This project grew out of prediction market research begun in 2017 under the name *twebet* — an experiment in collective intelligence and crowd-sourced forecasting. ClawSwarm carries that work forward with modern LLM agents as the "crowd."

## License

MIT — see [LICENSE](LICENSE)

## Author

**李卓伦** (Zhuolun Li)
