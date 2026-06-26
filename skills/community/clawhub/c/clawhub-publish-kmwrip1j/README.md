# MBTI Skill

[简体中文](docs/zh-CN/README.md) | [English](README.md)

Infer your MBTI from your conversation history with agents and related context, greatly reducing the time spent answering questions. Currently supports [OpenClaw](https://openclaw.ai/) skills.

Data safety: this skill analyzes your MBTI locally inside your own [OpenClaw](https://openclaw.ai/). No data is uploaded anywhere else.

## Quick Start

### For People

```bash
# Install
openclaw skills install mbti-analyzer

# Run in OpenClaw
mbti-report

# You can also trigger it with `MBTI`, `personality analysis`, `type me`, or `分析我的 MBTI`.
```


### For OpenClaw

```text
Install this skill and analyze my MBTI: openclaw skills install mbti-analyzer
```

## How It Works

```
Discover → Analyze → Report
```

Discover identifies candidate source categories across your workspace and OpenClaw state. Analyze uses only the sources you allow, builds a traceable evidence pool, and asks follow-up questions only when uncertainty remains. Report renders the final HTML and Markdown outputs.

## Trust And Scope

- Candidate source categories may include workspace long-term memory (`MEMORY.md`), workspace daily notes (`memory/*.md`), OpenClaw sessions, memory index records, task metadata, and cron metadata.
- The skill is designed to exclude sensitive or low-signal paths such as `.env`, `credentials/*`, `identity/*`, approval files, generic config files, and runtime logs.
- It only reads sources you allow for the current run.
- Reports may include short excerpts from allowed sources unless quoting is disabled.
- Code review is welcome if you want to verify the data boundary yourself.

## Report Preview

Try the [interactive demo](https://kingofsoysauce.github.io/mbti-skill/) for a live sample report.

### Overview

Overview of the generated report

<p align="center">
  <img src="docs/assets/shared/report-overview.png" alt="Overview" width="600" />
</p>

### Narrative And Validation

<p align="center">
  <img src="docs/assets/shared/report-narrative-validation.png" alt="Narrative and validation" width="600" />
</p>

## What You Get

- A best-fit MBTI type hypothesis with explicit confidence.
- A preference profile that explains how each axis was scored.
- A traceable evidence chain instead of a raw-history guess.
- Adjacent-type comparison that shows why nearby alternatives did not win.
- Uncertainty and follow-up prompts when the evidence stays close.
- Automatic English/Chinese report rendering based on the source language mix.

## References

| Document | Purpose |
|---|---|
| [`SKILL.md`](SKILL.md) | Skill contract, maintainer notes, and stage workflow details |
| [`references/analysis_framework.md`](references/analysis_framework.md) | Four-preference + cognitive-function analysis model |
| [`references/evidence_rubric.md`](references/evidence_rubric.md) | Signal strength scoring and pseudo-signal filtering |
| [`references/report_copy_contract.md`](references/report_copy_contract.md) | Copy and tone rules for generated reports |
| [`references/report_structure.md`](references/report_structure.md) | Report section layout |

## License

MIT
