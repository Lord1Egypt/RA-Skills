---
name: djtu-vehicle-eng-thesis-check
description: >
  Activated ONLY by the explicit slash command /djtu-vehicle-eng-thesis-check.
  Do NOT activate on generic phrases like "check my thesis", "format my paper",
  or "convert to Word". This skill validates and builds DJTU Vehicle Engineering
  thesis documents from a Markdown draft into a formatted .docx file.
---

# DJTU Vehicle Engineering Thesis Checker & Formatter

Activate ONLY when the user explicitly runs the command:

```
/djtu-vehicle-eng-thesis-check
```

Do NOT activate on natural language requests such as "check my thesis",
"format my paper", "generate docx", or "convert to Word" — those are too broad
and may not relate to a DJTU Vehicle Engineering thesis.

---

## STRICT RULES — read before doing anything

**NEVER use `pypandoc.download_pandoc()` or download pandoc from GitHub.**

**NEVER attempt to install pandoc by any method other than `check_env.sh`.**
Do not write ad-hoc install commands. Do not try `apt-get` without sudo.
Do not try running without sudo as a fallback. These will always fail silently
or with errors and waste the user's time.

**If `check_env.sh` outputs `[SUDO NEEDED]`:**
- STOP immediately. Do not try any alternative install method.
- Tell the user: "Please run this command in your terminal, then let me know
  when it's done:" and show them the exact command from the script output.
- Wait for the user to confirm, then re-run `bash scripts/check_env.sh`.

**sudo scope:** sudo is used ONLY for `apt-get install -y pandoc` (or dnf).
Never for pip, never for building the docx, never for anything else.

**pandoc install priority (handled by check_env.sh automatically):**
1. `sudo apt-get install -y pandoc` — always first
2. `sudo dnf install -y pandoc` — if apt not available
3. `brew install pandoc` — macOS only
4. If all fail: tell user to search https://gitee.com, paste the URL

---

## Workflow

### Step 1 — Environment Check (always run first, no exceptions)

```
bash scripts/check_env.sh
```

Run this and follow its output exactly:
- If it prints `[OK]` for all items → proceed to Step 2.
- If it prints `[SUDO NEEDED]` → stop, show the user the command, wait for
  them to run it, then re-run this step.
- If it prints `[ERROR]` or `[MISSING]` for anything other than pandoc →
  report the error to the user and stop.

Full dependency list: `references/requirements.txt`.

---

### Step 2 — Validate the Draft

```
python scripts/validate.py <path/to/draft.md>
```

Checks performed (rules sourced from `references/formatting-spec.md`):

| Check | What it looks for |
|-------|------------------|
| Cover page fields | `学生姓名`, `导师`, `专业名称`, `学号` in first 50 lines |
| Section order | `摘要` → `绪论` → `结论` → `参考文献` → `致谢` all present as H1, in order |
| Heading hierarchy | No H3 before H2; no headings deeper than H3 |
| Figure captions | Every `![…]` image followed by `图X.X 图名` on next non-empty line |
| Table captions | Every table row preceded by `表X.X 表名` caption |
| Citations | No author-year format `(Smith, 2020)` — must use `[n]` superscript |
| References section | `# 参 考 文 献` exists; entries numbered `[1] Author …` |
| Abstract length | Chinese abstract: 500–800 CJK characters |
| Total length | Total CJK character count flagged if < 10 000 |
| Glossary terms | Technical terms cross-checked against `references/glossary.md` |

Warnings report line numbers only — no draft content is echoed into output.
Fix all `[ERROR]` items before proceeding. `[WARN]` items are advisory.

---

### Step 3 — Build the .docx

```
python scripts/build_docx.py <path/to/draft.md> <output/thesis.docx>
```

Applied formatting (all values from `references/formatting-spec.md`):

| Element | Value |
|---------|-------|
| Margins | Top 2.5 cm / Bottom 2.0 cm / Left 2.0 cm / Right 2.0 cm |
| Body font | SimSun (宋体) + Times New Roman, 小四号 (12pt) |
| Body spacing | 多倍行距 1.25×, first-line indent 2 characters (24pt) |
| H1 font | SimHei (黑体) + Times New Roman, 小三号 (15pt), centered, page-break before |
| H2 font | SimHei + Times New Roman, 四号 (14pt), justified, 1.5× spacing |
| H3 font | SimHei + Times New Roman, 小四号 (12pt), justified, 1.5× spacing |
| TOC | Auto-generated, 3 levels deep |
| Section numbering | Preserved as-is from the Markdown headings (no auto-numbering) |

Output: `<output/thesis.docx>` — open in Word for final review.

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/formatting-spec.md` | Official DJTU formatting rules (extracted from 模板.docx comments) |
| `references/glossary.md` | Vehicle engineering terminology & standard abbreviations |
| `references/requirements.txt` | pip dependencies (pinned versions) |
| `references/examples/chapter-sample.md` | Correctly-formatted sample chapter |
| `references/examples/bad-vs-good.md` | Common mistakes with corrections |

---

## Notes

- `build_docx.py` applies fonts, margins, spacing, and page breaks.
  Final touches (page headers, Roman numeral front-matter page numbers,
  three-line table borders) still require manual adjustment in Word.
- Caption format must exactly match `图X.X 图名` / `表X.X 表名` for validation to pass.
- Glossary terms are loaded from `references/glossary.md`.
  Add project-specific terms there before running validate.py.
