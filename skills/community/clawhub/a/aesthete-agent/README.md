<p align="center">
<b>English</b> | <a href="README.zh-CN.md">简体中文</a> | <a href="https://docsor1212.github.io/aesthete-agent/">Online demo</a>
</p>

# aesthete-agent

**Mechanically validated frontend aesthetics for AI agents.** An agent skill (and MCP server) that plans, validates, and exports color systems — so your agent stops shipping purple-gradient AI slop and starts shipping palettes that pass WCAG, survive color-blindness, and read as designed.

```bash
npx skills add docsor1212/aesthete-agent   # 30 seconds; also: skillhub / clawhub / MCP uvx — see Install
```

Other tools give your agent taste advice. This one gives it **gates**: nothing ships until it passes four mechanical checks (WCAG contrast, three color-blindness simulations, AI-slop detection, scorecard) — backed by a 119-palette evidence library, five full-page layout recipes, and a render-verified review loop.

[![install](https://img.shields.io/badge/install-npx%20skills%20add%20docsor1212%2Faesthete--agent-blue)](https://github.com/docsor1212/aesthete-agent)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![palette library](https://img.shields.io/badge/palette%20library-119%20curated-orange)](#the-evidence-library)
[![tests](https://img.shields.io/badge/tests-125%20passing-brightgreen)](tests/)

## Why

LLMs choose colors badly for measurable reasons: they treat hex codes as text, they regress to the median of their training data (the frontend-tutorial median is purple/indigo), and they cannot see the colors they emit. `aesthete-agent` fixes this the engineering way — **outsource taste to process**:

- an **evidence library** of 119 curated palettes filtered by objective quality gates (flat lightness → rejected; no readable text pair → rejected; color-blind collisions / slop signatures → flagged),
- **mechanical gates** on every decision: a 5-dimension scorecard, exact WCAG 2.2 boundaries (APCA optional), three color-blindness simulations, AI-slop signature detection, a gradient ban (any gradient = P0), and an HTML delivery linter,
- a **six-step method** (manifesto → register check → source → roles → validate → five-lens review) that turns "make it pretty" into a reproducible pipeline,
- a **preference profile** (`profile.json`) that learns from every accept/reject verdict and mechanically down-ranks what the user rejects.

## What it renders

Every image below is a real deliverable produced by the engine — roles derived in OKLCH, contrast gated, color-blind simulated, slop checked, then rendered into a full scene. No hand-picked colors. Live versions: [visual showcase](https://docsor1212.github.io/aesthete-agent/demo/showcase.html) (30 scenes across curated palettes).

<table>
<tr>
<td width="50%"><img src="docs/img/showcase-mobile.png" alt="Mobile wallet scene"><br><sub><b>Mobile app</b> — Bees &amp; Honey · text/bg 5.6:1 AA</sub></td>
<td width="50%"><img src="docs/img/showcase-landing.png" alt="SaaS landing scene"><br><sub><b>SaaS landing</b> — same palette, browser chrome, 3:1 accents</sub></td>
</tr>
<tr>
<td width="50%"><img src="docs/img/showcase-dashboard.png" alt="Analytics dashboard scene"><br><sub><b>Dashboard</b> — KPI cards, chart bars, status pills</sub></td>
<td width="50%"><img src="docs/img/showcase-ecom.png" alt="E-commerce product card scene"><br><sub><b>E-commerce</b> — Deep Space Blue · 60-30-10 enforced</sub></td>
</tr>
<tr>
<td width="50%"><img src="docs/img/showcase-editorial.png" alt="Magazine editorial scene"><br><sub><b>Editorial</b> — Lavender · print-grade restraint</sub></td>
<td width="50%"><img src="docs/img/showcase-hero.png" alt="Visual showcase page"><br><sub><b>The showcase itself</b> — 30 scenes, one engine</sub></td>
</tr>
</table>

## Install

**Agent skill** — one line in any skills-compatible agent (Claude Code, ZCode, Codex, Cursor, Gemini CLI):

```bash
npx skills add docsor1212/aesthete-agent
```

**SkillHub** (中文站, fastest in China — primary release channel):

```bash
skillhub install aesthete-agent --dir <your-skills-dir>   # e.g. ~/.claude/skills
```

or open [skillhub.cn/skills/aesthete-agent](https://skillhub.cn/skills/aesthete-agent) and click 安装到本地 Agent.

**DeepSeek Harness native plugin** (DSH desktop / web / TUI) — 11 native tools over the bundled engine:

```bash
dsh plugin --profile web add github:docsor1212/dsh-aesthete-agent
```

**ClawHub** (international registry):

**ClawHub** (international registry):

```bash
npx clawhub install aesthete-agent
```

**MCP server** (Claude Desktop, Cursor, any MCP client) — the engine as 21 callable tools:

```bash
uvx aesthete-agent-mcp            # from PyPI, zero keys
# or: npx -y @smithery/cli install docsor1212/aesthete-agent-mcp --client claude
```

Pure Python stdlib in the core engine (offline, zero keys, zero telemetry); Pillow optional for image extraction; FastMCP optional for the MCP server.

## 30-second agent quickstart

```bash
S="scripts/palette_forge.py"   # inside the installed skill directory
python "$S" match --brief "pediatric clinical teaching page" --limit 6   # rank the evidence library by register
python "$S" score --palette 264653,2A9D8F,E9C46A,F4A261,E76F51           # 5-dim scorecard /20
python "$S" matrix --palette ... --method apca --recommend               # full contrast matrix (APCA = WCAG 3 draft)
python "$S" semantic --count 8 --base 2A9D8F                             # color-blind-safe categorical colors
python "$S" visualize --palette ... --variants 3                         # 10 real UI scenes + variants
python "$S" report --palette ...                                         # all gates → one PASS/FAIL verdict
python "$S" theme "Golden Window Suya" --format css                      # named theme pack → CSS tokens
python "$S" export --palette ... --format w3c                            # W3C Design Tokens JSON
python "$S" export --palette ... --format prompt                         # image-generation prompt block
python "$S" doctor                                                       # environment health check
```

Full method (manifesto → register → source → roles → validate → five-lens review) lives in [SKILL.md](SKILL.md). References carry a 30-second routing table per task.

## What's inside

| Area | Highlights |
|---|---|
| Engine (38 subcommands) | match/search/harmony/ramp/mutate/roles/score/contrast/blind/matrix/semantic/slop/themes/theme/export(w3c·context·css·tailwind·prompt)/card/showcase/visualize/report/critique/doctor/selftest/house/extract/directions/scene/scaffold/check-image/evidence/tokens/audit/chartpal/typescale/qc/narrate/exemplar/patch/loop |
| Evidence library | 119 curated palettes with like tiers, computed style tags, gate flags |
| Scene visualizer | 10 real front-end scene types × any palette, light and dark, `--variants` for A/B, `--svg` slot-list recoloring |
| Theme packs | 8 named packs (colors + fonts + voice + use-when), all with provenance |
| Quality gates | exit-code enforced: scorecard, contrast, blind collisions, slop, HTML lint (**gradient ban: any gradient = P0**), `report` one-verdict aggregator |
| Learning | `profile.json` preferences consumed by match/score/lint; verdict write-back is an iron rule |
| Tests | 39 automated tests incl. WCAG boundary values (#767676=4.54 pass / #777777=4.48 fail), APCA, W3C export |

## The evidence library

Nobody can know "beautiful" a priori — so the library is built from three filters, each doing only what it can: **crowd signal** (community-endorsed charts, like tiers, cross-page recurrence), **objective gates** (reject only objectively broken architecture: flat lightness, no readable pair; flag CB collisions and slop), and **in-context review** (the final verdict happens in real layouts, with the user). Every rejection is recorded with a measured cause.

## MCP server

`mcp/` wraps the engine as MCP tools (JSON-RPC over stdio). Zero keys, zero telemetry; ships as a self-contained wheel — `server_data/` carries the engine, so `uvx aesthete-agent-mcp` works standalone. A pure-stdlib stdio fallback (`--stdio`) runs even without FastMCP.

| Tool | Wraps |
|---|---|
| `palette_match` | evidence-library ranking by brief |
| `palette_harmony` | OKLCH harmony generation |
| `palette_score` / `palette_report` | 5-dim scorecard / all-gates PASS-FAIL verdict |
| `palette_contrast` / `palette_matrix` | pair check / full pair matrix (WCAG + APCA) |
| `palette_blind` / `palette_semantic` | CB simulation / CB-safe categorical colors |
| `palette_slop` | AI-slop signature detection |
| `palette_visualize` | 10-scene renderings + variants |
| `palette_themes` / `palette_theme` | named theme packs |
| `palette_export` | css / tailwind / w3c / context / prompt |

## Platform availability

| Platform | Handle | Link |
|---|---|---|
| GitHub (source of truth) | [docsor1212/aesthete-agent](https://github.com/docsor1212/aesthete-agent) | install above |
| SkillHub (中文站) | [aesthete-agent](https://skillhub.cn/skills/aesthete-agent) | `skillhub install aesthete-agent` |
| ClawHub | [aesthete-agent](https://clawhub.ai/skills/aesthete-agent) | `npx clawhub install aesthete-agent` |
| PyPI (MCP) | [aesthete-agent-mcp](https://pypi.org/project/aesthete-agent-mcp/) | `uvx aesthete-agent-mcp` |
| Smithery (MCP) | [docsor1212/aesthete-agent-mcp](https://smithery.ai/server/docsor1212/aesthete-agent-mcp) | `npx -y @smithery/cli install ...` |
| Online demo | [GitHub Pages](https://docsor1212.github.io/aesthete-agent/) | showcase + live visualizers |

## License

MIT
