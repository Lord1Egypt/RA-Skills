# cross_check

An OpenClaw skill that cross-checks factual claims across multiple sources with confidence ratings.

## What it does

- Optimizes search queries for verification
- Evaluates sources using a 4-tier credibility system (T1–T4)
- Resolves contradictions between sources
- Presents answers with confidence ratings and citations

## Install

```bash
cp -r . ~/.openclaw/skills/cross_check
```

Or clone directly:

```bash
git clone https://github.com/marianachow0321/openclaw-skill-cross-check.git ~/.openclaw/skills/cross_check
```

## Usage

The skill activates automatically when you ask questions that need fact verification. Examples:

- "Is it true that Company X uses Platform Y?"
- "Verify this statistic: ..."
- "Cross-check this claim for me"

## Structure

```
cross_check/
├── SKILL.md                        # Core workflow
├── references/
│   ├── query-optimization.md       # Search query patterns
│   ├── source-tiers.md             # Source credibility tiers
│   └── research-patterns.md        # Multi-query strategies
└── README.md
```

## Security & Privacy

- No API keys required
- No data is stored or sent beyond what OpenClaw's built-in `web_search` and `web_fetch` tools do

## License

MIT
