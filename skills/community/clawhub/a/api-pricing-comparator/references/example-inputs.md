# Example Inputs and Use Cases

## Sample structured pricing table

| provider | model | input_per_1m | output_per_1m | cached_input_per_1m | notes |
|---|---|---:|---:|---:|---|
| Provider A | Model X | 2.50 | 10.00 | 0.50 | direct API |
| Provider B | Model X | 2.10 | 9.50 | null | gateway pricing |
| Provider C | Model Y | 0.60 | 2.40 | null | low-cost alternative |

## Example prompts

### Landing page
Turn this normalized pricing table into a pricing comparison section for a product page aimed at developers choosing an AI API gateway.

### Buyer guide
Compare Claude, GPT, Gemini, and DeepSeek pricing for startups that expect medium traffic and need a good quality-to-cost ratio.

### Internal decision
Summarize the cheapest, best-value, and safest long-term options for a team that wants multi-model flexibility without vendor lock-in.

## Output guidance
Always separate:
- raw unit price
- practical value
- customer-segment fit
- caveats caused by missing assumptions
