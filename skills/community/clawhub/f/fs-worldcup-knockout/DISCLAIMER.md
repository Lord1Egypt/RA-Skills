# Disclaimer

- **Play-money system.** This skill trades propSPACE play-money ($1,000 per session). The prize pool is real USDC — administered entirely by FunctionSpace, not Simmer. Simmer makes no representations about prize payouts.
- **No performance guarantees.** Historical conversion rates are backward-looking. Edges depend on consensus distribution, market mechanics, data accuracy, and timing.
- **High variance events.** Penalty outcomes are inherently stochastic. An 85% converter misses 1 in 6.
- **Dry-run by default.** Pass `--live` explicitly to place positions.
- **Data currency.** `penalty_data.json` is manually maintained. Refresh WC stats before each round with `fetch_wc_shootouts.py`.
- **Engine stability.** FunctionSpace runs on a single Render instance (dev + prod). Treat the skill as best-effort if the engine is unreachable.
