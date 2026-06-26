# Academic Thesis Review Skill

[简体中文](README.zh-CN.md)

Reusable agent skill for reviewing Chinese master's theses in multiple rounds.

## Overview

This repository packages a reusable thesis-review skill for agent frameworks such as:

- OpenCode
- OpenClaw
- Claude Code
- Other markdown-based prompt/skill loaders

The skill focuses on **Chinese master's theses** (硕士学位论文) in general, while remaining especially well-suited for management-oriented programs such as **MBA**, **MEM**, and **MPA**, as well as other similar professional or applied research master's theses.

It uses a **3-round review strategy**:

1. Macro structure review
2. Per-chapter deep review
3. Inter-chapter consistency review

It is designed to generate **strict but actionable** revision feedback in Chinese.

## Multi-round Review Support

Yes — this skill explicitly supports **multi-round review workflows**.

- **Round 1:** macro structure and overall logic
- **Round 2:** chapter-by-chapter deep review
- **Round 3:** inter-chapter consistency review
- **Iterative re-review:** if an existing `review_results.md` is present, the skill can verify whether previously flagged issues were fixed, partially fixed, or left unchanged

This makes it suitable not only for a first-pass review, but also for **revision follow-up and repeated review cycles**.

## Files

- `SKILL.md` — canonical cross-platform skill entry with metadata frontmatter
- `skill.json` — repository-level metadata for publishing and later automation
- `.gitignore` — recommended ignore rules for local temp outputs

## Supported Agent Use Cases

This skill is intended for agent systems that can load or reference a markdown instruction file as a reusable skill, command, prompt, or workflow definition.

Recommended scope:

- MBA theses
- MEM theses
- MPA theses
- Other management, public administration, engineering management, and similarly structured applied master's theses

Typical use cases:

- Review a `.docx` thesis draft
- Re-review a revised thesis against prior comments
- Produce a structured `review_results.md`

## Installation

Because different agent frameworks organize skills differently, use one of these approaches:

### Option 1: Direct file use

Point your agent system to `SKILL.md` directly.

### Option 2: Copy into your skill directory

Copy this folder into the target framework's local skills/prompts directory and register it according to that framework's conventions.

#### Claude Code

Personal install:

```bash
mkdir -p ~/.claude/skills/academic-thesis-review
cp -r . ~/.claude/skills/academic-thesis-review
```

Project install:

```bash
mkdir -p .claude/skills/academic-thesis-review
cp -r . .claude/skills/academic-thesis-review
```

#### OpenClaw

Suggested global install:

```bash
mkdir -p ~/.openclaw/skills/academic-thesis-review
cp -r . ~/.openclaw/skills/academic-thesis-review
```

#### OpenCode / compatible prompt loaders

Use `SKILL.md` as the imported markdown asset.

### Option 3: Reference this GitHub repository

Upload this folder to GitHub, then use the raw markdown or repository contents wherever your agent platform accepts remote or synced prompt assets.

## Suggested Trigger Phrases

- 审阅论文
- review thesis
- 论文评审
- 帮我看看论文
- 修改后再看看

## Inputs Expected by the Skill

- Thesis file in `.docx` format
- Python available for text extraction
- Optional existing `review_results.md` for iterative review mode

## Output

- Markdown review report: `review_results.md` (working directory)
- Extracted thesis text and working notes: `review_artifacts/` directory (auto-created)

## Repository Metadata

- Author GitHub: https://github.com/wmpluto
- Repository URL: `https://github.com/wmpluto/academic-thesis-review-skill`
- Homepage / docs URL: `https://github.com/wmpluto/academic-thesis-review-skill`

## Publishing Notes

- `SKILL.md` is the canonical file for ecosystems following the Agent Skills style convention.
- On Windows, case-only duplicate filenames such as `SKILL.md` and `skill.md` cannot reliably coexist, so this package standardizes on `SKILL.md`.
- `skill.json` is a generic metadata file for publishing convenience. It is not assumed to be required by every agent framework.
- Replace remaining placeholder values only if you later add a separate homepage or documentation site.

## Changelog

### v1.1.0

**Scope broadened** — Removed the "management-oriented" restriction from the skill description. The skill now targets Chinese master's theses in general, while remaining especially well-suited for MBA / MEM / MPA programs.

**Structured output directory** — Review artifacts (extracted thesis text, working notes) are now written to a `review_artifacts/` subdirectory with timestamped filenames, keeping the working directory clean.

**Anti-anchoring iterative review** — In iterative mode (re-reviewing a revised thesis), each chapter now goes through a two-phase review:

- **Phase A (Independent Discovery):** The agent reviews the chapter with NO historical issues visible, using a dimension coverage checklist as evidence of systematic review.
- **Phase B (Historical Verification):** Only after Phase A is complete are prior issues injected for verification (✅ fixed / ⚠️ partially fixed / ❌ unchanged).

This separation prevents the agent from treating prior issues as a checklist and skipping independent analysis.

**Round 1 isolation in iterative mode** — Round 1 no longer receives any injected prior issues (including global-scope ones). It executes identically to first-version mode, ensuring a fully independent macro-level assessment.

**Spot check mechanism** — When a chapter's Phase A claims "no new issues found" but that chapter has serious historical issues, Round 3 can trigger a targeted spot check (up to 3 per cycle) to validate the claim.

**Working file structure** — A detailed working file template is now defined for iterative mode, providing full traceability of the review process (Phase A / Phase B records, spot checks, historical issue verification summary).

**Enhanced consolidation** — Persistent issues (flagged across 3+ consecutive versions) now receive escalated treatment: minimum-cost fix suggestions, defense risk assessment, and (from version 4+) oral defense preparation advice.

### v1.0.0

Initial release.

## Notes

- If you later decide to target a specific platform with a strict manifest format, add that platform-specific file separately instead of replacing `SKILL.md`.
