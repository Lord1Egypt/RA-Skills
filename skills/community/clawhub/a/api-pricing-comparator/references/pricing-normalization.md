# Pricing Normalization Rules

Use these rules before comparing providers, gateways, or model vendors.

## Required normalization steps

1. Identify billing unit
   - input tokens
   - output tokens
   - cached input tokens
   - images / requests / minutes when applicable

2. Normalize the price basis
   - prefer per 1M tokens for text models
   - if source uses 1K tokens, convert to 1M tokens
   - keep image/video/audio units explicit; do not force them into token units

3. Separate price dimensions
   - input price
   - output price
   - cached input price
   - fixed monthly/platform fees if any

4. State assumptions explicitly
   - sample workload ratio (for example 3:1 input:output)
   - whether caching is used
   - whether prices are list prices or gateway prices
   - whether routing/convenience features change value beyond raw unit price

## Practical comparison rules

- Do not compare token and image pricing as if they are the same unit.
- Do not hide missing pricing fields; mark them as unavailable.
- If one provider bundles platform value (routing, unified billing, multi-model access), mention that separately from unit price.
- If exact workload is unknown, provide scenario-based estimates instead of fake precision.

## Recommended output sections

1. Scope and assumptions
2. Normalized pricing table
3. Cheapest options
4. Best-value options
5. Tradeoffs beyond raw price
6. Best fit by customer segment
7. Final recommendation

## Suggested customer segments

- hobby / side project
- startup shipping fast
- production team optimizing cost
- enterprise needing reliability / vendor flexibility
