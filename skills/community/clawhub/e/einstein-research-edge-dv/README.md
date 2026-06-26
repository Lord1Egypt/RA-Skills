# Edge Candidate Generator

Convert market observations and anomalies into structured research tickets and pipeline-ready strategy specifications.

## Description

Edge Candidate Generator transforms daily market observations, price anomalies, and trading hypotheses into reproducible research tickets. It performs auto-detection from end-of-day OHLCV data, prioritizes signal quality, validates interface compatibility with the trade-strategy-pipeline Phase I schema, and exports candidates as `strategy.yaml` + `metadata.json` files ready for backtesting.

## Key Features

- **Auto-detection** - Daily EOD scan for price anomalies and patterns
- **Hypothesis structuring** - Convert loose ideas into formal research tickets
- **Pipeline compatibility** - Validates against `edge-finder-candidate/v1` interface
- **Export formats** - YAML strategy specs + JSON metadata for pipeline handoff
- **Preflight validation** - Checks schema compliance before backtest execution
- **Prioritization** - Scores candidates by signal strength and feasibility
- **Split workflow support** - Integrates with hint extraction, concept synthesis, and strategy design

## Quick Start

```bash
# Install dependencies
pip install PyYAML pandas

# Auto-detect candidates from EOD data
python3 scripts/auto_detect_candidates.py \
  --tickers SPY QQQ IWM \
  --lookback 60 \
  --output tickets/

# Export validated ticket to pipeline format
python3 scripts/export_candidate.py \
  --ticket tickets/momentum_breakout_001.yaml \
  --output strategies/momentum_breakout_001/

# Validate pipeline compatibility
python3 scripts/validate_candidate.py \
  --candidate strategies/momentum_breakout_001/strategy.yaml
```

**Output Structure:**
```
strategies/
  <candidate_id>/
    strategy.yaml       # Phase I-compatible spec
    metadata.json       # Provenance + interface version
tickets/
  exportable/          # Ready for pipeline
  research_only/       # Needs refinement
```

## What It Does NOT Do

- Does NOT run backtests (export to trade-strategy-pipeline for that)
- Does NOT provide live trading signals
- Does NOT validate fundamental or macro factors (price action only)
- Does NOT guarantee strategy profitability
- Does NOT work with options or derivatives (equity long/short only)

## Requirements

- Python 3.9+
- PyYAML, pandas
- Access to trade-strategy-pipeline repo for validation
- `uv` (optional, for pipeline-managed validation)

## License

MIT
