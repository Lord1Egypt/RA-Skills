# AI Session Analysis

A [Claude Code skill](https://agentskills.io/specification) that analyzes local AI coding assistant session data — Claude Code, Codex (OpenAI), and Kimi Code.

Three Python scripts (stdlib only, zero dependencies):

| Script | Output |
|--------|--------|
| `scripts/analyze.py` | Terminal overview: sessions, tool counts, projects, daily timeline |
| `scripts/tool_analysis.py` | Deep dive: shell categories, file ops, token usage, errors |
| `scripts/generate_report.py [out.html]` | Self-contained HTML report with Chart.js visualizations |

## Preview

![HTML Report Preview](assets/report-preview.png)

See [SKILL.md](SKILL.md) for the full skill reference — data sources, interpretation guidance, and common issues.
