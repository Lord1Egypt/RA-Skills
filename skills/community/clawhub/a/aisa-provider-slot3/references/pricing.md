# AIsa Pricing Notes

> Prices and model catalogs change. Treat this file as a historical reference only and verify the latest numbers at https://marketplace.aisa.one/pricing before making operational or purchasing decisions.

## Official Sources To Check First

- Pricing page: https://marketplace.aisa.one/pricing
- API docs: https://aisa.one/docs/api-reference
- Model catalog: `GET https://api.aisa.one/v1/models`

## Indicative Snapshot

The values below are a lightweight early-2026 snapshot, kept only to show rough ordering between common models.

| Model | Example ID | Indicative Input | Indicative Output |
|-------|------------|------------------|-------------------|
| Qwen MT Flash | `aisa/qwen-mt-flash` | ~$0.05 / 1M | ~$0.30 / 1M |
| Qwen Plus | `aisa/qwen-plus-2025-12-01` | ~$0.30 / 1M | ~$0.90 / 1M |
| Qwen3 Max | `aisa/qwen3-max` | ~$1.20 / 1M | ~$4.80 / 1M |
| DeepSeek V3.1 | `aisa/deepseek-v3.1` | ~$0.27 / 1M | ~$1.10 / 1M |
| Kimi K2.5 | `aisa/kimi-k2.5` | ~$0.60 / 1M | ~$2.40 / 1M |

## What To Re-Verify Before Production Use

- whether the model ID is still live in the current catalog
- whether retention, routing, and downstream-provider terms match your data requirements
- whether region, quota, rate limit, or account-tier behavior changed
- whether model-specific constraints such as Kimi temperature handling still apply

## Practical Guidance

- do not hard-code business decisions around old snapshot pricing
- prefer a dedicated, revocable API key for provider testing
- for sensitive or regulated workloads, confirm privacy and retention terms directly with the current provider documentation
