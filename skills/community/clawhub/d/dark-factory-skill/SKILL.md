# Dark Factory Multi-Agent Startup Platform

Run multiple SaaS startups in parallel using specialized OpenClaw agents, a CEO orchestrator, and ChatDev-powered code generation. Based on Chris Benson's L4.1 Dark Factory architecture.

## What This Skill Installs

A complete multi-agent startup operating system with:
- CEO/orchestrator agent that routes work across product agents
- Per-product agents (pre-configured for VerdictLegal, Surfaced, SayfeAI, CashPing)
- 3-Gate Pipeline enforcement: BUILD -> TEST -> JUDGE
- L6 continuous improvement engine
- ChatDev integration for multi-agent code generation

## Architecture (The Factory Floor Analogy)

Think of this like a real startup factory:
- The CEO agent is the plant manager — decides what gets built and when
- Product agents are specialized assembly lines — each knows its product deeply
- ChatDev is the robotic assembly arm — multi-agent code generation
- The 3-Gate Pipeline is quality control — nothing ships without passing all 3 gates

## Usage

After installing, configure your products in DARK_FACTORY.md:

  1. Run CEO agent for strategic prioritization
  2. CEO routes spec to the right product agent
  3. Product agent runs ChatDev for BUILD gate
  4. Independent TEST gate validates against spec scenarios
  5. JUDGE gate scores 8 dimensions — SHIP if avg >= 4.0

## 3-Gate Pipeline

**Gate 1: BUILD** — Implements from spec. Uses SDD scenarios as acceptance criteria.
**Gate 2: TEST** — Independent QA validates. Real data. Screenshots as evidence. Grades A-F.  
**Gate 3: JUDGE** — Sees spec + test results only (never code). 8 dimensions. SHIP or ITERATE.

## Decision Hierarchy

Strategy > Specifications > Validation > Selling > Building > Debugging

If your agent is debugging instead of strategizing, this skill will push it back up.

## L6 Self-Improvement Engine

Four feedback loops that make the factory smarter every day:
1. Weekly Retrospective (Sundays 9PM)
2. Post-Build Learning (every ITERATE/REJECT logs root cause)
3. Competitive Reprioritization (daily intel updates build queue)
4. Tester → Builder Direct Feedback (closes the knowledge gap)

## Requirements

- OpenClaw with multiple agent support
- Claude API key (Anthropic)
- ChatDev (auto-cloned on setup): github.com/OpenBMB/ChatDev
- Product repositories configured in workspace

## Setup

1. Install this skill: npx clawhub@latest install dark-factory
2. Configure DARK_FACTORY.md with your products
3. Run setup script: bash scripts/setup-dark-factory-v2.sh
4. Launch CEO agent and describe your product portfolio

## License

MIT
