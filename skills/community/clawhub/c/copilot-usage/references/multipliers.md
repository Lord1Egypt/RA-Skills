# GitHub Copilot — Model Multipliers

Source: https://docs.github.com/en/copilot/concepts/billing/copilot-requests#model-multipliers
Last verified: 2026-04

## Key Concepts

- **Multiplier**: how many premium requests are charged per actual user prompt
- **grossQuantity** in the API response already includes the multiplier
- To calculate actual prompts sent: `actual_prompts = grossQuantity / multiplier`
- GPT-4.1, GPT-4o, GPT-5 mini = **0× multiplier on paid plans** (free, unlimited)
- Auto model selection in VS Code gives a **10% discount** (e.g., Sonnet 4.6 → 0.9×)

## Multiplier Table (as of April 2026)

| Model                          | Multiplier (Paid Plans) | Multiplier (Free Plan) | Notes                        |
|-------------------------------|------------------------|------------------------|------------------------------|
| GPT-5 mini                    | 0 (free)               | 1                      | Included model               |
| GPT-4.1                       | 0 (free)               | 1                      | Included model               |
| GPT-4o                        | 0 (free)               | 1                      | Included model               |
| Claude Haiku 4.5              | 0.33                   | 1                      |                              |
| Gemini 3 Flash                | 0.33                   | N/A                    |                              |
| Claude Sonnet 4               | 1                      | N/A                    |                              |
| Claude Sonnet 4.5             | 1                      | N/A                    |                              |
| Claude Sonnet 4.6             | 1                      | N/A                    | Subject to change; 0.9× with auto-select |
| Gemini 2.5 Pro                | 1                      | N/A                    |                              |
| Gemini 3.1 Pro                | 1                      | N/A                    |                              |
| Claude Opus 4.5               | 3                      | N/A                    |                              |
| Claude Opus 4.6               | 3                      | N/A                    |                              |
| Claude Opus 4.6 (fast, preview)| 30                    | N/A                    | Experimental                 |
| Spark (any model)             | 4 (fixed)              | N/A                    | Fixed rate, not per-model    |

## Lookup Map for Scripts

```python
MODEL_MULTIPLIERS = {
    "gpt-5 mini":                     0,
    "gpt-4.1":                        0,
    "gpt-4o":                         0,
    "claude haiku 4.5":               0.33,
    "gemini 3 flash":                 0.33,
    "claude sonnet 4":                1,
    "claude sonnet 4.5":              1,
    "claude sonnet 4.6":              1,
    "gemini 2.5 pro":                 1,
    "gemini 3.1 pro":                 1,
    "claude opus 4.5":                3,
    "claude opus 4.6":                3,
    "claude opus 4.6 (fast mode)":    30,
}
DEFAULT_MULTIPLIER = 1  # assume 1x for unknown models
```

## Notes

- Multipliers may change as GitHub updates pricing — always verify at the source URL above
- The `pricePerUnit` field in the API response is always $0.04 (the overage rate), not the multiplier
- `discountQuantity` = requests covered by plan allowance (not billed)
- `netQuantity` = overage requests actually billed at $0.04 each
