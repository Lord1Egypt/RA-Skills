# Disclaimer

- Play-money system. This skill trades propSPACE play-money ($1,000 bankroll per round). The prize pool is real USDC, administered entirely by FunctionSpace, not Simmer. Simmer makes no representations about prize payouts.
- No performance guarantees. Edges depend on the consensus distribution, market mechanics, data accuracy, and timing.
- High variance. Player fantasy scores are noisy. One match is a small sample, and a good projection still loses often.
- Dry-run by default. Pass --live explicitly to place propSPACE play-money positions.
- Data currency. Base projections come from FunctionSpace market metadata. Optional sentiment enrichment (`data/player_data.json`) is manually maintained, refresh with scripts/enrich_from_web.py before each round.
- Engine stability. FunctionSpace runs on a single Render instance. Treat the skill as best-effort if the engine is unreachable.
