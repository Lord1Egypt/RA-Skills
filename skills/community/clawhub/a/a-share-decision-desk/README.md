# uwillberich

A ClawHub/OpenClaw-ready skill for next-session A-share discretionary planning.

It is designed for one job: turn today’s tape and overnight developments into a concrete game plan for tomorrow’s open.

Author: 超超
Contact: `grdomai43881@gmail.com`

GitHub is the main source of truth for installation and updates:

```text
https://github.com/huangrichao2020/uwillberich
```

## Good Use Cases

- "What is the most likely A-share path tomorrow?"
- "Which sectors are most likely to repair first after today’s selloff?"
- "Give me a `09:00 / 09:25 / 09:30-10:00` opening checklist."
- "Build a watchlist-driven pre-open note for A-shares."
- "Tell me whether this is real repair or just defensive concentration."
- "Use the cross-cycle core stock pool to narrow tomorrow's key observation list."
- "In a war-oil shock regime, tell me which A-share groups benefit and which ones get hurt."
- "Continuously watch public news and map major events into A-share watchlists."
- "Run a preset `Step 1 / Step 2 / Step 3` desk workflow and save all artifacts."
- "Benchmark which public and MX data sources are healthy before the open."

## Workflow Map

1. `Step 1: overnight and policy`
   - `scripts/news_iterator.py`
   - `scripts/mx_toolkit.py preset --name preopen_policy`
   - `scripts/mx_toolkit.py preset --name preopen_global_risk`
2. `Step 2: board resonance`
   - `scripts/fetch_market_snapshot.py`
   - `scripts/morning_brief.py`
   - `scripts/capital_flow.py`
   - `scripts/market_sentiment.py`
   - `scripts/mx_toolkit.py preset --name board_optical_module`
   - `scripts/mx_toolkit.py preset --name board_compute_power`
3. `Step 3: single-name validation`
   - `scripts/fetch_quotes.py`
   - `scripts/mx_toolkit.py preset --name validate_inspur`
   - `scripts/mx_toolkit.py preset --name validate_luxshare`
4. `Step 4: chain expansion`
   - `scripts/industry_chain.py`
   - `scripts/news_iterator.py`
   - `scripts/opening_window_checklist.py`
5. `Source benchmark`
   - `scripts/benchmark_sources.py`

## What This Skill Contains

- `SKILL.md`: main instructions and trigger description
- `references/methodology.md`: decision framework
- `references/data-sources.md`: primary and market data sources
- `references/persona-prompt.md`: decision-maker persona prompt
- `references/trading-mode-prompt.md`: time-based pre-open trading mode prompt
- `references/cross-cycle-watchlist.md`: how to use the cross-cycle core stock pool
- `references/event-regime-watchlists.md`: war-shock overlay watchlists
- `references/message-iterator.md`: persistent message iterator for high-attention news
- `assets/mx_presets.json`: preset `Step 1 / Step 2 / Step 3` MX workflows
- `scripts/fetch_market_snapshot.py`: index and sector breadth snapshot
- `scripts/fetch_quotes.py`: Tencent quote watchlist snapshot
- `scripts/morning_brief.py`: one-command markdown morning brief
- `scripts/capital_flow.py`: main-force capital-flow overlay for the market and watchlists
- `scripts/market_sentiment.py`: breadth + board-dispersion + capital-flow sentiment classifier
- `scripts/opening_window_checklist.py`: first-30-minute decision sheet
- `scripts/industry_chain.py`: event-to-industry-chain expansion for fresh stock pools
- `scripts/news_iterator.py`: RSS polling, classification, SQLite state, markdown/jsonl outputs, and automatic event stock pools
- `scripts/runtime_config.py`: local credential helper for the required `EM_API_KEY`
- `scripts/mx_api.py`: Meixiang / Eastmoney API wrapper for live finance queries
- `scripts/mx_toolkit.py`: CLI wrapper for real news search, stock screen, structured data queries, and desk presets
- `scripts/benchmark_sources.py`: source latency / availability benchmark
- `scripts/install_news_iterator_launchd.py`: macOS launchd installer for scheduled polling
- `scripts/smoke_test.py`: local smoke test for the bundled scripts

## Agent Install

Install this folder into:

- `~/.codex/skills/uwillberich`
- `~/.openclaw/skills/uwillberich`

Example:

```bash
git clone https://github.com/huangrichao2020/uwillberich.git
mkdir -p ~/.codex/skills
cp -R uwillberich/skill/uwillberich ~/.codex/skills/uwillberich
```

One-line install for Codex:

```bash
git clone https://github.com/huangrichao2020/uwillberich.git && cd uwillberich && ./install_skill.sh
```

One-line install for OpenClaw:

```bash
git clone https://github.com/huangrichao2020/uwillberich.git && cd uwillberich && ./install_skill.sh openclaw
```

## Keys And Credentials

This skill hard-requires `EM_API_KEY`.

- Apply here:
  `https://ai.eastmoney.com/mxClaw`
- After opening the link, click download and you will see the key.
- Official site:
  `https://ai.eastmoney.com/nlink/`
- Store it locally in `~/.uwillberich/runtime.env`.
- Check or set it with:

```bash
python3 scripts/runtime_config.py status
printf '%s' 'your_em_api_key' | python3 scripts/runtime_config.py set-em-key --stdin
```

Without `EM_API_KEY`, the scripts will exit and print the application URL plus setup command.

- GitHub read access: only if the repo is private and an agent must clone it
- GitHub write access: only if an agent should push changes back
- Model-provider API keys: may be required by the host agent environment, but not by this skill itself

## Local Smoke Test

```bash
python3 scripts/smoke_test.py
python3 scripts/runtime_config.py status
python3 scripts/mx_toolkit.py list-presets
python3 scripts/mx_toolkit.py preset --name preopen_repair_chain
python3 scripts/mx_toolkit.py preset --name flow_main_force
python3 scripts/mx_toolkit.py news-search --query '立讯精密 最新资讯'
python3 scripts/mx_toolkit.py stock-screen --keyword 'A股 光模块概念股' --page-size 10 --csv-out /tmp/cpo.csv --desc-out /tmp/cpo-columns.md
python3 scripts/mx_toolkit.py query --tool-query '浪潮信息 最新价 市值'
python3 scripts/capital_flow.py --groups tech_repair defensive_gauge
python3 scripts/market_sentiment.py
python3 scripts/industry_chain.py --groups tech_repair defensive_gauge
python3 scripts/benchmark_sources.py
python3 scripts/fetch_market_snapshot.py --format markdown
python3 scripts/fetch_quotes.py sz300502 sh688981 sh600938
python3 scripts/morning_brief.py --groups core10 tech_repair
python3 scripts/morning_brief.py --groups cross_cycle_anchor12
python3 scripts/morning_brief.py --groups cross_cycle_ai_hardware cross_cycle_semis cross_cycle_software_platforms cross_cycle_defense_industrial
python3 scripts/morning_brief.py --groups war_shock_core12
python3 scripts/morning_brief.py --groups war_benefit_oil_coal war_headwind_compute_power
python3 scripts/opening_window_checklist.py --groups tech_repair defensive_gauge policy_beta
python3 scripts/news_iterator.py poll
python3 scripts/news_iterator.py report --hours 12
python3 scripts/install_news_iterator_launchd.py install --interval-seconds 300
python3 scripts/morning_brief.py
python3 scripts/opening_window_checklist.py
```

## Optional ClawHub Publish

From this folder:

```bash
clawhub login
clawhub publish /absolute/path/to/uwillberich --slug uwillberich --name "uwillberich" --version 0.1.7 --tags latest,finance,a-share,china,markets
```

## Notes

- ClawHub publishes a skill folder with `SKILL.md` plus supporting text files.
- This skill uses only text-based resources and Python standard library scripts.
- `EM_API_KEY` is mandatory for this skill.
- The runtime helper automatically maps `EM_API_KEY` to the `MX_APIKEY` convention used by the public MX skills.
- Preset and benchmark outputs default to `~/.uwillberich/data/`.
- If `clawhub publish .` misreads the folder, use an absolute path or pass `--workdir` explicitly.
- The opening-window script is intended for `09:00-10:00` use, especially the first 30 minutes after the A-share cash open.
- For the larger quality pool, use `cross_cycle_anchor12` daily and reserve `cross_cycle_core` for weekly or phase-rotation review.
- For geopolitical shocks, treat `war_benefit_oil_coal` and `war_headwind_compute_power` as temporary regime overlays, not permanent core watchlists.
- If you only want one wartime overlay, start with `war_shock_core12`.
- For continuous event intake, run `news_iterator.py` as a local service and treat the alert stream as an overlay, not a replacement for tape and breadth.
- The morning brief and opening checklist can automatically append event-driven stock pools when `event_watchlists.json` exists in the default state directory.
