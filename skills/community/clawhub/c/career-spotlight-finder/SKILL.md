---
name: career-spotlight-finder
version: 1.0.0
description: Use when wanting to discover hidden strengths, industry buzzwords, and career narratives from past projects, articles, or code — for resumes, self-introductions, and personal branding
metadata:
  openclaw:
    requires:
      anyBins: [pandoc]
    homepage: https://github.com/RealZST/career-spotlight-finder
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - WebFetch
  - AskUserQuestion
---

# Career Spotlight Finder

Discover hidden strengths and career narratives from your past projects.

## Pipeline

```
Init → Analyze → Position → Synthesize → Write Copy → Review
```

## Quick Reference

| Step | Guide | Template |
|------|-------|----------|
| Init + Analyze | `guides/input-collection-guide.md`, `guides/project-analysis-guide.md` | `templates/project-analysis.md` |
| Position | `guides/domain-positioning-guide.md` | — |
| Synthesize | `guides/narrative-synthesis-guide.md` | `templates/aggregated-report.md` |
| Write Copy | `guides/copywriting-guide.md` | `templates/copywriting-variants.md` |

## Output

```
~/.career-spotlight/
├── analyses/    # per-project analyses
├── report.md    # aggregated career brand report
├── copies/      # resume-bullets, elevator-pitch, linkedin-summary, casual-intro
└── history/     # archived reports and prior copy
```

---

## Step 0 — Init

Read `guides/input-collection-guide.md` Section 1 and follow its procedure to set up `~/.career-spotlight/`.

## Step 1 — Analyze

Read `guides/input-collection-guide.md` Sections 2-8 for the full procedure. Summary:

1. Collect sources from the user (local paths, URLs, or `.docx` files).
2. Validate and expand sources (auto-detect document collections in directories).
3. Ask the user to set project priorities (`highlight` or `supporting`).
4. Check existing analyses for staleness (via git hash, file mtime, or URL age).
5. Run new analyses per `guides/project-analysis-guide.md`, write to `~/.career-spotlight/analyses/`.

## Step 2 — Position

1. Read `guides/domain-positioning-guide.md` and follow Sections 2-4.
2. Recommend one expert framing with a distinctiveness thesis. Keep alternatives as wrappers.
3. Ask the user to confirm the framing before proceeding.

## Step 3 — Synthesize

1. Read all analyses from `~/.career-spotlight/analyses/`.
2. Read `guides/narrative-synthesis-guide.md` and follow its methodology.
3. Archive any existing `report.md` to `~/.career-spotlight/history/report-YYYY-MM-DDTHH-MM-SS.md`.
4. Write the new report to `~/.career-spotlight/report.md` using `templates/aggregated-report.md`.

## Step 4 — Write Copy

1. Read `~/.career-spotlight/report.md`.
2. Read `guides/copywriting-guide.md` and follow its methodology.
3. Archive any existing files in `~/.career-spotlight/copies/` to `history/` with timestamp suffix.
4. Write four files to `~/.career-spotlight/copies/` using `templates/copywriting-variants.md`:
   - `resume-bullets.md`
   - `elevator-pitch.md`
   - `linkedin-summary.md`
   - `casual-intro.md`

## Step 5 — Review

Present a summary: positioning statement, theme line count, top 3 hidden capabilities.

Then offer:

1. Add more projects → Step 1
2. Change domain direction → Step 2
3. Adjust narrative emphasis → Step 3
4. Regenerate copy variants → Step 4
5. Accept and finish — remind the user their files are at `~/.career-spotlight/`
