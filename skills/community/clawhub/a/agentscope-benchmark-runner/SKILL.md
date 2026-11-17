---
name: agentscope-benchmark-runner
description: Run benchmarks against AgentScope 2.0 agents and pipelines. Use this when the user wants to measure latency, throughput, token usage, or compare model/prompt performance in a reproducible way.
version: 0.1.0
metadata:
  openclaw:
    requires:
      env:
        - OPENAI_API_KEY
      bins:
        - python3
    primaryEnv: OPENAI_API_KEY
    envVars:
      - name: OPENAI_API_KEY
        required: false
        description: Optional API key for live benchmark runs.
      - name: AGENTSCOPE_MODEL
        required: false
        description: Optional default model for benchmark configs.
    emoji: "🏁"
    homepage: https://github.com/agentscope-ai/agentscope
---

# AgentScope Benchmark Runner

This skill generates benchmark configs and a runner for AgentScope 2.0 agents. It focuses on reproducible performance measurement for:

- single-agent latency
- pipeline throughput
- token usage estimation
- prompt variant comparison

## What this skill does

- Creates benchmark scenario files
- Generates a runner script for repeated measurements
- Outputs JSON/CSV results for analysis
- Supports baseline and variant comparisons

## How to use

Run the generator script from this skill folder:

```bash
python3 scripts/generate_benchmark.py --output /path/to/benchmarks --scenario latency
```

Supported scenarios:

- `latency` - single request latency benchmark
- `throughput` - concurrent request throughput benchmark
- `compare` - prompt/model variant comparison

After generation:

```bash
cd /path/to/benchmarks
python run_benchmark.py
```

## Security notes

- Generated configs use placeholder API keys
- No secrets are hardcoded in benchmark files
- Results files may contain prompt text; review before sharing

## Troubleshooting

- If agentscope import fails, install the package: `pip install agentscope`
- For model-specific benchmarks, configure the provider credentials
- High concurrency benchmarks may hit rate limits; adjust `--concurrency`
