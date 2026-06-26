# Emergence SEO GEO Skill

A professional Generative Engine Optimization (GEO) and AI-native search engine optimization (AEO) website auditor. Developed by **Emergence Science**, this skill evaluates target domains for visibility, crawlability, and semantic authority across conversational AI platforms (ChatGPT, Perplexity, Gemini, Claude, Copilot, Google AI Overviews).

## Overview

**Emergence SEO GEO** acts as an autonomous auditor to evaluate whether your brand, documentation, or product is ready to be cited and surfaced by LLM-powered search engines. It uses a differentiated 100-point scorecard tailored to the type of web application:
- **Agent-First**: Optimized for machine traversal (checking JSON-LD, `/llms.txt`, `/skill.md` at root, and developer registries).
- **Human-First**: Optimized for traditional and search-based user interactions (focusing on BLUF formats, structured comparisons, EEAT, and sitemaps).

## Key Features

- **Differentiated Scoring Scorecard**: Weighting heuristics mapped dynamically to either agent networks or human audiences.
- **E2E Indexation Checks**: Performs live verification queries on Brave Search, Tavily Search, Google, and Bing to detect actual index presence.
- **Actionable Reporting**: Generates a standard report detailing current state, citation gap analysis, and a 30-60-90 day optimization roadmap.

## Usage

Run the automated auditor script on any domain:
```bash
# Audit an agent network app or dev protocol (Agent-first)
python3 scripts/geo_audit.py emergence.science --type agent --prompt "openclaw bounty market"

# Audit a B2B SaaS or E-commerce site (Human-first)
python3 scripts/geo_audit.py soldy.ai --type human --prompt "AI video generator"
```

To run a live E2E search engine indexation query (requires local `bx` and `tvly` CLIs):
```bash
python3 scripts/geo_audit.py emergence.science --type agent --prompt "openclaw bounty market" --e2e
```

## Report Examples & Demos

- **Live Interactive Tool & Report Demo**: [Emergence Science SEO-GEO Audit Tool](https://emergence.science/en/tools/seo-geo)
- **Bundled Audit Report Reference**: An example of a generated English audit report is bundled with this skill at [examples/emergence_science_analysis_en.md](file:///Users/julian/operators/emergence_oracle/skills/emergence-seo-geo/examples/emergence_science_analysis_en.md) for direct reference and templates.

---
© 2026 Emergence Science. Built for the future of autonomous agent and human discovery.
