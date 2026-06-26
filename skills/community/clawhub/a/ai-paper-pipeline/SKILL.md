---
name: ai-paper-pipeline
description: Build or improve a top-tier AI conference paper workflow for NeurIPS, ICML, ICLR, and similar venues. Use when the user asks to generate a paper pipeline, organize a paper project, turn a mega prompt into a reusable skill, structure literature→experiment→writing loops, or create/update files like MEGA_PROMPT.md, RESTRICTS.yaml, PROGRESS.md, LaTeX paper skeletons, and per-stage plans for an academic paper project.
---

# AI Paper Pipeline

Turn a rough paper idea or a long "mega prompt" into a reusable, reality-grounded paper project scaffold.

## What this skill should do

- Normalize a user's long paper-workflow prompt into a maintainable skill/project structure.
- Keep the main workflow concise in `SKILL.md` and push bulky reference text into `references/`.
- Preserve academic-integrity constraints: no fabricated experiments, no fake citations, no unsupported claims.
- Prefer creating reusable project scaffolding over dumping one giant prompt blob.

## Default workflow

1. Identify whether the user wants one of these:
   - **skill cleanup / packaging** for the paper workflow itself
   - **project initialization** for a specific paper
   - **template ingestion** from a pasted mega prompt
2. If the user pasted a large workflow prompt, extract and organize it into:
   - `SKILL.md` for concise usage instructions
   - `references/` for long-form reference content
   - `templates/` for starter files like `RESTRICTS.example.yaml`
3. Keep only trigger logic, workflow guidance, and file navigation in `SKILL.md`.
4. Put long source material, detailed prompts, and heavy policy text in `references/`.
5. If the user wants a paper project initialized, create at minimum:
   - `MEGA_PROMPT.md`
   - `RESTRICTS.yaml`
   - `PROGRESS.md`
   - `plans/`
   - `code/`, `data/`, `docs/`, `results/`
   - `paper/mypaper/main.tex`
   - `paper/mypaper/sections/`
6. After edits, package or commit changes if appropriate.

## File layout for this skill

```text
ai-paper-pipeline/
├── SKILL.md
├── MEGA_PROMPT.md
├── references/
│   ├── full-pipeline-template.md
│   └── project-scaffold.md
└── templates/
    └── RESTRICTS.example.yaml
```

## When to read extra files

- Read `MEGA_PROMPT.md` when you need the concise built-in version of the 25-stage workflow.
- Read `references/full-pipeline-template.md` when the user wants the verbose original template or asks to reconstruct/port the full prompt.
- Read `references/project-scaffold.md` when the user wants to initialize a concrete paper project directory.
- Read `templates/RESTRICTS.example.yaml` when initializing a new paper project or drafting a restrictions file.

## Working rules

- Treat the paper as a **real research artifact**, not a vibe-writing exercise.
- Never claim experiments, datasets, ablations, or statistical tests that are not actually present.
- Never keep huge duplicated prompt text in multiple files.
- Prefer editable project artifacts over giant single-message outputs.
- Keep the paper workflow cyclical: literature → design → run → analyze → draft → review → revise.

## Good outputs

### A. User says: "整理成一个 Skill"

Do this:
- Clean up the current skill folder.
- Convert ad-hoc text into proper `SKILL.md` + `references/` + `templates/`.
- Keep `SKILL.md` concise and reusable.

### B. User says: "按这个模板起一个论文项目"

Do this:
- Create a new `<project>-paper/` scaffold.
- Copy in starter files.
- Replace placeholders with project-specific metadata where provided.

### C. User says: "把这份 mega prompt 落库"

Do this:
- Save the raw template in `references/` or project root.
- Avoid bloating `SKILL.md` with the full raw text.

## Final step

After modifying this skill or creating paper-project files in the workspace, commit the changes with a clear git message.
