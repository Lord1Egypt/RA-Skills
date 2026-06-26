# /depradar — Quick Start

## Install

```bash
bash scripts/sync.sh
```

This copies the skill to `~/.claude/skills/depradar-skill/`, making `/depradar` available in all Claude Code sessions.

## Run

```bash
/depradar                      # Scan current project
/depradar stripe               # Check one package
/depradar --quick              # Fast mode (60s)
/depradar --diagnose           # Check API key config
/depradar --mock               # Demo mode (no network)
```

## Add API Keys (Optional)

```bash
mkdir -p ~/.config/depradar
cat > ~/.config/depradar/.env << 'EOF'
# github.com/settings/tokens — no scopes needed
GITHUB_TOKEN=ghp_...

# scrapecreators.com — enables Reddit signals
SCRAPECREATORS_API_KEY=sc_...
EOF
```

## Run Tests

```bash
cd scripts && python3 -m pytest ../tests/ -v
```

## File Layout

```
depradar-skill/
├── SKILL.md                    ← Claude reads this to run /depradar
├── CLAUDE.md                   ← This file
├── scripts/
│   ├── depradar.py             ← Main entry point
│   ├── sync.sh                 ← Install script
│   └── lib/
│       ├── dep_parser.py       ← Parse dependency files
│       ├── github_releases.py  ← GitHub Releases API
│       ├── npm_registry.py     ← npm Registry API
│       ├── pypi_registry.py    ← PyPI JSON API
│       ├── crates_registry.py  ← crates.io API
│       ├── maven_registry.py   ← Maven Central API
│       ├── changelog_parser.py ← Extract breaking changes
│       ├── usage_scanner.py    ← Scan codebase for usage
│       ├── impact_analyzer.py  ← Map impact to files
│       ├── github_issues.py    ← GitHub Issues search
│       ├── stackoverflow.py    ← Stack Overflow API
│       ├── reddit_sc.py        ← Reddit via ScrapeCreators
│       ├── hackernews.py       ← HN Algolia + Firebase
│       ├── twitter_x.py        ← X/Twitter via xAI Grok
│       ├── score.py            ← Scoring formulas
│       ├── normalize.py        ← Score normalization
│       ├── dedupe.py           ← Deduplication
│       ├── render.py           ← Output rendering
│       ├── schema.py           ← Data model
│       ├── semver.py           ← Version parsing
│       ├── cache.py            ← File-based caching
│       ├── env.py              ← Config + API key loading
│       ├── dates.py            ← Date utilities
│       ├── http.py             ← HTTP client (stdlib only)
│       └── ui.py               ← Terminal UI
├── tests/                      ← pytest test suite (371 tests)
├── fixtures/                   ← Test fixtures
├── hooks/
│   ├── hooks.json              ← SessionStart hook definition
│   └── scripts/
│       └── check-config.sh     ← Config validator
├── .claude-plugin/
│   ├── plugin.json             ← Plugin manifest
│   └── marketplace.json        ← ClawHub metadata
└── agents/
    └── openai.yaml             ← OpenAI Codex compatibility
```
