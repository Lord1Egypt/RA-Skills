# Routing Playbooks — Deep Infra

## Workload Classes

Define routing by workload first, then select models.

| Workload | Primary Objective | Suggested Model | Fallback Model |
|----------|-------------------|-----------------|----------------|
| Short coding tasks | Fast turnaround | `stepfun-ai/Step-3.5-Flash` | `deepseek-ai/DeepSeek-V3.2` |
| Deep analysis | Reasoning quality | `zai-org/GLM-5.1` | `moonshotai/Kimi-K2.5` |
| Long-context synthesis | Context capacity | `moonshotai/Kimi-K2.5` | `MiniMaxAI/MiniMax-M2.5` |
| Extraction and formatting | Deterministic output | `deepseek-ai/DeepSeek-V3.2` | `stepfun-ai/Step-3.5-Flash` |
| Heavy reasoning | Complex multi-step tasks | `nvidia/NVIDIA-Nemotron-3-Super-120B-A12B` | `zai-org/GLM-5.1` |

## Available Key Models

| Model | Strengths |
|-------|-----------|
| `stepfun-ai/Step-3.5-Flash` | Fast inference, good for coding and quick tasks |
| `zai-org/GLM-5.1` | Strong reasoning, default recommended model |
| `MiniMaxAI/MiniMax-M2.5` | Reasoning capable, large context window |
| `moonshotai/Kimi-K2.5` | Vision + reasoning, 262K context window |
| `nvidia/NVIDIA-Nemotron-3-Super-120B-A12B` | Large parameter count, strong reasoning |
| `deepseek-ai/DeepSeek-V3.2` | Versatile, good cost-to-quality ratio |

Model refs in OpenClaw use the `deepinfra/` prefix (e.g., `deepinfra/zai-org/GLM-5.1`).

## Decision Sequence

1. Identify workload class and acceptable latency.
2. Choose primary model for that class.
3. Assign fallback from a different model family when possible.
4. Define trigger: timeout, rate limit, or quality threshold.
5. Validate with a small prompt set before rollout.

## Verification Prompt Set

Use 3-5 representative prompts per workload class:

- One typical case
- One edge case with long or noisy input
- One strict-format output case

Track success rate, latency, and output consistency before finalizing policy.

## Anti-Pattern

Using one "best model" for every workflow causes avoidable cost spikes and weak reliability when task shapes change. Leverage DeepInfra's diverse model catalog to match models to workloads.
