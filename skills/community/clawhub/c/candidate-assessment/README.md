# candidate-assessment

A Claude Code / [ClawHub](https://clawhub.ai) skill that **scores a candidate's
resume against a job description (JD)** and produces a clean, professional,
brand-neutral **HTML / PDF hiring assessment report** — a top-recruiter-grade
《候选人内部评估报告》.

## What it does

Given a resume and a target JD, it:
1. parses the resume into structured data,
2. reads the JD from any format (txt / md / pdf / docx / rtf),
3. scores the fit across a weighted 7-module model (硬实力 30% / 经验 30% /
   胜任力 15% / 动机稳定 10% / 潜力 10% / 文化 5% + 准入 + 亮点),
4. renders a report with an overall score & grade, per-dimension breakdown with
   score bars, an eligibility checklist, risk flags, and interview questions,
5. exports to PDF (in-page button or `--pdf` via headless Chrome).

## Dependency: resume-parsing

Step 1 uses the sibling skill
[**resume-parsing**](https://github.com/casperkwok/resume-parsing-skill) to turn
the resume PDF/DOCX into structured data without hallucination. Install it too:

```bash
clawhub install resume-parsing
clawhub install candidate-assessment
```

If `resume-parsing` isn't present, you can still run this skill by extracting the
resume text yourself, but the resume-parsing step is recommended.

## How it works

Same philosophy as resume-parsing — the model judges, scripts do the
deterministic parts:

- **`scripts/read_jd.py`** — reads the JD into plain text (pdf/docx via pdfmuse,
  auto-installed).
- **The model** — applies `reference/assessment-prompt.md` to resume + JD and
  writes `assessment.json`.
- **`scripts/render_report.py`** — renders `assessment.json` into a
  self-contained HTML report (and PDF with `--pdf`). Consistent visuals every
  time; no third-party deps.

## Usage

```bash
# 1. parse the resume with the resume-parsing skill → resume.json
# 2. read the JD
python scripts/read_jd.py JD.pdf --out jd.txt
# 3. the model writes assessment.json (see reference/assessment-prompt.md)
# 4. render HTML (+ PDF)
python scripts/render_report.py assessment.json --out report.html --pdf
```

In Claude Code just say *"用这份 JD 评估这个候选人"* / *"简历 JD 匹配评估"* and it
runs the whole flow.

## Output

- **`assessment.json`** — structured scores + analysis (reusable / for a DB).
- **`report.html`** — the report, with a 「⬇ 导出 PDF」 button and print-friendly
  styles (A4, colors preserved, no mid-card page breaks).
- **`report.pdf`** — with `--pdf`, a print-ready A4 PDF.

## Requirements

- `python3`
- [`pdfmuse`](https://pypi.org/project/pdfmuse/) (auto-installed; for pdf/docx JDs)
- Headless Chrome / Chromium / Edge — optional, only for `--pdf`
- [resume-parsing](https://github.com/casperkwok/resume-parsing-skill) skill (for
  the resume step)

## Credits

Resume extraction: [pdfmuse](https://github.com/casperkwok/pdfmuse) via
[resume-parsing](https://github.com/casperkwok/resume-parsing-skill). Report
design language adapted from an internal PRD (brand-neutral). Licensed under MIT.
