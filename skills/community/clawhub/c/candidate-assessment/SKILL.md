---
name: candidate-assessment
description: Evaluates how well a candidate's resume matches a target job description (JD) and produces a clean, professional HTML assessment report. Parses the resume (via the resume-parsing skill), reads the JD from any format (txt/md/pdf/docx), scores the fit across a weighted 7-module model, and renders a hiring report with overall score, grade, dimension breakdown, risks, and interview questions. Use when the user wants to assess/score a candidate against a job, match a resume to a JD (简历 JD 匹配 / 候选人评估 / 匹配度打分 / 招聘评估), or generate a candidate evaluation report.
version: 1.0.3
license: MIT
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env: []
---

# Candidate assessment (resume × JD match)

Score a resume against a job description and produce a **clean, professional
HTML evaluation report** (brand-neutral) — for a top-recruiter-grade hiring
assessment.

## How it works — division of labor

Same philosophy as `resume-parsing`: the model does judgment, scripts do the
deterministic parts.

- **`resume-parsing` skill** turns the resume PDF/DOCX into structured
  `resume.json` + clean markdown (no hallucination).
- **`scripts/read_jd.py`** reads the JD from any format into plain text.
- **You (the model)** apply the evaluation model in
  `reference/assessment-prompt.md` to the resume + JD and produce
  `assessment.json` (scores, analysis, risks, questions).
- **`scripts/render_report.py`** renders `assessment.json` into a self-contained,
  professionally-styled `report.html` — consistent visuals every time.

Only `python3` is needed; `pdfmuse` auto-installs on first use.

## Workflow

Copy this checklist and track progress:

```
- [ ] 1. Parse the resume (resume-parsing skill) → resume.json + .extract.md
- [ ] 2. Read the JD (read_jd.py) → jd text
- [ ] 3. Read reference/assessment-prompt.md
- [ ] 4. Evaluate → write assessment.json (per the schema there)
- [ ] 5. Render → render_report.py assessment.json --out report.html
- [ ] 6. Open report.html in the browser
```

### Step 1 — Parse the resume

Use the **resume-parsing** skill on the candidate's resume to get `resume.json`
and `<name>.extract.md`. (Directly:
`python ~/.claude/skills/resume-parsing/scripts/extract.py RESUME.pdf --out out`,
then map to `resume.json` per that skill.)

### Step 2 — Read the JD

```bash
python scripts/read_jd.py JD.pdf --out jd.txt      # .txt/.md/.pdf/.docx/.rtf
```

If the target position name isn't obvious, take it from the JD title (fallback:
the JD filename), and confirm with the user if ambiguous.

### Step 3–4 — Evaluate

Read `reference/assessment-prompt.md` — it defines the recruiter role, the
weighted 7-module model (0 准入 / 1 硬实力 30% / 2 经验 30% / 3 胜任力 15% /
4 动机稳定 10% / 5 潜力 10% / 6 文化 5% / + 亮点), the scoring discipline
(evidence only, quantify, specific risks), and the exact `assessment.json`
schema. Write `assessment.json` following it.

### Step 5 — Render (HTML, and PDF if wanted)

```bash
python scripts/render_report.py assessment.json --out report.html          # HTML
python scripts/render_report.py assessment.json --out report.html --pdf    # + report.pdf
```

`--pdf` prints the report to `report.pdf` via headless Chrome (colors preserved,
no browser header/footer). If no Chrome/Chromium/Edge is found, skip `--pdf` and
use the in-page button instead.

### Step 6 — Show it

```bash
open -a "Google Chrome" report.html    # macOS; falls back to any browser
```

The HTML has a floating **「⬇ 导出 PDF」** button (Print → Save as PDF) with
print-friendly styles (A4, colors kept, no mid-card page breaks, button hidden
in the PDF) — so the user can export a clean PDF themselves anytime.

## Output

- **`assessment.json`** — structured scores + analysis (reusable / for a DB).
- **`report.html`** — the 候选人内部评估报告, clean brand-neutral design; export to
  PDF via the in-page button or `--pdf`. Design tokens: `reference/report-design.md`.
- **`report.pdf`** — (with `--pdf`) print-ready A4 report.

## Reference files

- `reference/assessment-prompt.md` — evaluation model + `assessment.json` schema.
- `reference/report-design.md` — design tokens the report follows (indigo accent + semantic colors).
- `scripts/read_jd.py` — JD reader (run it).
- `scripts/render_report.py` — JSON → HTML renderer (run it).
