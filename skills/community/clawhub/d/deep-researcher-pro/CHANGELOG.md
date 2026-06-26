# Changelog

All notable changes to deep-researcher will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2026-04-28

### Changed
- Add Chinese description for better discoverability in Chinese-language skill search

## [1.0.0] - 2026-04-28

### Added
- Initial release of deep-researcher

**Core report structure**
- Top 5 Consensus with evidence strength tags (HIGH / MEDIUM / LOW)
- Top 5 Divergences with both sides' arguments side by side
- Key Numbers with mandatory source citations; forecasts marked `[ESTIMATED]`
- Failed Paths with failure reasons and recurrence conditions
- Core Tension — the irreducible contradiction in one sentence
- Decision Readiness with confidence index (0–10) and next concrete action

**Optional sections (auto-included when relevant)**
- Landscape — competitive/ecosystem structure, key players, recent moves
- Implications — stakeholder-specific impact analysis
- Scenarios — base / upside / downside scenario analysis

**Research engine**
- 5-angle deep search protocol (direct, critical, practitioner, forward-looking, cross-domain)
- Local-language research: auto-detects domain region and searches in official local language
- Fallback language inference (Steps A–D) for regions not in the explicit mapping table
- Multi-language and supranational region handling (EU, Schengen, multilingual countries)
- Multi-country region language allocation (e.g. Southeast Asia → per-country language assignment)

**Semantic intent routing**
- Automatic mode detection from natural language: brief, compare, brief-multi, compare-multi, update, file-only
- No flags or explicit commands required
- Per-subject independent region and language detection in multi-subject mode

**Evidence quality**
- Evidence scoring (HIGH / MEDIUM / LOW) with mandatory source citations
- Full-text fetch before inference (anti-hallucination)
- Vendor self-reported data auto-downgraded to LOW
- Forecast/estimate values marked `[ESTIMATED]`
- Full-text fetch failure handling: evidence downgrade + annotation

**Output**
- Section title localization: all structural labels translated for zh / ja / es / fr / de output
- Overwrite protection: prompts before overwriting existing files
- RESEARCH_LOG with second-precision timestamps for reproducibility

**Environment**
- Startup check: detects missing web search tool and guides user to configure a provider
- Supports: Serper, Tavily, Brave Search, Gemini, Kimi/Moonshot, and any tool named `*search*`
