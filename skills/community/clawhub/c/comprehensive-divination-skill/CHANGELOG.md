# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## Unreleased

### ✨ Features
- Four traditional Chinese divination methods in one package:
  - 小六壬 (Xiao Liu Ren) — palm-counting, second-level divination
  - 六爻纳甲 (Liu Yao Na Jia) — six-line coin oracle with full 纳甲装卦 system
  - 梅花易数 (Mei Hua Yi Shu) — Plum Blossom Numerology, time/number/image based
  - 大六壬 (Da Liu Ren) — Grand Liu Ren with twelve heavenly generals
- Intelligent 4-dimensional routing matrix (complexity / importance / time-sensitivity / domain) that auto-recommends the optimal method for any question
- **Beijing time (UTC+8) is the canonical time anchor**, independent of the user's local clock. True solar time correction by longitude is applied on top. Works correctly for users in any timezone.
- Cross-day handling: when TST correction crosses midnight, `tst_datetime` reflects the actual local date
- True Solar Time (TST) correction for any longitude (covers 60+ Chinese cities + 40+ English city names out of the box, manual longitude input — east positive, west negative — for anywhere else)
- **Geocoding with 3-tier fallback** (local dict → local cache → Open-Meteo Geocoding API) for any city name in any language. Network calls are cached to `scripts/_geo_cache.json` and only fire on cache miss (~0.3-0.8s).
- ZhDate-based accurate lunar calendar / solar-term / ganzhi (heavenly stems & earthly branches) calculation
- **Functional pipeline** (4 composable functions):
  - `get_beijing_time()` — always returns current Beijing time
  - `longitude_to_true_solar(bj_dt, longitude)` — Beijing time + longitude → local TST
  - `datetime_to_shichen(dt)` — datetime → 12 Earthly Branches shichen
  - `get_full_pipeline()` — one-shot pipeline returning the full divination context
- 15 reference markdown files covering core theory (bagua, tiangan-dizhi, yinyang-wuxing, liuqin) plus per-method methodologies
- 5 independently callable Python scripts with `--json` output for LLM consumption
- Bilingual triggers (Chinese keywords + English equivalents)
- Comprehensive pitfalls documentation (`references/comprehensive-divination-skill-pitfalls.md`)

### 📚 Documentation
- `SKILL.md` — main skill document with architecture overview, routing logic, method-specific workflows
- `README.md` — bilingual user-facing documentation with installation, quick start, international users section
- `LICENSE` — MIT (with cultural-use disclaimer)
- `CHANGELOG.md` — this file

### 🔧 Technical notes
- Single external dependency: `zhdate==0.1` (pinned). PyPI Windows max version; 1.0 only ships macOS ARM wheel so we explicitly pin to 0.1 for cross-platform install success.
- Pure Python stdlib only for the geocoding (urllib); no `requests` needed.
- `get_current_lunar_info()` kept as a backward-compatible wrapper around the new functional pipeline

### ✅ Verified
- End-to-end tested on Windows 10 with Python 3.11 (Hermes venv) and Python 3.13 (system)
- All four methods return deterministic results from the same frozen timestamp
- Tested with 5 timezone scenarios: 成都 / 香港 / 纽约 / 伦敦 / 悉尼
- Geocoding tested with 3-tier fallback: local dict hit, cache hit, network fetch
