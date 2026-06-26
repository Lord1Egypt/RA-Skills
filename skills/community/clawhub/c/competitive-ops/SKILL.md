---
name: competitive-ops
description: AI competitive intelligence pipeline -- analyze competitors, generate reports, track changes
author:
  name: 大脸猫
  email: ""
category: productivity
homepage: https://github.com/dalianmao000/competitive-ops-v2
tags:
  - competitive-analysis
  - intelligence
  - market-research
  - reporting
---

# Competitive-Ops -- Router

## Mode Routing

Determine the mode from `{{mode}}`:

| Input | Mode |
|-------|------|
| (empty / no args) | `discovery` -- Show command menu |
| `setup` | `setup` -- Install dependencies and configure system |
| `add <company>` | `add` -- Add competitor to tracking |
| `analyze <company> [html]` | `analyze` -- Full analysis with SWOT + report (add `html` for HTML output) |
| `compare <A> vs <B> [html]` | `compare` -- Side-by-side comparison (add `html` for HTML output) |
| `update <company>` | `update` -- Check for changes |
| `pricing <company> [html]` | `pricing` -- Pricing research (add `html` for HTML output) |
| `pricing-deep-dive <company>` | `pricing-deep-dive` -- Deep pricing analysis with value scoring |
| `batch` | `batch` -- Batch processing |
| `report [html]` | `report` -- Generate consolidated report (add `html` for HTML output) |
| `track` | `track` -- View tracking dashboard |
| `monitor [interval]` | `monitor` -- Set up scheduled monitoring (default: weekly) |
| `pdf [report]` | `pdf` -- Export report to PDF |
| `png [report]` | `png` -- Export report to PNG image |

---

## Discovery Mode (no arguments)

Show this menu:

```
competitive-ops -- Competitive Intelligence Command Center

Available commands:
  /competitive-ops add <company>      → Add competitor to tracking
  /competitive-ops analyze <company>  → Full analysis: SWOT + scoring + HTML report
  /competitive-ops compare <A> vs <B> → Side-by-side feature matrix
  /competitive-ops update <company>   → Check for changes since last analysis
  /competitive-ops pricing <company> → Pricing research with change detection
  /competitive-ops pricing-deep-dive <company> → Deep pricing analysis with value scoring
  /competitive-ops batch              → Batch process multiple competitors
  /competitive-ops report             → Generate consolidated report
  /competitive-ops track             → View tracking dashboard
  /competitive-ops monitor [daily|weekly|monthly] → Set up scheduled monitoring
  /competitive-ops pdf [report]      → Export report to PDF
  /competitive-ops png [report]      → Export report to PNG image

First time? Say "setup" to configure your company info.
```

---

## Setup Mode

If `{{mode}}` is "setup":

### Step 1: Install Dependencies

Check for required tools and install if missing:

1. **Playwright** for screenshots (required):
   - Run: `npx playwright install chromium`
   - Verify: `npx playwright --version`

2. **ui-ux-pro-max** for HTML reports:
   - Install: `npx -y uipro-cli init --ai claude` (in project directory)
   - Skill location: `{project}/.claude/skills/ui-ux-pro-max/`
   - Usage: `/skill ui-ux-pro-max`

3. **Tavily MCP** (optional, for fallback search):
   - Correct package name: `tavily-mcp` (NOT `@tavily/tavily-mcp`)
   - Add with: `claude mcp add tavily -- npx -y tavily-mcp`
   - Set API key: `TAVILY_API_KEY=your_key`

4. **Python dependencies** (required, use virtual environment):
   ```bash
   python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
   ```
   - Or directly: `pip install -r requirements.txt` (in project directory)

### Step 2: Configure System

Check if the system is configured:

1. **Required:** Check if `data/competitors.md` exists
   - If missing, create from template or empty file with headers:
     ```
     # Competitors Tracker
     | # | Company | Tier | Score | Status | Last Updated | Notes |
     |---|---------|------|-------|--------|--------------|-------|
     ```
2. **Optional:** `cv.md` and `config/profile.yml`
   - These define your own product for scoring context
   - Not required for basic competitive analysis
   - If missing, skip and proceed with analysis

### Step 3: Summary

Output setup status:
```
✅ competitive-ops v2 ready!

Installed:
  ✅ Playwright (screenshots)
  ✅ ui-ux-pro-max (HTML reports: npx -y uipro-cli init --ai claude)
  ✅ Tavily MCP (fallback search)
  ✅ Python dependencies

Required:
  ✅ data/competitors.md

Optional (for scoring context):
  [?] cv.md (your product)
  [?] config/profile.yml
```

---

## Add Mode

When `{{mode}}` is `add`:

1. Read `{{company}}` from args
2. Check if competitor already exists in `data/competitors.md`
   - **If exists:** Output warning: "⚠️ {company} already in tracker (score: X)" and skip
   - **If new:** Add entry with tier assignment (Tier 1/2/3)
3. Create initial research structure (snapshot folder)
4. Output confirmation with tier and initial score placeholder

---

## Search Fallback Order

When researching competitors, use this search order:

1. **web-search** → Primary search tool
2. **web-fetch** → Fetch specific URLs for detailed info
3. **Tavily MCP server** → Fallback when native tools unavailable

**Tavily MCP Usage:**
```
Use Tavily MCP server for competitive intelligence search:
- tavily-search for company overview, products, pricing
- tavily-search with topic="business" for business intelligence
- tavily-search with topic="news" for recent news
```

**Fallback Detection:**
- If `web-search` returns no results or error → try `web-fetch`
- If `web-fetch` fails or unavailable → invoke Tavily MCP server
- Always log which search method was used in the report metadata

---

## Analyze Mode

When `{{mode}}` is `analyze`:

1. Read `{{company}}` and optional `{{html}}` flag from args
2. Check if competitor exists in `data/competitors.md`
   - **If new:** Add to `data/competitors.md` first
   - **If exists:** Note: "ℹ️ New analysis for {company}"
3. Run research (following fallback order above):
   - Try web-search first for company info
   - Try web-fetch for specific URLs
   - Fallback to Tavily MCP server if needed
   - Cross-validate from multiple sources
4. Generate SWOT analysis
5. Score across 6 dimensions
6. Generate report in `data/reports/{date}/{company}-{date}.md`
   - **Always creates new file (never overwrites)**
   - **Update symlink** to point to the new report:
     ```bash
     rm -f data/reports/latest/{company}.md
     ln -s ../{date}/{company}-{date}.md data/reports/latest/{company}.md
     ```
     This ensures `latest/` always reflects the most recent analysis, regardless of date.
7. **If `html` flag is present in args:**
   - Read the markdown report
   - Use ui-ux-pro-max skill: `/skill ui-ux-pro-max`
   - Generate HTML report with Tailwind dark theme
   - Save to `data/reports/html/{company}-{date}.html`
8. Update `data/competitors.md` with new score and date
9. Output summary with score and confidence
   - Include path to HTML report if generated

**Note:** For incremental change tracking, use `update` mode instead. `analyze` always creates fresh analysis.

---

## Compare Mode

When `{{mode}}` is `compare`:

1. Parse `A vs B` and optional `{{html}}` flag from args
2. Load both companies' latest reports from `data/reports/latest/`
3. Generate feature matrix comparison
4. Score delta analysis
5. Save comparison to `data/reports/{date}/compare-{A}-vs-{B}-{date}.md`
6. **If `html` flag is present:**
   - Read the comparison markdown
   - Use ui-ux-pro-max skill: `/skill ui-ux-pro-max`
   - Generate HTML report with Tailwind dark theme
   - Save to `data/reports/html/compare-{A}-vs-{B}-{date}.html`
7. Output path to comparison report

---

## Update Mode

When `{{mode}}` is `update`:

1. Read `{{company}}` from args
2. Re-run research (following Search Fallback Order):
   - Try web-search/web-fetch first
   - Fallback to Tavily MCP if unavailable
3. Load the previous report from `data/reports/{company}-{prev-date}.md` as baseline
4. Generate new analysis: SWOT + scores → new `data/reports/{company}-{date}.md`
5. **Diff analysis:** Compare old vs new report, compute score delta per dimension
6. **If score change ≥ 5% on any dimension → alert user with 🔴 flag**
7. Save snapshot to `data/snapshots/{company}/{date}.json`
8. Output:
   - New report path
   - Score delta table (before → after per dimension)
   - Changelog: what changed (new features, pricing changes, etc.)

---

## Pricing Mode

When `{{mode}}` is `pricing`:

1. Read `{{company}}` and optional `{{html}}` flag from args
2. Research pricing from (following fallback order):
   - Company website (try web-fetch first)
   - G2, Capterra, Glassdoor
   - News articles
   - Tavily MCP server as fallback for business intelligence
3. Compare to `data/snapshots/pricing/{company}.json`
4. If change detected, alert user with change details
5. Update `data/snapshots/pricing/{company}.json`
6. Save pricing report to `data/reports/{date}/pricing-{company}-{date}.md`
7. **If `html` flag is present:**
   - Read the pricing report markdown
   - Use ui-ux-pro-max skill: `/skill ui-ux-pro-max`
   - Generate HTML report with Tailwind dark theme
   - Save to `data/reports/html/pricing-{company}-{date}.html`
8. Output pricing table

---

## Pricing Deep Dive Mode

When `{{mode}}` is `pricing-deep-dive`:

1. Read `{{company}}` from args
2. Research comprehensive pricing data from (following fallback order):
   - Company website (web-fetch first for pricing pages)
   - G2, Capterra, TrustRadius for verified pricing
   - News articles mentioning pricing changes
   - Tavily MCP server for business intelligence
3. Load previous snapshot from `data/pricing-snapshots/{company}.json` (if exists)
4. **Build PricingSnapshot using scripts/pricing_analyzer.py:**
   ```python
   from scripts.pricing_analyzer import PricingSnapshot, Plan, PricingAnalyzer, save_snapshot

   snapshot = PricingSnapshot(
       company="CompanyName",
       last_updated="2026-04-07",
       plans=[
           Plan(
               name="Pro",
               type="subscription",
               price=20.0,
               period="monthly",
               users=10,
               api_access=True,
               price_per_1m_input=1.0,
               price_per_1m_output=3.0,
               features=["API Access", "Advanced Analytics", "Priority Support"]
           )
       ],
       enterprise=True,
       free_tier=True,
       sources=["https://example.com/pricing"]
   )
   ```
5. **Compute value scores using PricingAnalyzer:**
   ```python
   analyzer = PricingAnalyzer(subscription_baseline=10.0, api_baseline=1.0)
   for plan in snapshot.plans:
       score = analyzer.compute_value_score(plan)
       print(f"{plan.name}: {score:.2f}")
   ```
6. **Detect changes using PricingChangeDetector:**
   ```python
   from scripts.pricing_analyzer import PricingChangeDetector

   detector = PricingChangeDetector(any_change=True)  # Alert on ANY change
   if old_snapshot:
       changes = detector.detect_change(old_snapshot, new_snapshot)
       for change in changes:
           print(f"ALERT: {change.description}")
   ```
7. **Save snapshot to `data/pricing-snapshots/{company}.json`**
8. **Generate deep dive report using template:**
   - Read `templates/report/markdown/pricing-deep-dive-template.md`
   - Fill in all sections: Executive Summary, Value Comparison, Plan Breakdown, Pricing History, Alert Log
   - Save to `data/reports/{date}/pricing-deep-dive-{company}-{date}.md`
9. Output summary with value scores and any detected changes

**Key Features:**
- Value Score = (Feature Count / Price) * Market Normalization Factor
- AI API baseline: $1/1M tokens = score 3.0
- SaaS baseline: $10/user/mo = score 3.0
- **ANY pricing change triggers alert** (no threshold)
- Stores $/token data in JSON format for programmatic access

---

## Batch Mode

**Multi-Agent Parallel Implementation** (see `modes/batch.md` for full details)

When `{{mode}}` is `batch`:

1. Read optional tier filter from args (e.g., `batch tier 1` → only Tier 1)
2. Check for `data/batch-queue.md` file with list of companies
3. If file doesn't exist, prompt user to create it
4. **Filter by tier if specified** (e.g., `tier 1` → only ## Tier 1 section)
5. **Create agent team** using TeamCreate
6. **Spawn parallel agents** - one per company (max 5 concurrent)
7. Each agent runs full `analyze` workflow independently
8. Track progress in `data/batch-status.json`
9. Consolidate results from all agents
10. Output batch summary

**Key Feature:** Uses Claude Code multi-agent for ~3x speedup

### Batch Queue Format

Create `data/batch-queue.md`:

```markdown
# Batch Queue

## Tier 1 (Direct Competitors)
- Anthropic
- OpenAI
- Google DeepMind

## Tier 2 (Indirect Competitors)
- Mistral
- Cohere
- Meta AI

## Tier 3 (Emerging)
- Character.AI
- Inflection
```

Or use CSV format in `data/batch-queue.csv`:

```csv
company,tier,priority
Anthropic,1,high
OpenAI,1,high
Mistral,2,medium
```

---

## Report Mode

When `{{mode}}` is `report`:

1. Check for optional `html` flag and filters in args (company, date range)
2. Aggregate all reports in `data/reports/`
3. Generate consolidated report in `data/reports/{date}/consolidated-{date}.md`
4. **If `html` flag is present in args:**
   - Read the consolidated markdown report
   - **Generate HTML with ECharts visualizations:**
     - Score bar chart (ranking by overall score)
     - Radar chart (6 dimensions across all competitors)
     - Pricing heatmap (input/output prices by model)
   - **Pricing change detection:**
     - Compare with `data/snapshots/pricing/{company}.json`
     - Highlight price changes with 🔴 alert badges
     - Show delta (e.g., "-67%", "+20%")
   - Generate HTML report with Tailwind dark theme + ECharts
   - Save to `data/reports/html/index.html`
5. Output path to report (include HTML path if generated)

**ECharts Integration:**
- Use ECharts 5.x via CDN: `https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js`
- Charts should be responsive and dark-themed to match Tailwind dark mode

**HTML Template CSS (include in `<head>`):**
```html
<style>
    section { page-break-inside: avoid; break-inside: avoid; }
    div { page-break-inside: avoid; break-inside: avoid; }
    table { page-break-inside: avoid; break-inside: avoid; }
</style>
```
Every section, inner div, and table should have `page-break-inside: avoid` to prevent content from splitting across PDF pages.

**Chart Layout Guidelines:**
- Bar chart: Grid left margin ~15% to prevent y-axis label cutoff, height 320px
- Radar chart: Legend positioned on right (vertical) to avoid overlap with 7 companies, height 400px
- Heatmap: Model names shortened (e.g., "Gemini 3.1 Flash" → "Gemini 3.1") to prevent label overlap, height 400px
- Use `grid-cols-2` for radar + heatmap side-by-side layout
- Include tooltips showing exact values on hover

---

## Monitor Mode

When `{{mode}}` is `monitor`:

Use `/loop` skill to set up continuous competitive intelligence monitoring:

1. Read optional `interval` from args (e.g., `monitor daily`, `monitor weekly`)
   - Default: weekly
   - Options: `daily`, `weekly`, `monthly`
2. Parse companies from `data/competitors.md`
3. Set up cron job using `/loop`:
   ```
   /loop [interval] /competitive-ops update [company]
   ```
4. For full batch monitoring:
   ```
   /loop [interval] /competitive-ops batch
   ```
5. Store schedule in `data/.monitor-schedule.json`:
   ```json
   {
     "enabled": true,
     "interval": "weekly",
     "last_run": "2026-04-07",
     "next_run": "2026-04-14",
     "companies": ["Anthropic", "OpenAI", "..."]
   }
   ```
6. Output confirmation with schedule details

**Available Intervals:**
- `daily` -- 57 8 * * * (8:57 AM local, off-minute to avoid load spike)
- `weekly` -- 57 8 * * 1 (Monday 8:57 AM local)
- `monthly` -- 57 8 1 * * (1st of month 8:57 AM local)

**Monitoring Scope:**
- Tier 1 competitors: Weekly update recommended
- Tier 2 competitors: Bi-weekly acceptable
- Pricing changes: Monthly review

---

## PDF Mode

When `{{mode}}` is `pdf`:

Export reports to PDF for external sharing:

1. Read optional `report` arg (default: latest consolidated report)
   - `pdf` → export `data/reports/html/index.html`
   - `pdf anthropic` → export `data/reports/html/anthropic-{date}.html`
2. Run PDF export script:
   ```bash
   node scripts/export_pdf.js data/reports/html/index.html
   ```
   The script uses Playwright to:
   - Wait for ECharts to fully render (3 second delay)
   - Verify 3 ECharts instances are present
   - Generate A4 PDF with header/footer
3. Save PDF to `data/reports/pdf/{date}/{report}-{date}.pdf`
4. Output PDF path and file size

**PDF Script Implementation (`scripts/export_pdf.js`):**
```javascript
const { chromium } = require('playwright');
// - Launches headless Chromium
// - Sets viewport to 1200x1600 for proper rendering
// - Waits for networkidle + 3s for ECharts
// - Generates A4 PDF with margins and page numbers
// - Adds footer: "Page X of Y | competitive-ops v2 | {date}"
```

**HTML CSS for PDF Page Breaks:**
Add to `<head>` of HTML reports:
```html
<style>
    section { page-break-inside: avoid; break-inside: avoid; }
    div { page-break-inside: avoid; break-inside: avoid; }
    table { page-break-inside: avoid; break-inside: avoid; }
</style>
```

**PDF Output Locations:**
| Report | PDF Location |
|--------|-------------|
| Consolidated | `data/reports/pdf/{date}/index-{date}.pdf` |
| Company | `data/reports/pdf/{date}/{company}-{date}.pdf` |
| Comparison | `data/reports/pdf/{date}/compare-{A}-vs-{B}-{date}.pdf` |

**Styling for PDF:**
- ECharts rendered via Playwright with 3s wait for JS execution
- CSS page-break properties prevent section splitting across pages
- A4 format with 15mm margins
- Dark-themed with printed background colors

---

## PNG Mode

When `{{mode}}` is `png`:

Export reports to PNG/JPEG image for visual sharing:

1. Read optional `report` arg (default: latest consolidated report)
   - `png` → export `data/reports/html/index.html`
   - `png anthropic` → export specific company report
2. Run image export script:
   ```bash
   node scripts/export_image.js data/reports/html/index.html
   ```
   The script uses Playwright to:
   - Wait for ECharts to fully render (3 second delay)
   - Verify ECharts instances are present
   - Capture viewport screenshot (default 1400x900) or full page
3. Save image to `data/reports/images/{date}/{report}-{date}.png`
4. Output image path, file size, and format

**Image Script Options (`scripts/export_image.js`):**
```bash
node scripts/export_image.js [html-path] [options]
  -o, --output <path>   Output file path
  -f, --full            Capture full page (not just viewport)
  -j, --jpeg            Export as JPEG (default: PNG)
```

**Image Output Locations:**
| Report | Image Location |
|--------|---------------|
| Consolidated | `data/reports/images/{date}/index-{date}.png` |
| Company | `data/reports/images/{date}/{company}-{date}.png` |

**Image Features:**
- High-resolution screenshot with ECharts fully rendered
- Dark background preserved (omitBackground: false)
- PNG default with JPEG quality option
- Viewport or full page capture modes

---

## Track Mode

When `{{mode}}` is `track`:

1. Read `data/competitors.md`
2. Display dashboard:
   - All competitors with scores
   - Last updated dates
   - Alert indicators (stale data, significant changes)
   - Filter by tier, score, status
3. Output formatted table

---

## Shared Context

All modes have access to:

- `cv.md` -- Your company/product definition
- `config/profile.yml` -- Configuration
- `config/sources.yml` -- Trusted data sources
- `modes/_shared.md` -- Scoring system, archetypes, rules
- `modes/_profile.md` -- Your customizations

---

## Scoring System

**Reference values (customizable in `modes/_profile.md` or `config/profile.yml`):**

| Dimension | Default Weight |
|-----------|---------------|
| Product Maturity | 20% |
| Feature Coverage | 20% |
| Pricing | 15% |
| Market Presence | 15% |
| Growth Trajectory | 10% |
| Brand Strength | 10% |

**Confidence Levels (customizable):**
- 🟢 High: 3+ sources agree
- 🟡 Medium: 2 sources agree
- 🔴 Low: Conflicting or insufficient data

---

## Archetypes

**Reference types (customizable in `modes/_profile.md` or `config/profile.yml`):**

Classify competitors into:
- **Direct Competitor** -- Same product, same market
- **Indirect Competitor** -- Different approach, same need
- **Emerging Threat** -- New technology, new model
- **Replacement Threat** -- Alternative solution
- **Adjacent Player** -- Overlapping users
- **Reference Model** -- Industry benchmark

---

## Output Locations

**Standard Structure:** All reports are organized by date in `data/reports/{date}/`, with `latest/` containing symlinks only.

| Output | Location |
|--------|----------|
| Analysis Report | `data/reports/{date}/{company}-{date}.md` |
| Latest Symlink | `data/reports/latest/{company}.md` → `../{date}/{company}-{date}.md` |
| Comparison Report | `data/reports/{date}/compare-{A}-vs-{B}-{date}.md` |
| Pricing Report | `data/reports/{date}/pricing-{company}-{date}.md` |
| Pricing Deep Dive Report | `data/reports/{date}/pricing-deep-dive-{company}-{date}.md` |
| Pricing Snapshot (JSON) | `data/pricing-snapshots/{company}.json` |
| Consolidated Report | `data/reports/{date}/consolidated-{date}.md` |
| HTML Report | `data/reports/html/{company}-{date}.html` |
| PDF Report | `data/reports/pdf/{date}/{company}-{date}.pdf` |
| Image (PNG) | `data/reports/images/{date}/{company}-{date}.png` |
| Snapshot (update diff) | `data/snapshots/{company}/{date}.json` |
| Pricing Snapshot | `data/snapshots/pricing/{company}.json` |
| Monitor Schedule | `data/.monitor-schedule.json` |
| Screenshot (Playwright) | `data/reports/screenshots/{company}-{date}.png` |
| Competitor Tracker | `data/competitors.md` |

**Snapshot Usage:**
- `update` mode compares old vs new report scores (default ≥5% triggers alert, customizable)
- `pricing` mode compares historical pricing changes
- Auto-saved after each analyze/update

**Playwright Usage:**
- Generates competitor website screenshots for `analyze` / `report` mode
- Used when visual evidence is needed
- Optional feature, does not affect core analysis flow

**Note:** Reports are never overwritten — each run creates a new dated file. Use `update` mode for incremental change tracking.

---

## Next Steps

After routing, execute the selected mode by reading:
- `modes/{mode}.md` for mode-specific instructions
- `modes/_shared.md` for system context
- `modes/_profile.md` for user customizations

## Agent Implementation

For **batch mode**, use multi-agent architecture:

```
/competitive-ops batch tier 1
    ↓
TeamCreate: competitive-batch-{timestamp}
    ↓
Agent analyzer-1 → analyze Anthropic (parallel)
Agent analyzer-2 → analyze OpenAI (parallel)
Agent analyzer-3 → analyze Google DeepMind (parallel)
    ↓
Wait for all agents to complete
    ↓
Consolidate results → output batch summary
```

Each agent executes independently using the `analyze` workflow.
