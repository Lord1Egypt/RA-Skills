# Competitive-Ops v2

AI-powered competitive analysis pipeline for Claude Code.

<p align="center">
  <a href="https://github.com/anthropics/claude-code">
    <img src="https://img.shields.io/badge/Claude_Code-000?style=flat&logo=anthropic&logoColor=white" alt="Claude Code">
  </a>
  <a href="https://github.com/nextlevelbuilder/ui-ux-pro-max-skill">
    <img src="https://img.shields.io/badge/Design_System-ui--ux--pro--max-blue?style=flat" alt="UI UX Pro Max">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License">
  </a>
</p>

---

## What Is This

Competitive-Ops is a **Claude Code Skill** — callable via `/competitive-ops` or natural language (e.g., "analyze Anthropic"), it turns Claude Code into a **competitive intelligence command center**.

### Pain Points Solved

- **No historical persistence** — ChatGPT-based research starts fresh every session. Competitive insights disappear after each conversation.
- **Blind to changes** — Pricing adjustments, product launches, and market shifts go unnoticed until manually rediscovered.
- **Unstructured outputs** — Ad-hoc analysis produces inconsistent formats that resist aggregation, comparison, or trending.
- **Reactive posture** — Competitive intelligence remains firefighting rather than systematic, continuous monitoring.

### What You Get

An AI-powered competitive intelligence pipeline:

- **Structured analysis** — SWOT framework + 6-dimension scoring with industry-specific templates
- **Professional reporting** — Markdown and HTML reports with ECharts visualizations
- **Automatic change detection** — ANY pricing change triggers alerts (no threshold), feature deltas tracked over time
- **Side-by-side comparison** — Multi-competitor matrix with scoring delta analysis
- **Batch processing** — Multi-agent parallelism (~3x speedup), independent context windows per agent
- **Deep pricing dive** — Value scoring (features/$) with market normalization

---

## Quick Start

### 1. Install

```bash
# Clone the repo
git clone https://github.com/YOUR_ORG/competitive-ops-v2.git
cd competitive-ops-v2

# Install Python dependencies
pip install -r requirements.txt

# Configure (copy and edit)
cp config/profile.yml config/profile.yml  # Your company info
```

### 2. Configure API Keys (Optional)

```bash
# Add to your environment or .env file
export TAVILY_API_KEY="tvly-xxxxx"
```

Get a Tavily API key at [tavily.com](https://tavily.com).
Or use Tavily MCP server if configured in Claude Code.

### 3. Use in Claude Code

```bash
claude

# Add a competitor
/competitive-ops add Anthropic

# Full analysis with HTML report
/competitive-ops analyze Anthropic

# Compare two competitors
/competitive-ops compare Anthropic vs OpenAI

# Check pricing changes
/competitive-ops pricing Anthropic

# View all tracked competitors
/competitive-ops track
```

---

## Features

### Skill Modes

| Command | Description |
|---------|-------------|
| `/competitive-ops setup` | Install dependencies and configure system |
| `/competitive-ops add <company>` | Add a competitor to tracking |
| `/competitive-ops analyze <company>` | Full analysis: SWOT + scoring + HTML report |
| `/competitive-ops compare <A> vs <B>` | Side-by-side feature matrix |
| `/competitive-ops update <company>` | Check for changes since last analysis |
| `/competitive-ops pricing <company>` | Pricing research with change detection |
| `/competitive-ops pricing-deep-dive <company>` | Deep pricing analysis with value scoring |
| `/competitive-ops batch` | Batch process multiple competitors (supports `tier 1/2/3` filter) |
| `/competitive-ops report` | Generate consolidated report |
| `/competitive-ops track` | View tracking dashboard |
| `/competitive-ops monitor [daily\|weekly\|monthly]` | Set up scheduled monitoring (uses `/loop` for continuous updates) |
| `/competitive-ops pdf [report]` | Export report to PDF (uses Playwright) |
| `/competitive-ops png [report]` | Export report to PNG image (uses Playwright) |

### Scoring System

Evaluate competitors across 6 dimensions (1-5 scale):

| Dimension | Weight |
|-----------|--------|
| Product Maturity | 20% |
| Feature Coverage | 20% |
| Pricing | 15% |
| Market Presence | 15% |
| Growth Trajectory | 10% |
| Brand Strength | 10% |

### Archetype Detection

Classify competitors into types:

- **Direct Competitor** — Same product, same market
- **Indirect Competitor** — Different approach, same need
- **Emerging Threat** — New technology, new model
- **Replacement Threat** — Alternative solution
- **Adjacent Player** — Overlapping users
- **Reference Model** — Industry benchmark

### Confidence Scoring

Data is cross-validated from multiple sources:

| Level | Condition |
|-------|-----------|
| 🟢 High | 3+ sources agree |
| 🟡 Medium | 2 sources agree |
| 🔴 Low | Conflicting or insufficient data |

### Industry Templates

Industry-specific SWOT questions and scoring weights:

| Industry | Focus | Key Metrics |
|----------|-------|-------------|
| AI (default) | Model capabilities, API pricing | Tokens/$, context window |
| SaaS | MRR, churn, NPS | Net Revenue Retention, integrations |
| FinTech | Compliance, security | Transaction volume, fraud rate |

Set in `config/profile.yml`:
```yaml
company:
  industry: "saas"  # ai, saas, or fintech
```

### Pricing Deep Dive

Track competitor pricing changes with value scoring:

```bash
/competitive-ops pricing-deep-dive Anthropic
```

- **Value Score** = (Feature Count / Price) × Market Normalization
- **ANY pricing change triggers alert** (no threshold)
- Stores snapshots in `data/pricing-snapshots/{company}.json`

---

## Project Structure

```
competitive-ops-v2/
├── CLAUDE.md                        # Project instructions
├── cv.md                           # Your product definition (user layer)
├── config/
│   ├── profile.yml                # Company/product config (user layer)
│   └── industry-profiles.yml      # Industry configurations (AI/SaaS/FinTech)
├── .claude/skills/competitive-ops/ # Skill definitions
│   ├── SKILL.md                   # Router + mode definitions
│   └── modes/                    # Mode implementations
├── scripts/                        # Python utilities
│   └── pricing_analyzer.py        # Value scoring & change detection
├── templates/
│   └── report/
│       └── markdown/              # Report templates
│           ├── swot-template-ai.md
│           ├── swot-template-saas.md
│           ├── swot-template-fintech.md
│           └── pricing-deep-dive-template.md
├── modes/
│   ├── _industry-context.md      # Industry-specific SWOT questions
│   ├── _shared.md                # Shared rules and scoring
│   ├── _profile.md              # User customizations
│   ├── add.md, analyze.md, batch.md, compare.md
│   ├── pricing.md, pricing-deep-dive.md, report.md
│   ├── track.md, update.md, monitor.md, pdf.md, png.md
├── data/
│   ├── competitors.md              # Competitor tracker
│   ├── batch-queue.md             # Batch queue
│   ├── batch-status.json          # Batch processing status
│   ├── pricing-snapshots/         # JSON pricing snapshots
│   │   └── {company}.json
│   ├── reports/
│   │   ├── {date}/               # Dated reports
│   │   └── latest/                # Symlinks to latest
│   └── snapshots/                 # Historical snapshots
└── exports/                        # PNG/PDF exports
    └── index-{date}.png
```

---

## Output Examples

### Report File Structure

```
data/reports/
├── 2026-04-07/
│   ├── anthropic-2026-04-07.md
│   ├── openai-2026-04-07.md
│   ├── pricing-deep-dive-anthropic-2026-04-07.md
│   └── consolidated-2026-04-07.md
└── latest/                        # Symlinks to latest
    ├── anthropic.md → ../2026-04-07/anthropic-2026-04-07.md
    └── openai.md → ../2026-04-07/openai-2026-04-07.md
```

### Markdown Report

```markdown
# Competitive Analysis: Anthropic

**Date:** 2026-04-07
**Tier:** 1 (Direct Competitor)
**Overall Score:** 79.6 / 100
**Confidence:** High (multiple source validation)

## Scoring Matrix

| Dimension | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Product Maturity | 4.6 | 20% | 0.92 |
| Feature Coverage | 4.6 | 20% | 0.92 |
| Pricing | 4.3 | 15% | 0.645 |
| Market Presence | 4.1 | 15% | 0.615 |
| Growth Trajectory | 4.5 | 10% | 0.45 |
| Brand Strength | 4.3 | 10% | 0.43 |
| **TOTAL** | | **100%** | **3.98 → 79.6** |
```

### HTML Report

Professional, responsive HTML reports with Tailwind dark theme:
- Executive summary with score overview
- Scoring matrix with progress bars
- SWOT analysis in 4-quadrant grid
- Key findings and risk assessment
- **Interactive ECharts visualizations:**
  - Score bar chart (ranking by overall score)
  - Radar chart (6 dimensions across all competitors)
  - Pricing heatmap (API prices by model)
- **Pricing change alerts** with 🔴 delta badges
- **PDF export** with Playwright rendering and page-break control

### PDF Export

Export reports for external sharing:
```bash
node scripts/export_pdf.js data/reports/html/index.html
```
- Uses Playwright to wait for ECharts rendering
- A4 format with 15mm margins
- Page numbers in footer
- CSS page-break control prevents section splitting

### PNG Export

Export reports as high-resolution images:
```bash
node scripts/export_image.js data/reports/html/index.html
node scripts/export_image.js data/reports/html/index.html --full  # Full page
node scripts/export_image.js data/reports/html/index.html --jpeg   # JPEG format
```
- Captures ECharts with full rendering
- Dark background preserved
- PNG default, JPEG option available
- Viewport or full page capture modes

---

## Data Privacy

- **Local-first**: All data stored in your project directory
- **No external APIs** without your consent (Tavily is opt-in)
- **User layer**: Your CV, profile, and tracker are never shared
- **System layer**: Skill modes can be updated without overwriting your config

---

## Contributing

1. Fork the repo
2. Create a feature branch
3. Make changes
4. Submit a PR

---

## License

MIT — free to use, modify, and distribute.

---

## Related

- [ui-ux-pro-max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) — Design system for AI agents
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) — AI coding assistant
