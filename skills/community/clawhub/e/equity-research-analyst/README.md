# Equity Research Analyst Skill

This repository contains the source for the `equity-research-analyst` skill: a reusable AI skill for producing institutional-style equity research deliverables with a structured workflow, TradingView-backed market data, and workflow-specific reference materials.

## What This Skill Does

The skill is designed to help an AI agent handle common sell-side and buy-side research tasks such as:

- initiation-of-coverage reports
- earnings analyses
- earnings previews
- catalyst calendars
- morning notes
- sector overviews
- thesis trackers
- financial model updates
- idea-generation and stock screens

The skill prefers structured numeric data from the bundled `tradingviewapi` reference set, then falls back to web research for narrative material such as guidance wording, transcripts, risk factors, management commentary, and proprietary industry context.

## `SKILL.md` Is The Real Entry Point

The most important file in this repository is [SKILL.md](/Users/barry/code/skills/equity-research-analyst/SKILL.md).

For git users, this `README.md` explains the repository. For AI agents, `SKILL.md` is the actual product entry point and the file that gets packaged into the distributable `.skill`.

`SKILL.md` defines:

- the skill metadata used for triggering
- which user requests should map to which workflow
- how the agent should load files progressively instead of reading everything at once
- when to use `tradingviewapi` versus web research
- which workflows already have explicit `tradingviewapi` playbooks for earnings, previews, model updates, thesis tracking, morning notes, sector work, and idea generation
- global conventions for freshness checks, citation style, ticker resolution, and output formatting

In practice, `SKILL.md` acts as a dispatcher. It does not try to contain every detail inline. Instead, it routes the agent to the smallest relevant file in `references/` for the active task.

## How The Skill Is Organized

The repository follows a progressive-disclosure structure:

- `SKILL.md`
  The top-level dispatcher and packaged entry point.
- `references/workflows/`
  Workflow routing files such as initiating coverage, earnings analysis, earnings preview, and idea generation.
- `references/initiating-coverage/`
  Deep-dive task files for the five-step initiation workflow.
- `references/earnings-analysis/`
  Detailed guidance for earnings-update execution, report structure, and QA.
- `references/tradingviewapi.md`
  The main task-to-endpoint mapping for the TradingView proxy API, now including workflow-specific scenarios beyond earnings and initiation.
- `references/tradingviewapi-docs/`
  Bundled API specification and endpoint examples used as a lookup bundle.
- `assets/`
  Output-oriented templates, currently focused on initiation-report assembly.

## Key Design Ideas In `SKILL.md`

If you are reviewing or extending this skill, these are the main design decisions to understand first:

- Single-workflow discipline
  The agent should map a request to one workflow at a time.
- Progressive disclosure
  The agent should read only the workflow and reference files needed for the active task.
- Structured-data-first research
  Numeric market and financial content should come from `tradingviewapi` before web search.
- Workflow-specific endpoint mapping
  Each major workflow should say which `tradingviewapi` endpoints provide its numeric baseline, and which tasks still need Web / SEC / IR follow-up.
- Clear fallback rules
  Web search is still required for narrative, regulatory, and transcript-heavy content.
- Institutional output standards
  Reports are expected to follow consistent citation, formatting, and completeness rules.

## Repository-Only Files Vs Packaged Skill Files

This repository is both:

- a git repository for humans
- a source directory for a packaged `.skill` artifact

That means some files are useful for the repository but should not be shipped inside the final skill package.

- `.skillignore` defines repo-only files to exclude from packaged `.skill` artifacts
- `README.md` is intentionally kept for the git repository and excluded from `.skill` output
- the packager also skips `.git/` by default

This keeps the distributed skill clean while still allowing the repository to have normal project documentation.

## Packaging

To validate and package the skill from the repository root:

```bash
python3 ~/.agents/skills/skill-creator/scripts/package_skill.py .
```

The packager now respects `.skillignore`, so repo-only files like this `README.md` are not included in the generated `.skill` file.
