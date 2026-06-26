---
name: arxiv-cv-daily
description: Fetch arXiv papers for a target date in cs.CV, screen them against a user topic, save logs under a user-chosen output directory, download matched PDFs, and summarize the matched papers from full text.
---

# arXiv cs.CV Topic Daily Workflow

Use this skill when the user gives a topic and a date and wants you to:

- fetch the arXiv papers for that day in `cs.CV`
- save all titles and abstracts under a chosen output directory
- screen papers against the topic
- download the matched papers
- read the downloaded full text before summarizing
- optionally repeat that workflow across multiple consecutive days

Do not use `.openclaw/skills/auto-research-ideation` for this workflow. This skill must run independently.

## Interaction Contract

When the user calls this skill, follow this sequence:

1. Extract or confirm the `topic` and `date`.
2. Decide the output root. If the user already gave one, use it. Otherwise ask the user where logs and artifacts should be saved before running the workflow. If the user explicitly says they have no preference or wants the default, use `/tmp`.
3. Expand the topic into a structured topic spec JSON and save it under the chosen output root.
4. Tell the user what you are about to do.
5. Run the workflow script and pass `--topic-spec-file` plus `--output-root`.
6. Tell the user that the titles, abstracts, logs, PDFs, extracted text, and topic spec have been saved under the chosen output root.
7. Use the saved screening results to identify which papers matched the topic.
8. In your first user-facing result, list matched papers day by day. For each paper, include at least the title and relevance score.
9. Only after listing the matched papers should you ask or infer which papers the user wants to inspect in more detail.
10. Read the downloaded full text from `extracted_text/*.txt` before writing any detailed paper summaries.
11. Save your own final user-facing summary into the same run directory.

If the user asks for multiple days, process them sequentially. Finish the first requested day, report progress, then continue to the next day. Keep the logs and outputs separated by day. Do not report the same resolved release day twice in one multi-day run; if fallback for a later requested day lands on a date that was already used earlier in the run, keep walking backward.

While you work, send short progress updates to the user. The user should know when you are:

- fetching the daily paper list
- loading a cached daily paper list if it already exists
- saving the raw catalog
- screening titles
- screening abstracts
- downloading PDFs
- reading extracted full text
- writing the final summary

Do not claim a paper matches the topic unless the saved title and abstract screening logs support it. If a title is inconclusive, inspect the abstract. If the paper still looks relevant enough to keep, download it and inspect the extracted full text before summarizing.

Default download rule:

- If the paper is already clearly relevant from the title or abstract, do not download the PDF just to confirm relevance.
- Only trigger automatic PDF download when title plus abstract are still inconclusive and the paper needs full-text review.
- If the user later asks for a detailed reading of a specific paper, then use the saved PDF and extracted full text if available, or download that paper at that point.

Default interaction pattern:

1. First response after the workflow finishes:
   List the matched papers day by day.
   For each paper include:
   - title
   - arXiv ID
   - relevance score
   - short one-line match reason if useful
   Do not jump straight into long paper summaries here.
   Prefer a mobile-friendly numbered list, not a wide markdown table.
   Use this format:

   `2026-03-20`

   `1. Paper Title`
   `arXiv ID: 2603.12345`
   `相关性分数: 17`
2. Second-stage analysis:
   When the user asks to inspect one or more specific papers, then read the saved full text and produce a proper paper analysis.

When analyzing a specific paper in detail, cover these points:

- Problem: what problem the paper is solving and why it matters
- Method: the core idea, model, algorithm, or system design
- Data / Setting: datasets, benchmarks, or evaluation setting
- Results: the main quantitative or qualitative findings
- Takeaway: why this paper is relevant to the user's topic
- Limits: obvious caveats, scope limits, or unanswered questions when visible in the paper

Use this detailed-paper output shape by default:

1. `Title`
2. `Why It Was Retrieved`
3. `Problem`
4. `Method`
5. `Data / Benchmark`
6. `Main Results`
7. `Why It Matters For The User Topic`
8. `Limitations / Open Questions`
9. `Saved Files`

For `Why It Was Retrieved`, explicitly cite the saved evidence:

- relevance score
- match status
- whether the match came from title, abstract, or full text
- the saved PDF path
- the saved extracted text path

For `Method`, prefer answering:

- what inputs the model/system uses
- what the main architectural or algorithmic novelty is
- what the pipeline looks like at a high level

For `Main Results`, prefer answering:

- what baselines it compares against
- what the strongest reported result is
- whether the gains are broad or narrow

If the paper text is incomplete or extraction quality is poor, say so explicitly instead of overclaiming.

The topic spec should be a JSON object. A good default structure is:

```json
{
  "topic": "文档理解",
  "canonical_topic": "document understanding",
  "positive_phrases": [
    "document understanding",
    "visual document understanding",
    "document parsing",
    "pdf parsing",
    "table extraction"
  ],
  "anchor_terms": [
    "document",
    "layout",
    "pdf",
    "table",
    "form"
  ],
  "related_topics": [
    "ocr",
    "table understanding"
  ],
  "negative_phrases": [
    "audio-video understanding",
    "video understanding",
    "3d scene understanding"
  ]
}
```

Generate this JSON from the user's topic, save it under the chosen output root, and then pass it to the script. Prefer this model-generated topic spec over hardcoded topic expansion.

## Storage Rule

All workflow outputs must be saved under the chosen `output_root`. Before running the workflow, explicitly confirm that output root with the user unless the user already provided it. If the user explicitly says they have no preference or asks for the default, use `/tmp`. This includes:

- raw request metadata
- generated topic spec JSON
- fetched paper lists
- title and abstract screening logs
- downloaded PDFs
- extracted full-text `.txt` files
- activity logs
- the final user-facing summary you produce

Prefer keeping one run's artifacts under one output root so the user can find them easily.

## Entry Point

Resolve the launcher path from the installed skill location in the current deployment environment. Do not hardcode a personal absolute path in instructions. For local shell use, a relative invocation from the repo root is fine:

```bash
python3 arxiv_cs_cv_daily.py \
  --topic "document understanding or OCR" \
  --topic-spec-file /tmp/topic_specs/document_understanding.json \
  --date 2026-03-22 \
  --days 3 \
  --category cs.CV \
  --timezone Asia/Shanghai \
  --output-root /tmp \
  --output json \
  --verbose
```

In deployed environments such as Telegram bots, the bot/backend should resolve the launcher path from the installed skill location. Do not ask the end user for a launcher path. The only filesystem choice that may be exposed at the interaction layer is `output_root`, and this skill should ask for that before running unless the user already gave it.

## Environment Requirements

- Python 3.11 or newer
- `pdftotext` available on `PATH` for PDF text extraction
- write access to the selected output root, default `/tmp`
- network access to `export.arxiv.org` and `arxiv.org`

## Main Inputs

- `--topic`: required
- `--topic-spec-file /path/to/spec.json`: optional but preferred; structured topic expansion generated by the model
- `--date YYYY-MM-DD`: optional; defaults to today in the requested timezone
- `--days N`: optional; process `N` consecutive days starting from `--date` and walking backward one day at a time
- `--category`: defaults to `cs.CV`
- `--timezone`: defaults to `UTC`
- `--fallback-days`: how far to walk backward if the requested day has no papers
- `--max-results`: arXiv API page size
- `--limit`: limit the number of fetched papers after daily filtering
- `--output-root`: defaults to `/tmp`
- `--output json|markdown`: console output format
- `--verbose`: include full text content in JSON output (default: false for more concise output)

## Progress Feedback

The script now provides real-time progress updates:

- `[1/110] Screening titles...` - Title screening progress
- `[10/110] Screening titles...` - Every 10 papers
- `✓ Screening complete: 87/110 papers matched.` - Summary after screening
- `Downloading 18 PDFs for full-text review...` - Before PDF downloads
- `[1/18] Downloading 2603.20187v1...` - Per-PDF download progress

These progress messages appear on stderr and won't interfere with JSON output on stdout.

## Workflow Outputs

Each run creates a readable directory under the chosen output root, for example:

`/tmp/2026-03-23_103000_cs-cv_document-understanding-or-ocr_2026-03-22`

Typical files:

- `01_request.json`
- `topic_specs/*.json`
- `07_manifest.json`
- `07_summary.md`
- `activity.log`
- `days/YYYY-MM-DD/02_all_papers.json`
- `days/YYYY-MM-DD/02_all_papers.md`
- `days/YYYY-MM-DD/03_title_screening.json`
- `days/YYYY-MM-DD/04_abstract_screening.json`
- `days/YYYY-MM-DD/05_matched_papers.json`
- `days/YYYY-MM-DD/06_downloads_and_text.json`
- `days/YYYY-MM-DD/07_manifest.json`
- `days/YYYY-MM-DD/07_summary.md`
- `days/YYYY-MM-DD/downloads/*.pdf`
- `days/YYYY-MM-DD/extracted_text/*.txt`
- `cache/arxiv_api/<category>/<date>.json`

After you inspect the saved full text and write the final answer for the user, also save:

- `08_user_summary.md`

## How To Talk To The User

Use concrete status updates. For example:

- "我先根据你的主题生成一个结构化 topic spec，再用这个 spec 去筛选最近几天的 `cs.CV` 论文。"
- "我先按你给的日期抓取当天 `cs.CV` 的全部论文，并把 title 和 abstract 保存到你指定的目录。"
- "原始列表已经保存，我现在开始先看 title，再对不确定的论文看 abstract 做主题筛选。"
- "筛出的候选论文已经下载 PDF，我现在读提取出来的全文文本，再给你每篇的核心内容总结。"
- "第 1 天的结果已经保存，我现在继续处理第 2 天，所有日志还会继续写到同一个输出目录。"
- "我先按天把筛出的相关论文标题和相关性分数列给你，你确认想深看哪几篇后，我再逐篇读全文分析。"

When the workflow finishes, tell the user:

- the resolved date
- how many papers were fetched
- how many candidate papers matched the topic
- where the run directory is
- where the PDFs and extracted full text are
- and a day-by-day list of matched papers with title and relevance score

When the user picks a paper for deeper reading, save the detailed analysis under the same run directory, preferably as:

- `08_user_summary.md` for a combined note
- or `08_user_summary_<arxiv_id>.md` for paper-specific notes

## Important Constraints

- The user asked for better interaction, not hardcoded replies. Base your response on the actual saved outputs.
- Prefer model-generated topic specs over the built-in fallback library. The built-in library is only a fallback when no `--topic-spec-file` is provided.
- Do not say "script path missing" without first verifying the absolute launcher path.
- If there are zero matches, still tell the user where the raw paper catalog and screening logs were saved.
- If a PDF download or text extraction fails, say so plainly and point to the saved log files.
- Final summaries should be based on full text when available, not just the title and abstract.
- Reuse cached day-level paper lists from `<output_root>/cache/arxiv_api/...` before calling the arXiv API again.
- For multi-day requests, summarize day by day rather than collapsing everything into one block.
- The first output after retrieval should be a navigable shortlist, not a long narrative. Help the user choose which papers deserve deeper reading.
- In second-stage paper analysis, be concrete and evidence-based. Avoid generic summaries that could apply to any paper.
- For paper shortlists, avoid markdown tables by default. Use day-grouped numbered entries that read well on mobile screens.
