# alphalens-api

Agent skill that turns the [AlphaLens](https://alphalens.ai) API into installable workflows: competitive landscape maps, investor networks, peer benchmarks, and white space analysis. Each workflow produces a standalone HTML report you can open in any browser, embed as a Claude.ai artifact, or export to PDF.

> Requires an active [AlphaLens](https://alphalens.ai) subscription with API access. Contact **contact@alphalens.ai** for pricing.

## What this produces

Self-contained HTML pages — favicons embedded as base64, no proxy or CORS workaround required:

- **Market maps** — competitive landscape grids with logos and named clusters
- **Product-centric maps** — tabbed maps with one cluster grid per product line
- **Investor networks** — D3 force-directed graph of who funds whom across the landscape
- **Peer benchmarks** — headcount growth, funding scale, capital efficiency, qualitative positioning
- **White space analysis** — 4-phase report on saturation, adjacencies, feature survival, and ICP expansion

## Install

### Cross-tool (recommended) — `npx skills add`

Vercel Labs' `skills` CLI auto-detects which agents you have installed (Claude Code, Cursor, Codex, etc.) and copies the skill into the right place for each:

```bash
npx skills add alphalens-intelligence/alphalens-skills
```

Then set your API key in the shell:

```bash
export ALPHALENS_API_KEY=your_key_here
```

### Claude Code (direct git clone)

```bash
# Personal install (available in any project)
git clone https://github.com/alphalens-intelligence/alphalens-skills \
  ~/.claude/skills/alphalens-api

# Or per-project install
git clone https://github.com/alphalens-intelligence/alphalens-skills \
  .claude/skills/alphalens-api
```

### OpenClaw

```bash
openclaw skills install WalidMustapha/alphalens-api
```

Set `ALPHALENS_API_KEY` in your OpenClaw secret store; the runtime injects it into the execution environment automatically.

## How to use

Describe what you want in plain language:

- `Build a market map around ramp.com using AlphaLens`
- `Run a bottom-up deep dive on legora.com`
- `Show me the investor network for the companies around Mercury`
- `Build a peer benchmark comparing Brex to its 5 closest competitors`
- `Find the white space around zoominfo.com`

See [`references/EXAMPLES.md`](references/EXAMPLES.md) for more prompts and [`references/REFERENCE.md`](references/REFERENCE.md) for the full API endpoint catalog the skill draws on.

## Authentication contract

The skill expects `ALPHALENS_API_KEY` to be available as an environment variable inside whatever container the agent runs in.

The workflows reference a `$KEY` shell variable for brevity. **The agent must alias `ALPHALENS_API_KEY` as `KEY` in the first bash command of any session that uses this skill**, before any API calls:

```bash
KEY="$ALPHALENS_API_KEY"
API="https://api-production.alphalens.ai"
```

`SKILL.md` instructs the agent to do this. If calls fail with 401, the most common cause is the agent skipping the aliasing step — verify with `echo "$KEY" | head -c 4` (should print 4 characters, not be empty).

## Repository layout

```text
alphalens-skills/
├── README.md              # This file
├── LICENSE                # MIT-0
├── CHANGELOG.md
├── SKILL.md               # Agent-readable skill definition
├── skill.yaml             # Runtime metadata (env vars, license, version)
├── workflows/
│   ├── market-map-org.md          # Simple org-level competitive landscape
│   ├── market-map-product.md      # Tabbed, one map per product line
│   ├── investor-network.md        # D3 force-directed graph
│   ├── peer-benchmark.md          # Headcount + funding comparison
│   ├── suite-bottom-up.md         # Orchestrator for the 3-deliverable suite
│   ├── white-space.md             # White space report (4 phases)
│   └── white-space-phase{1,2,3,4}.md
└── references/
    ├── REFERENCE.md       # Endpoint catalog + filter reference
    └── EXAMPLES.md        # Example prompts
```

## Security and trust

Agent skills run code and make network calls inside the runtime's container, so auditing before install is reasonable. This skill:

- Calls only the AlphaLens production API (`api-production.alphalens.ai`) and Google's public favicon service (`t0.gstatic.com`) for company logos
- Never logs, transmits, or persists your API key beyond the curl calls in the workflows themselves
- Has no third-party runtime dependencies — pure bash + browser-rendered HTML output
- Output HTML is self-contained (no external script tags or remote resources at view time beyond optional CDN-loaded Chart.js / D3 for interactive views)

See [`references/REFERENCE.md`](references/REFERENCE.md) for the complete list of endpoints the skill calls.

## Versioning

Releases are tagged on this repo. The skill version is also tracked in `skill.yaml` and the SKILL.md frontmatter for runtimes that read it. We follow semver: patch for fixes, minor for new workflows or non-breaking changes, major for breaking changes to the skill contract (including install path or required environment).

See [`CHANGELOG.md`](CHANGELOG.md) for the version history.

## License

[MIT-0](LICENSE) (MIT No Attribution). Use it freely, no attribution required.

## Contact

- Product and pricing: [alphalens.ai](https://alphalens.ai) · contact@alphalens.ai
- Bug reports and feature requests: [GitHub Issues](https://github.com/alphalens-intelligence/alphalens-skills/issues)
