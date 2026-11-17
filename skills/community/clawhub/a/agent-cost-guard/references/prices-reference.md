# Reference: provider prices for the models you are most likely to be paying for

Prices are per **1 million tokens** (input / output) as published around **October 2026**, collected for
estimation only. Prices change: verify against your provider before making a money decision. Your invoice is the
authority, not this table.

## Anthropic (Claude)
| Model | Input | Output | Note |
|---|---|---|---|
| Fable 5.1 | 10 | 50 | flagship, 1M context |
| Opus 5.5 | 4 | 20 | cache read about 0.20 |
| Opus 5 / 4.8 / 4.7 | 5 | 25 | 1M context |
| Sonnet 5.5 | 2 | 10 | |
| Sonnet 4.6 | 3 | 15 | |
| Haiku 4.5 | 1 | 5 | cheapest current tier |
| Claude 3 Opus / Opus 4.1 (legacy) | 15 | 75 | the 15 dollars per million rate behind the case study |

## OpenAI
| Model | Input | Output |
|---|---|---|
| GPT-5.5 Pro | 30 | 180 | most expensive in this table |
| GPT-6 Astra | 10 | 50 | flagship |
| GPT-5.6 Sol | 5 | 30 | promotional tier pricing existed |
| GPT-6.1 Sol | 2 | 10 | |
| GPT-6 Luna | 0.10 | 0.50 | cheapest |

## Google (Gemini)
| Model | Input | Output | Note |
|---|---|---|---|
| Gemini 3.1 Pro | 2 | 12 | documented long-context surcharge above 200k tokens |
| Gemini 3.6 Flash | 1.50 | 7.50 | |
| Gemini 2.5 Flash-Lite | 0.10 | 0.40 | cheapest |

## Vendors with peak / off-peak pricing
Some vendors bill a higher rate during defined peak windows and a lower rate off-peak. One example measured in
October 2026: DeepSeek V4.1 Flash, vendor-direct, off-peak input about 0.15 / output about 0.60, cache hit about
0.003, and **double** those rates at peak; peak was Monday to Friday, 09:00-12:00 and 14:00-18:00 Beijing time.
When your vendor prices this way, always compute and report **both** numbers - a single number is wrong half the
day.

## What to do with this
1. Take your token totals per model per day from your agent's own usage records.
2. Multiply by the row you matched. If a model name does not match exactly, match on the longest known prefix and
   say which row you used.
3. If nothing matches, report "not computable" and ask the provider - never invent a rate.
4. Check whether a cheaper model would do the job for background work. That is usually where the money is.
