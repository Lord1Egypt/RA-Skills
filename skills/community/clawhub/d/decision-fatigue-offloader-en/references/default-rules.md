# Default Rules
## Default City
Beijing. Used when the user has not provided a city. If a city name such as "Shanghai / Hangzhou / Chengdu / Changsha" appears in the user's message, prefer it.
## City Cost Multiplier Table (baseline = new tier-1 cities, multiplier 1.0)
Multipliers are estimated from 2026 fast-food lunch prices, delivery average order values, and per-capita consumption gradients across cities. **They multiply price thresholds only — never preferences.**
| City / Tier | Dining | Shopping | Leisure |
|---|---|---|---|
| Shanghai, Beijing | 1.5 | 1.3 | 1.2 |
| Shenzhen, Guangzhou | 1.3 | 1.2 | 1.1 |
| Hangzhou, Nanjing, Suzhou | 1.1 | 1.1 | 1.0 |
| Chengdu, Wuhan, Tianjin, Xi'an, Chongqing | 1.0 (baseline) | 1.0 | 1.0 |
| Changsha, Zhengzhou, Jinan, Fuzhou, Foshan, Wuxi | 0.75 | 0.8 | 0.85 |
| Tier-3/4 and below (unlisted cities) | 0.65 | 0.7 | 0.8 |
Reference anchors: a typical fast-food lunch costs about ¥38–42 in Shanghai, ¥30–40 in Beijing, ¥15–25 in Chengdu, ~¥14 in Changsha, and ¥10–15 in Zhengzhou. Delivery average order value: ¥44–47 in Shanghai/Beijing; ¥32–45 in Shenzhen/Hangzhou/Nanjing/Guangzhou.
**Coverage note:** the built-in table covers major Chinese cities. For cities outside China, save your city in `user-rules.md` together with a suitable multiplier (benchmark: new tier-1 = 1.0) so the thresholds scale honestly instead of guessing.
## Dining
**Lunch base budget ¥40, dinner base ¥60.** Actual budget = base × dining multiplier, rounded to the nearest ¥10. Dietary restrictions default to "none"; prefer places within ≤1 km or delivery within 30 minutes; on weekdays, skip anything requiring a queue longer than 10 minutes.
## Clothing
**Not affected by city multipliers.** By feels-like temperature: ≤5°C heavy coat + thermal layer; 6–15°C jacket + long sleeves; 16–25°C single long-sleeve layer or light jacket; ≥26°C short sleeves / breathable fabrics. Rain → bring an umbrella by default. Wind → avoid skirts and wide-leg pants by default.
## Shopping
**Daily-goods base unit-price threshold ¥100**; actual threshold = 100 × shopping multiplier. Below the threshold, pick the first option that is "top-selling with a rating ≥ 4.5"; above it, comparing two candidates is allowed. Gift base budget ¥100–300, multiplied by the shopping multiplier, preferring "returnable" items.
## Leisure
**City multipliers do not change the energy bands, but they do change spend expectations.** Energy ≤2 defaults to "low-effort, can quit anytime"; 3–4 allows "semi-structured"; 5 is required before recommending "going out to socialize". If a recommended activity costs money, adjust the acceptable-price phrasing by the leisure multiplier (e.g., "under ¥100 per person" becomes "under ¥120 per person" in tier-1 cities).
## General
The user saying "whatever" = authorization to decide directly using the default rules and the resolved city, with no follow-up questions. If the same category was already decided today, reuse the previous decision (unless the user says "switch").
