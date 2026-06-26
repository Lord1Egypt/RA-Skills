# Eval Criteria for Prediction Market Strategy Quality

Use these binary yes/no criteria to evaluate the quality of a prediction market strategy (strategy.py).
Each criterion should be answered YES or NO. Count the YESes for the pass rate.

1. Does the strategy apply a credibility weight that regresses far-future markets toward 0.5 (to account for uncertainty in long-dated predictions)? → yes/no

2. Does the strategy correct for at least one known systematic bias (e.g., framing bias, status quo bias, overconfidence on novel events)? → yes/no

3. Are all signal weights explicitly defined as named constants (not magic numbers) and do they sum to approximately 1.0? → yes/no

4. Does the strategy avoid using any signals that require external API access unavailable at backtest time (i.e., is it self-contained and backtestable offline)? → yes/no

5. Does the strategy clip final probabilities to a range like [0.05, 0.95] to avoid overconfident predictions at the extremes? → yes/no
