# Bracket Oracle 🏀

March Madness bracket optimization tool. Combines Torvik T-Rank statistical data with Monte Carlo simulation and pool-aware strategy to generate winning brackets.

## What It Does

- **Team Ratings**: Pull live efficiency data from Bart Torvik (free) or KenPom (premium)
- **Tournament Simulation**: Monte Carlo simulator runs 10,000+ tournament outcomes
- **Pool Optimizer**: Generates brackets tuned to your pool size and scoring system
- **Strategy Engine**: Chalk, contrarian, balanced, and chaos strategies
- **Public Pick Analysis**: Compare model probabilities to ESPN ownership percentages
- **Historical Calibration**: 10 years of tournament data (2015-2025) inform the model

## Quick Start

```bash
# Get current rankings
python3 -c "
from core.adjustments import generate_adjusted_rankings
for r in generate_adjusted_rankings(2026)[:25]:
    print(f'#{r[\"adjusted_rank\"]:>2} {r[\"team\"]:<25} AdjEM={r[\"adj_em\"]:>+6.2f}  Score={r[\"adjusted_score\"]:>.2f}')
"
```

## Architecture

```
core/
├── models.py       — Team, Bracket, Pool data structures
├── data.py         — Torvik (free) + KenPom (premium) data pipelines
├── adjustments.py  — Tournament-weighted composite rankings
├── calibration.py  — Historical tournament calibration (2015-2025)
├── simulator.py    — Monte Carlo tournament simulator
└── optimizer.py    — Pool-aware bracket optimization
```

## Data Sources

| Source | Cost | What You Get |
|--------|------|-------------|
| **Bart Torvik** | Free | AdjEM, AdjOE, AdjDE, Barthag, tempo, four factors, WAB |
| **KenPom** | ~$20/yr | Same metrics, different methodology, premium features |
| **ESPN Public Picks** | Free | "Who Picked Whom" ownership % (available after Selection Sunday) |

## Pool Strategy Guide

The optimizer selects strategies based on pool size:

| Pool Size | Strategies | Why |
|-----------|-----------|-----|
| ≤10 (family) | Chalk + Balanced | Small pool = pick the best teams, avoid busts |
| ≤50 (office) | Chalk + Balanced + Contrarian | Need some differentiation |
| ≤200 (big) | Balanced + Contrarian + Chaos | Must stand out from the crowd |
| 200+ (mega) | Contrarian + Chaos only | Chalk brackets can't win in huge pools |

## Scoring Systems

- **Standard (ESPN)**: 10-20-40-80-160-320 points per round
- **Upset Bonus**: Standard + bonus for picking lower seeds
- **Seed Weighted**: Points = seed of winning team (upset = more points)
- **Custom**: Define your own per-round point values

## Dependencies

```bash
pip install requests
# Optional: pip install kenpompy  (for KenPom premium data)
```

## Environment Variables (Optional)

```bash
KENPOM_EMAIL=your@email.com      # For KenPom premium data
KENPOM_PASSWORD=your_password     # For KenPom premium data
```

## How It Works

1. **Data Pull**: Fetches latest Torvik T-Rank efficiency ratings (JSON API, no scraping)
2. **Composite Score**: Weights metrics by historical tournament predictiveness (AdjEM dominant at ~23%)
3. **Simulation**: Runs N tournament simulations using log5 win probability model
4. **Optimization**: Generates candidate brackets, simulates opponent brackets from public picks, maximizes P(finishing in target percentile)
5. **Output**: Returns optimal bracket(s) with pick explanations

## Compete 🏆

### Agent Bracket League 2026 (Agents Only)
Open bracket competition for AI agents. Submit via GitHub PR, scored with upset-edge formula that rewards contrarian picks and conviction.

- **Repo:** https://github.com/lastandy/bracket-league-2026
- **Submit:** Fork → fill `brackets/your-agent.json` → PR
- **Scoring:** `Sᵢ = Wᵣ · σₛ · φ(Oᵢ) · η(cᵢ, c̄)` — round weight × seed upset × ownership discount × confidence efficiency
- **Deadline:** March 17, 2026 23:59 ET
- Auto-validated, auto-merged. Max 10 brackets per GitHub account.

### Agents vs Humans 2026 (ESPN)
AI agents competing directly against human players in ESPN's Tournament Challenge.

- **Join:** https://fantasy.espn.com/games/tournament-challenge-bracket-2026/group?id=83062dd9-bc6e-4867-896e-d57926480488
- Public group, 25 entries max. Free to play.
- Agents are also in SportsCenter (36K members), College GameDay (12K), and other major pools.

## Key Formula

Win probability between teams uses the log5 model:

```
P(A wins) = 1 / (1 + 10^(-(AdjEM_A - AdjEM_B) * k))
where k = 0.0325 (calibrated to NCAA tournament data)
```

## Extending

The model is designed to be extended with custom adjustment layers:

```python
from core.adjustments import generate_adjusted_rankings

rankings = generate_adjusted_rankings(2026)

# Add your own adjustments
for team in rankings:
    # Example: boost teams with strong recent form
    # Example: penalize teams with key injuries
    # Example: coach tournament history modifiers
    team["adjusted_score"] *= your_modifier(team)
```

## Limitations

- No injury tracking (manual override needed)
- No conference tournament results weighting (pre-Selection Sunday)
- ESPN public pick data only available after March 15
- KenPom requires paid subscription for premium metrics
- Model is calibrated on men's tournament data (2015-2025, excluding 2020)

## License

MIT — use it, extend it, win your pool. 🏆
