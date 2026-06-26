---
name: cde-monitor
description: Query CDE China drug review public data for breakthrough therapy announcements, priority review announcements, included lists by company or drug, in-review registration lookups by company or drug, and acceptance-number review status lookups.
homepage: https://www.cde.org.cn
metadata: {"openclaw":{"emoji":"💊","homepage":"https://www.cde.org.cn","requires":{"anyBins":["python","python3","py"]},"os":["win32","linux"]}}
---

# CDE Monitor

Use this skill when the user needs live information from the China Center for Drug Evaluation site and the answer depends on current CDE public listings rather than static knowledge.

This skill should also activate when the user uses a clear trigger phrase such as `CDE 药物信息查询`, `查询 CDE 药物信息`, `cde drugs query`, or `CDE drug query`, even if the user has not yet provided a concrete company name, drug name, or query type.

When the user only provides a trigger phrase or a vague request, do not run a query immediately. First introduce the skill's capabilities in a short overview, then guide the user to choose one of the supported query types and provide the exact company name or drug name when needed.

## Quick Start

```bash
# List current breakthrough therapy announcements
python {baseDir}/scripts/cde_query.py breakthrough-announcements --pretty

# Find breakthrough included records for a company
python {baseDir}/scripts/cde_query.py breakthrough-included-by-company --company "示例公司" --pretty

# Find priority review included records for a drug
python {baseDir}/scripts/cde_query.py priority-included-by-drug --drug "示例药品" --pretty

# Query in-review catalog records across 2016 to 2026
python {baseDir}/scripts/cde_query.py in-review-by-company --company "示例公司" --years 2016 2017 2018 2019 2020 2021 2022 2023 2024 2025 2026 --pretty

# Query review task status by acceptance number
python {baseDir}/scripts/cde_query.py review-status-by-acceptance-no --acceptance-no "CYSB2600096" --pretty
```

Use `--show-browser` when the CDE page flow needs visible debugging. Omit `--pretty` when you want raw JSON output for downstream processing.

## Conversation Opening

If this skill is activated by a generic trigger such as `CDE 药物信息查询` or `cde drugs query`, start with a short capability summary before asking for input.

Match the conversation language to the user's language. If the user asks in Chinese, reply in Chinese. If the user asks in English, reply in English. Keep the language choice consistent across the introduction, clarification questions, and final results unless the user explicitly switches languages.

Do not reuse the Chinese opening when the user starts in English. If the trigger phrase or the user's request is in English, the first capability summary and the follow-up question must also be in English.

Recommended opening pattern for Chinese:

```md
我可以帮助你查询 CDE 公开药品审评信息，当前支持：

- 拟突破性治疗品种公示
- 纳入突破性治疗品种名单，按企业或药品查询
- 拟优先审评品种公示
- 纳入优先审评品种名单，按企业或药品查询
- 在审品种目录浏览，按企业或药品查询，支持年份 2016 到 2026
- 按受理号查询申请基础信息和评审状态

请告诉我你要查哪一类信息。
如果是按企业或药品查询，请尽量提供准确的企业全称或药品名称。
如果是按受理号查询，请提供完整受理号。
```

Recommended opening pattern for English:

```md
I can help you query public CDE drug review information. I currently support:

- Breakthrough therapy announcements
- Included breakthrough therapy lists, searchable by company or drug
- Priority review announcements
- Included priority review lists, searchable by company or drug
- In-review registration catalog lookups by company or drug for years 2016 through 2026
- Acceptance-number lookups for application basic info and review task status

Tell me which type of CDE information you want to check.
If you want a company-specific or drug-specific lookup, please provide the exact company name or drug name whenever possible.
If you want an acceptance-number lookup, please provide the full acceptance number.
```

If the user then chooses a company-specific or drug-specific query, confirm the exact company or drug name when the provided string could be ambiguous, abbreviated, or misspelled.
If the user chooses an acceptance-number lookup, confirm the acceptance number only when it appears incomplete, malformed, or ambiguous.

## Data Sources

| Source | URL | Data used by this skill |
| --- | --- | --- |
| CDE 信息公开入口 | https://www.cde.org.cn/main/xxgk/listpage/9f9c74c73e0f8f56a8bfbc646055026d | Entry page for all supported public query flows |
| 突破性治疗公示 | https://www.cde.org.cn/main/xxgk/listpage/9f9c74c73e0f8f56a8bfbc646055026d | 拟突破性治疗品种 and 纳入突破性治疗品种名单 |
| 优先审评公示 | https://www.cde.org.cn/main/xxgk/listpage/9f9c74c73e0f8f56a8bfbc646055026d | 拟优先审评品种公示 and 纳入优先审评品种名单 |
| 受理品种信息 | https://www.cde.org.cn/main/xxgk/listpage/9f9c74c73e0f8f56a8bfbc646055026d | 在审品种目录浏览 across the requested years |
| 审评任务公示 | https://www.cde.org.cn/main/xxgk/listpage/369ac7cfeb67c6000c33f85e6f374044 | 新报任务公示 review task lookup used by acceptance-number status queries |

This skill uses Selenium to drive the public CDE site and read the rendered listing data after the page JavaScript finishes loading. It does not rely on static local datasets. Results reflect the public CDE pages available at query time.

## Environment Requirements

Required:

- Python 3.10 or newer.
- Google Chrome or Chromium installed locally.
- Network access to https://www.cde.org.cn.
- Python packages from `scripts/requirements.txt`.

Install on Windows:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r .\scripts\requirements.txt
```

Install on Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r ./scripts/requirements.txt
```

OpenClaw only needs a working Python launcher on the machine. Chrome itself does not need to be on `PATH`, but Selenium must be able to launch a local Chrome or Chromium browser.

For `in-review-by-company` and `in-review-by-drug`, the supported year range is limited to 2016 through 2026. If the user passes any year outside that range, the CLI should return a clear validation error.

## Use Cases

- Breakthrough therapy: list drugs currently in 拟突破性治疗品种 announcements.
- Breakthrough therapy: find which drugs from a company are already in 纳入突破性治疗品种名单.
- Breakthrough therapy: find whether a drug appears in 纳入突破性治疗品种名单.
- Priority review: list drugs currently in 拟优先审评品种公示 announcements.
- Priority review: find which drugs from a company are already in 纳入优先审评品种名单.
- Priority review: find whether a drug appears in 纳入优先审评品种名单.
- In-review catalog: find CDE registration items for a company across years 2016 to 2026.
- In-review catalog: find CDE registration items for a drug across years 2016 to 2026.
- Acceptance number lookup: find the application basic info first, then locate the review task status and professional-stage lamp states.

## Name Confirmation Rule

For company-specific or drug-specific lookups, first confirm the exact company or drug name if the user input could be ambiguous, abbreviated, or misspelled. CDE matching is strict. If the user already provided a precise name and there is no ambiguity, proceed directly.

## Command Surface

Run the Python CLI from this skill directory.

```bash
python {baseDir}/scripts/cde_query.py breakthrough-announcements
python {baseDir}/scripts/cde_query.py breakthrough-included-by-company --company "<公司名>"
python {baseDir}/scripts/cde_query.py breakthrough-included-by-drug --drug "<药品名>"
python {baseDir}/scripts/cde_query.py priority-announcements
python {baseDir}/scripts/cde_query.py priority-included-by-company --company "<公司名>"
python {baseDir}/scripts/cde_query.py priority-included-by-drug --drug "<药品名>"
python {baseDir}/scripts/cde_query.py in-review-by-company --company "<公司名>" --years 2016 2017 2018 2019 2020 2021 2022 2023 2024 2025 2026
python {baseDir}/scripts/cde_query.py in-review-by-drug --drug "<药品名>" --years 2016 2017 2018 2019 2020 2021 2022 2023 2024 2025 2026
python {baseDir}/scripts/cde_query.py review-status-by-acceptance-no --acceptance-no "<受理号>"
```

Add `--show-browser` when you need visible browser debugging. JSON is the default output. Use `--pretty` only when you want a human-readable terminal summary during debugging. Use `--max-pages <n>` only for debugging or validation; omit it for the full production query.

## Response Handling

- Read `records` for the merged deduplicated results.
- Use each record's `normalized` object for answering. It exposes stable keys such as `drug_name`, `company_name`, `acceptance_no`, `publication_title`, `year`, `source_menu`, and `source_tab`.
- Use `metadata.total_records`, `metadata.pages_visited`, `metadata.years_queried`, and `metadata.applied_filters` to summarize scope.
- The final user-facing answer should be a Markdown table whenever records are returned.
- Prefer a compact table with columns such as `药品名称`, `企业名称`, `受理号`, and `年份`. Add a short summary line above the table for `total_records`, `pages_visited`, and the applied filters when helpful.
- If the command returns no records, tell the user that no matching public CDE entries were found for the confirmed query.
- For `review-status-by-acceptance-no`, read `basic_info_found`, `review_status_found`, `basic_info`, `review_status`, and `attempts` instead of `records`.
- For `review-status-by-acceptance-no`, the acceptance number's inferred year must currently fall within the CDE page's supported year range of 2016 through 2026.
- For `review-status-by-acceptance-no`, summarize the first-step basic info using fields such as `drug_name`, `drug_type`, `application_type`, and `acceptance_no`.
- For `review-status-by-acceptance-no`, when `review_status_found` is true, summarize `review_state`, `entered_center_at`, and each professional-stage lamp status from `review_status.stages`.
- For `review-status-by-acceptance-no`, when `basic_info_found` is true but `review_status_found` is false, tell the user that the application basic info was found but no matching public review-task status is currently shown on the CDE page.

## Failure Handling

- If Python or Selenium is missing, load [setup](./references/setup.md).
- If `review-status-by-acceptance-no` infers a year outside 2016 through 2026, report that the acceptance number's inferred year is outside the current CDE page query range.
- If the site structure changes or the query fails, report that the live CDE page could not be parsed reliably and include the command error summary.
- Do not invent results when the command fails.

## References

- [Setup](./references/setup.md)
- [Queries](./references/queries.md)
- [Development guide](./references/development-guide.md)
- [Publish checklist](./references/publish-checklist.md)

## Troubleshooting

- If Python or Selenium is missing, follow the install commands in [Setup](./references/setup.md).
- If Chrome or Chromium does not launch, verify that the browser is installed locally and can be opened manually on the same machine.
- If a query returns no expected records, first confirm the exact company name or drug name. CDE matching is strict.
- If the visible page flow or results change unexpectedly, rerun with `--show-browser` to inspect the live CDE page behavior.
- If the CDE page structure has changed, update the selector and parsing logic in `scripts/cde_client.py` before relying on the result.
