# ClawSwarm Configuration Reference

## Config Format

YAML or JSON. Pass to swarm_runner.py via `--config`.

## Fields

### target (required)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | yes | Display name (e.g. "Gold", "Copper") |
| current_price | number | yes | Current/reference price |
| unit | string | no | Price unit (e.g. "USD/troy oz") |
| context | string | no | Additional data for agents (indicators, history) |

### agents (required)

Array of agent groups:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| role | string | yes | System prompt / analyst persona |
| count | int | no | Number of agents in group (default: 1) |
| temperature_range | [min, max] | no | Temperature range, evenly distributed (default: [0.5, 0.5]) |
| model | string | no | Override model for this group |

### api (optional)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| provider | string | "groq" | "groq", "openai", or "ollama" |
| model | string | "llama-3.3-70b-versatile" | Model name |
| api_key_env | string | "GROQ_API_KEY" | Env var containing API key |
| api_key | string | - | Direct API key (prefer env var) |
| base_url | string | auto | Override API endpoint |
| max_tokens | int | 150 | Max response tokens |
| delay_ms | int | 1200 | Delay between requests in ms |

### consensus (optional)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| max_deviation | float | 0.15 | Max allowed deviation from anchor (0.15 = 15%) |
| bias | float | 0.0 | Known systematic bias to correct |

## Example Configs

### Minimal (5 agents, Groq)

```yaml
target:
  name: "Gold"
  current_price: 5023.1

agents:
  - role: "Financial analyst"
    count: 5

api:
  api_key_env: GROQ_API_KEY
```

### Full (300 agents, multi-role)

```yaml
target:
  name: "Gold"
  current_price: 5023.1
  unit: "USD/troy oz"
  context: |
    RSI(14): 40.8 | MACD: -48.2
    MA5: 5084 | MA10: 5120 | MA20: 5150
    Recent: -2.1% (5d) | Pattern: 跌→跌→涨→跌→跌

agents:
  - role: "Geopolitical risk analyst. Focus on political risk premium in price trends."
    count: 20
    temperature_range: [0.5, 0.7]
  - role: "Monetary policy analyst. Analyze based on interest rate expectations and MA alignment."
    count: 15
    temperature_range: [0.45, 0.65]
  - role: "Supply-demand fundamentalist. Focus on volume-price divergence signals."
    count: 25
    temperature_range: [0.4, 0.7]
  - role: "RSI momentum trader. Strictly follow overbought/oversold logic."
    count: 20
    temperature_range: [0.45, 0.6]
  - role: "MACD signal specialist. Predict based on MACD direction and magnitude."
    count: 15
    temperature_range: [0.5, 0.65]
  - role: "Mean reversion auditor. Calculate deviation from MA10/MA20 and predict regression."
    count: 30
    temperature_range: [0.35, 0.55]
  - role: "Chief Investment Officer. Synthesize trend, momentum, and volatility for most probable price."
    count: 30
    temperature_range: [0.4, 0.6]

api:
  provider: groq
  model: llama-3.3-70b-versatile
  api_key_env: GROQ_API_KEY
  max_tokens: 150
  delay_ms: 1200

consensus:
  max_deviation: 0.15
  bias: 0.0
```

### Multi-model (mixed providers)

```yaml
target:
  name: "Copper"
  current_price: 5.757
  unit: "USD/lb"

agents:
  - role: "Technical analyst"
    count: 10
    model: llama-3.3-70b-versatile
    temperature_range: [0.4, 0.6]
  - role: "Macro analyst"
    count: 5
    model: gemini-2.0-flash
    temperature_range: [0.5, 0.7]

api:
  provider: groq
  api_key_env: GROQ_API_KEY
```

Note: per-group `model` overrides the global `api.model`.
