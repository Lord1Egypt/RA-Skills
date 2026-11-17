---
name: cogneuro-paper-reader
description: Reads and summarizes cognitive neuroscience and experimental psychology research papers (PDF or plain text) on attention, working memory, sustained attention, memory, decision-making, and neural population coding. Extracts structured notes covering hypothesis, methods, participants, tasks, statistics, effect sizes, results, and limitations. Use when the user provides an academic paper and asks to summarize, explain, review, or extract key findings, methods, or statistics from it.
version: 1.0.0
metadata:
  openclaw:
    emoji: "📖"
---

# Cognitive Neuroscience Paper Reader

Read a cognitive-neuroscience / experimental-psychology paper (PDF or plain text)
and produce a structured, reproducible summary. Handles empirical studies,
reviews, and methods/theory papers.

## When to use

- The user shares a `.pdf` (or extracted text) of a paper on attention, working
  memory, sustained attention, memory, decision-making, or neural population
  coding and asks you to read, summarize, explain, or review it.

## Workflow

1. **Extract text.** If given a PDF, extract text first (for example
   `pdftotext -layout file.pdf file.txt`), then read the text. If extraction
   returns no text (a scanned PDF), say so and ask for text or OCR — do not
   fabricate content.
2. **Identify the paper type** — empirical study, review/meta-analysis, or
   methods/theory paper — and tailor the emphasis of the output.
3. **Fill the output template below.** Pull exact numbers from the text; never
   invent statistics. Write "not reported" for anything the paper omits.
4. **Define domain terms** using `references/domain-glossary.md` so a lay
   reader can follow the summary.
5. **Add a critical-reading section** — confounds, alternative explanations,
   limitations the authors admit, and what you would want to verify.

## Output template

1. **Citation** — authors, year, journal, DOI.
2. **Plain-language summary** — one paragraph: what they did and what they found.
3. **Research question & hypotheses.**
4. **Methods** — participants (n, population), task/paradigm, conditions, key
   manipulations, and measures (e.g. RT, accuracy, K, A′, response error).
5. **Analyses & statistics** — tests used (t-test, Spearman r, bootstrap, Bayes
   factor, Cohen's d) with exact values where reported.
6. **Key results** — numbered, each with its statistic.
7. **Conclusions & implications.**
8. **Limitations & confounds.**
9. **Key terms** — a short glossary of the domain terms used.
10. **Critical reading** — open questions, alternative explanations, what to check.

See `references/statistics-guide.md` for how to interpret the statistics, and
`references/domain-glossary.md` for definitions.

## Notes

- Prefer exact values; report both effect size and uncertainty (CI) when present.
- Note when a test is directional (one-tailed) or bootstrapped.
- Do not invent references or numbers; if absent, write "not reported".
