# Research Agent Skill

Deep research and analysis on any topic. 5 modes: Quick lookup, Deep Dive, Compare, Landscape, Evaluate. Structured reports with source evaluation.

Works with any [Agent Skills](https://agentskills.io) compatible tool: Claude Code, OpenAI Codex, Trae, Cursor, Gemini CLI, and more.

## Problem

You ask your AI "what is X?" and get a generic, unsourced paragraph. You ask "should we use X or Y?" and get "it depends."

**This skill gives you structured, sourced, opinionated research.**

## Modes

| Mode | You Say | Output |
|------|---------|--------|
| **Quick** | "What is gstack?" | 1-paragraph summary + 3 key facts |
| **Deep Dive** | "Research AI coding agents" | Full report in `RESEARCH.md` |
| **Compare** | "Claude Code vs Cursor vs Codex" | Scored comparison matrix + recommendation |
| **Landscape** | "What's out there for PM tools?" | Categorized market map |
| **Evaluate** | "Should we adopt X?" | Decision framework with scoring |

## Install

```bash
# Via agentskills-cli
npm install -g @jahonn/agentskills-cli
agentskills install ./research-agent-skill -t all

# Via ClawHub
clawhub install research-agent
```

## Example

**Input:** "Research the AI coding agent landscape and compare the top 5"

**Output:**
1. Web search across official docs, Reddit, HN, GitHub
2. Source evaluation (credibility, recency, bias)
3. Categorized landscape map (direct, adjacent, emerging)
4. Comparison matrix scored across 5 dimensions
5. Recommendation: "For solo devs → X, for teams → Y"
6. All findings sourced with URLs

## Research Quality

- Source hierarchy (official > community > opinion)
- Bias detection (sponsor, recency, popularity)
- Cross-reference across multiple sources
- Confidence scoring per finding
- "Gaps & caveats" section for what we couldn't verify

## Related

- [PM Agent Skill](https://github.com/jahonn/pm-agent-skill) — uses research as Phase 1
- [Dev Workflow Skill](https://github.com/jahonn/dev-workflow-skill) — uses research in Think phase
- [Agent Skills Spec](https://agentskills.io/specification)

## License

MIT
