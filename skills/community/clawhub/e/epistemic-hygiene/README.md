# Epistemic Hygiene

> Activate when user asks how to discuss product/strategy questions, requests analysis of unfamiliar markets, or when sparse documentation might tempt extrapolation. Provides 8 principles for grounded epistemic discussion with AI.

A discipline for AI-collaborative thinking. Catches the most common ways AI assistants drift off-track during open-ended product, strategy, and research discussions.

## Install

### Claude Code

```bash
clawhub install epistemic-hygiene
```

Or manually clone:

```bash
git clone https://github.com/<org>/epistemic-hygiene.git ~/.claude/skills/epistemic-hygiene
```

### OpenClaw / Hermes / Cursor

Standard agentskills.io-compatible install per platform.

## Quickstart

Once installed, the skill activates automatically when you discuss strategy / market / product questions or share sparse documentation. No explicit invocation needed.

Example interaction:

> **You**: Anyone working on benchmarks for agent interruption cost?
>
> **AI** (with skill): *[searches first]* "Found three: HiL-Bench (arxiv 2604.09408), ProAgentBench, and the Levels-of-Autonomy paper from late 2025. They overlap with what you're describing but emphasize different axes — want me to summarize how each frames the cost?"

vs without skill:

> **AI** (without skill): "No, this is largely unaddressed in current literature. Most agent benchmarks focus on task completion."

The skill enforces verify-before-claim discipline among other failure-mode counters.

## What this skill does

This skill provides 8 principles, organized in three clusters:

**Group A — Research-grounded** (Principles 1-3): treat external claims as needing verification before assertion.

**Group B — Stance and framing** (Principles 4-6): give real judgments without smuggling in unverified premises.

**Group C — Dialogue shape** (Principles 7-8): respect the user's reasoning rhythm and abstraction layers.

Full principle list and rationale: see [SKILL.md](SKILL.md) and [references/principles.md](references/principles.md).

## When NOT to use

- For straightforward technical questions ("how do I write a list comprehension"). Use a normal coding workflow instead.
- For creative/exploratory writing where stance and verification aren't load-bearing.
- When the user has explicitly asked you *not* to verify claims (e.g., "just speculate"). The skill should respect that override but flag epistemic status.

## Files

```
epistemic-hygiene/
├── SKILL.md             # frontmatter + main flow
├── README.md            # this file
├── references/
│   ├── principles.md         # full detail of 8 principles
│   ├── triggers.md           # input patterns → principle activation
│   └── anti-patterns-catalog.md  # 11 sanitized AP cases
└── examples/
    ├── research-before-assertion.md
    ├── sparse-evidence.md
    └── market-claim-verification.md
```

## Background

This skill was distilled from cross-session feedback patterns observed during AI-collaborative product / strategy / research work over many months. Each principle names a specific, repeatable failure mode and gives the discipline for catching it.

The principles are not "general good behavior advice" — they're specific counter-moves to specific drift patterns that show up reliably in AI-collaborative thinking. If a principle feels obvious in the abstract, the anti-pattern catalog will likely show you cases where it wasn't applied in practice.

## Versioning

Following [SemVer](https://semver.org/).

- `0.1.0` initial release with 8 principles, 3 examples, trigger catalog, anti-pattern library

## License

MIT

## Contributing

Issues and PRs welcome. Particularly interested in:
- Additional anti-pattern submissions (sanitized examples)
- Trigger pattern refinements
- Cross-domain examples (the existing examples skew toward AI/product strategy — examples from other domains help generalize the skill)
