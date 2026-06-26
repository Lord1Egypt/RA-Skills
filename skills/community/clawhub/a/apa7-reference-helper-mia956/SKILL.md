---
name: apa7-reference-helper
description: Format, audit, and polish academic references in APA 7th style, including in-text citations, DOI/URL cleanup, and correction tables for student papers.
version: 1.0.0
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    emoji: "📚"
---

# APA 7 Reference Helper

## Purpose
Use this skill when the user needs help with APA 7th edition references, in-text citations, reference-list cleanup, or a citation-quality audit for coursework, manuscripts, reports, literature reviews, or presentations.

This skill is designed for bilingual academic workflows. It can explain corrections in Chinese while producing references in English APA 7 format when the source metadata is in English.

## When to activate
Activate this skill when the user asks for any of the following:

- Format references in APA 7th style.
- Check whether references are complete or standardized.
- Convert rough citation information into a reference list.
- Generate in-text citations or parenthetical citations.
- Clean DOI, URL, journal title, volume, issue, page, publisher, or author formatting.
- Produce a table of reference problems and corrections.
- Prepare references for a psychology, education, medicine, public health, or social-science assignment.

## Required output behavior
When handling references, produce the answer in this order unless the user requests otherwise:

1. **可直接粘贴的 APA 7 参考文献列表**  
   Provide a clean final list. Sort alphabetically by first author's surname when there are multiple entries.

2. **问题检查表**  
   Provide a compact table with columns: `原条目`, `主要问题`, `建议修正`.

3. **文内引用示例**  
   Provide parenthetical and narrative citation examples for the most important references.

4. **不确定信息**  
   Clearly mark missing metadata instead of inventing it. Use `[缺失：年份]`, `[缺失：期刊名]`, `[缺失：DOI]`, etc.

## APA 7 formatting rules
Follow these rules strictly:

### Journal article
Template:

`Author, A. A., Author, B. B., & Author, C. C. (Year). Article title in sentence case. Journal Title in Title Case, volume(issue), page–page. https://doi.org/xxxxx`

Rules:

- Use sentence case for article titles.
- Use title case and italic style conceptually for journal titles. If plain text is required, do not use Markdown italics unless the user asks.
- Include issue number only when available.
- Format DOI as a URL: `https://doi.org/...`.
- Do not write `Retrieved from` for stable academic sources unless retrieval date is necessary.

### Book
Template:

`Author, A. A. (Year). Book title in sentence case. Publisher.`

Rules:

- Do not include publisher location.
- Include edition after the title when available, e.g., `(2nd ed.)`.

### Chapter in edited book
Template:

`Author, A. A. (Year). Chapter title in sentence case. In E. E. Editor & F. F. Editor (Eds.), Book title in sentence case (pp. xx–xx). Publisher.`

### Webpage
Template:

`Author, A. A. or Organization Name. (Year, Month Day). Page title in sentence case. Site Name. URL`

Rules:

- Use organization as author if no individual author is available.
- Include retrieval date only for pages designed to change over time.
- If author and site name are identical, omit the site name.

## In-text citation rules

- One author: `(Smith, 2020)` or `Smith (2020)`.
- Two authors: `(Smith & Lee, 2020)` or `Smith and Lee (2020)`.
- Three or more authors: `(Smith et al., 2020)` from the first citation onward.
- Multiple sources in one parenthesis: sort alphabetically and separate with semicolons.
- Direct quote: include page number, e.g., `(Smith, 2020, p. 15)`.

## Quality-control checklist
Before finalizing, check:

- Are all years present?
- Are author initials formatted consistently?
- Is the article title in sentence case?
- Is the journal title in title case?
- Are volume, issue, and pages distinguishable?
- Is the DOI formatted as `https://doi.org/...`?
- Are Chinese explanations separated from English reference entries?
- Are missing fields explicitly marked rather than hallucinated?

## Optional helper script
This skill includes `scripts/apa7_quick_check.py`, a lightweight local checker that flags common structural problems in a plain-text reference list. It uses only Python standard-library modules.

Use it when the user provides or uploads a text reference list and wants a quick audit:

```bash
python3 scripts/apa7_quick_check.py examples/demo_references.txt
```

If `python3` is not available, try:

```bash
python scripts/apa7_quick_check.py examples/demo_references.txt
```

The script does not replace academic judgment. Use its output as a triage aid, then apply the APA 7 rules above manually.

## Safety and integrity

- Do not fabricate authors, years, journals, volumes, issues, pages, DOIs, or URLs.
- When metadata is incomplete, ask for the missing field only if essential; otherwise mark it clearly.
- Do not use hidden web access unless the user explicitly wants current verification or source lookup.
- Do not claim that a DOI exists unless it is provided or verified.
