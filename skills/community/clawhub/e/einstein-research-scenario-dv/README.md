# Headline Scenario Analyzer

Multi-agent scenario analysis framework that projects 18-month investment implications from news headlines.

## Description

Headline Scenario Analyzer takes news headlines as input and generates comprehensive 18-month investment scenarios through a two-agent workflow. The scenario-analyst agent performs primary analysis (first, second, and third-order effects), while the strategy-reviewer agent provides critical second opinion. The skill outputs detailed reports in Japanese covering sector impacts, stock recommendations, and strategic positioning.

## Key Features

- **Multi-agent workflow** - Primary analyst + critical reviewer for balanced perspective
- **18-month horizon** - Medium-term scenario projection (not short-term reactions)
- **Layered impact analysis** - First-order (direct), second-order (ripple), third-order (structural)
- **Sector mapping** - Identify winners, losers, and neutral sectors
- **Stock recommendations** - Specific ticker suggestions with rationale
- **Japanese output** - Comprehensive reports in Japanese for local investors
- **Multiple scenarios** - Base case, optimistic, pessimistic paths

## Quick Start

```bash
# Install dependencies (if using LLM agents)
# Configure scenario-analyst and strategy-reviewer agents

# Analyze a headline
python3 scripts/scenario_analyzer.py \
  --headline "Fed raises interest rates by 50bp, signals more hikes ahead" \
  --output reports/

# OR trigger via skill command
/headline-scenario-analyzer "China announces new tariffs on US semiconductors"
```

**Output Structure:**
```
reports/
  scenario_analysis_<topic>_YYYYMMDD.md
    - ヘッドライン分析
    - 1次影響（直接的影響）
    - 2次影響（波及効果）
    - 3次影響（構造変化）
    - セクター別影響マップ
    - 推奨銘柄リスト
    - セカンドオピニオン（reviewer）
    - 総合評価
```

## Example Use Cases

- **Fed rate decision** - "Fed raises rates by 50bp" → Impact on tech, REITs, financials
- **Geopolitical events** - "China tariffs on semiconductors" → Supply chain, alternatives
- **Commodity shocks** - "OPEC cuts production by 2M bpd" → Energy sector, inflation
- **Regulatory changes** - "EU carbon tax on imports" → Materials, industrials, ESG winners

## What It Does NOT Do

- Does NOT provide short-term trading signals (18-month horizon only)
- Does NOT execute trades or manage portfolios
- Does NOT guarantee scenario accuracy (probabilistic analysis)
- Does NOT work without configured LLM agents (scenario-analyst, strategy-reviewer)
- Does NOT provide real-time news monitoring (manual headline input)

## Requirements

- Python 3.8+
- LLM agents configured: scenario-analyst, strategy-reviewer
- Access to market data for validation (optional)
- Japanese language support for output

## License

MIT
