<!-- agents: content-creator, researcher -->
# Team Preset — Content Studio

## Composition

| Agent | Type | Template |
|-------|------|----------|
| Leader | Required | `templates/leader/` |
| Executor | Recommended | `templates/executor/` |
| Content Creator | Specialist | `templates/agents/content-creator.md` |
| Researcher | Specialist | `templates/agents/researcher.md` |
| Reviewer | On-demand | `templates/reviewer/` |

## Routing Matrix (for Leader)

These rows are injected into Leader's AGENTS.md routing table during scaffold:

| Task Type | Route To |
|-----------|----------|
| Copy, visual briefs, content packages, campaigns | Content Creator |
| Market research, competitor analysis, trend research | Researcher |

## Multi-Agent Workflows

- **Content campaign**: Researcher → Content Creator (→ Reviewer if high-stakes)
- **Quick content**: Content Creator (self-contained research + copy)
- **Research report**: Researcher (standalone)

## When To Use

- Content production workflows (social media, marketing, documentation)
- Projects requiring research-backed content
- Teams that produce content across multiple platforms

## Scaffold Command

```bash
bash scripts/scaffold.sh --skill-dir "$(pwd)" --team content-studio
```
