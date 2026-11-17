---
name: exceldashboard-report
description: Prepare verified analytical outlines and create or track visual reports through ExcelDashboard AI MCP. Use when users request an ExcelDashboard AI report from Excel, CSV, verified metrics, or a research topic, or ask to track an existing report job.
---

# ExcelDashboard AI Reports

Use the current client's file-reading, computation, and web-search capabilities to complete the analysis. ExcelDashboard AI generates reports from the resulting outline. This Skill orchestrates only two MCP tools: `create_report` and `get_report`.

The official connection guide is https://www.exceldashboard.ai/mcp and the Streamable HTTP endpoint is https://api.exceldashboard.ai/mcp. Installing these instructions does not configure MCP or complete browser OAuth. Discover the two tools on the authorized ExcelDashboard AI connection before calling them; reading documentation is not proof of connection.

These instructions are written in English. User-facing replies and report content should follow the user's requested language; the instruction language does not require English report content.

## Tool Contract

| Tool | Parameters | Result |
| --- | --- | --- |
| `create_report` | Required `outline`: a nonempty Markdown string following the outline reference. Optional `locale`: a string, default `zh-CN`. | `job_id`, `status: "running"`, `report_url`, and `poll_after_seconds`. |
| `get_report` | Required `job_id`: the string returned by creation. | `status`, `stage`, page counts, `report_url`, and completion or failure details. |

Create using `{"outline":"<complete Markdown following references/outline-format.md>","locale":"en"}`. The outline text in this example is a placeholder: replace it with the complete analyzed report outline. Query using `{"job_id":"<returned job_id>"}` and replace the placeholder with the actual returned value.

A creation result has the form `{"job_id":"<job UUID>","status":"running","report_url":"<actual preview URL>","poll_after_seconds":15}`. Status results also include `operation`, `stage`, `completed_pages`, `pages_started`, `total_pages`, `report_id`, `share_url`, `error_code`, and `error_message`; some values can be null. `poll_after_seconds` is null after the job ends. Only `completed` proves success; `failed` ends tracking with an error. Do not call an editing tool: none is exposed by this connector.

Invalid parameters return a tool error with `error_code: "INVALID_ARGUMENT"` and `message`. Correct the parameters before retrying. After a creation timeout, use the known job ID if one was returned; if no ID was received, explain that submission is uncertain and ask before creating another job.

## Analysis and Outline

1. Determine the audience, business question, time range, metrics, grouping, and intended decision from the user's goal. Ask when an essential metric definition is missing; make explicit assumptions for other details when supported by the files. If the user requests analysis only, deliver the analysis without calling the report creation tool.
2. Read user-uploaded files through the current client. Check field meanings, record grain, time ranges, units, missing values, and duplicates. Use available computation tools for aggregation, comparisons, trends, and relevant group analysis. Verify the baseline, denominator, and sample scope for year-over-year or period-over-period calculations. Search the web only when external context is needed, and record sources and dates. Explain data limitations rather than inventing values or causes.
3. Build a narrative from question and definitions to key findings, evidence and possible causes, and recommendations. Include verified metrics, units, time ranges, and aggregated chart data in `outline`; do not upload raw detail files. Put sources, definitions, and uncertainty on the relevant outline pages. No separate `evidence` field is needed.
4. Before creating a report, write the complete outline according to [references/outline-format.md](references/outline-format.md) and check its format, numbers, and charts. The report name is extracted automatically from the outline's `# Main title`. Briefly explain the analysis approach and planned report if useful. When the user has already requested report creation, do not add a separate outline approval step.

## Creation and Tracking

1. Use the workspace selected on the OAuth consent page for the current connection. Tool calls do not require `workspace_id`. If the connection is unauthorized, ask the user to connect ExcelDashboard AI in the client and select a workspace. Switching workspaces requires authorization again. Do not ask users to send tokens or workspace IDs in the conversation.
2. Call `create_report` with the complete `outline` and, when needed, `locale` (default: `zh-CN`). Each call submits a new job; do not automatically retry creation. Save the returned `job_id` and immediately show the returned `report_url` as a "View report" link. If a callable built-in browser tool is available, open this URL before the first `get_report` call and save the tab identifier; do not wait until completion to open it. If no such tool exists or opening fails, explain this and continue tracking the job. ExcelDashboard AI automatically creates a public read-only share when generation completes; users do not need to share manually in the frontend. The preview's Edit button separately verifies the signed-in account and editing permissions.
3. Query status with `get_report({"job_id":"..."})`. Within the client's available execution time, poll serially using the returned `poll_after_seconds`, or approximately 15 seconds if absent. Do not query the same job concurrently. Report actual progress using `stage`, `completed_pages`, `pages_started`, and `total_pages`; do not invent percentages. After every `get_report` result, update the user-visible progress and refresh the same built-in browser tab, keeping the returned preview link in the update. If the client cannot keep waiting, give the user the `job_id` and preview link. The page updates its own progress; resume by querying the existing job next time rather than creating the same report again.
4. Check `status` and `report_url` after each `get_report` result. When `status` is `completed`, stop polling immediately, present the link using the rules below. Do not continue saying that report generation is pending. When `status` is `failed`, explain `error_code` and `error_message`; submit a new job only if regeneration is needed after the cause has been addressed. Status queries do not modify the job.

## Presenting Reports in the Client

- Show the report entry point in a user-visible reply in WorkBuddy or another client. Do not leave the link only in tool results, internal reasoning, or JSON.
- Apply the same presentation rules at creation, during generation, and after completion. Consistently display the returned `report_url` as a "View report" link. Do not replace the original preview entry point with `share_url`, generated HTML, or a local file after completion.
- After creation, discover and use the built-in browser or web-preview tools actually available in the current client to open the returned `report_url` in the results area. Save the tab or page identifier after the first successful open. Refresh or update that same page after every `get_report` result, including completion. Do not repeatedly create tabs or substitute system-browser commands.
- Open and refresh internally only when the client provides the required tools. Follow their actual schemas; do not invent tool names or private URL schemes. If no callable built-in browser tool exists or execution fails, explain this and retain a clickable link. WorkBuddy users can right-click the link and choose the option to open it internally, or set Settings > General > Link opening behavior to always use the built-in browser. These settings determine where clicked links open; they do not let MCP automatically open tabs.
- The page automatically updates generated report content every 5 seconds, independently of Agent polling. It shows a waiting message before the first page is generated. Do not describe a running report as completed.
- Prefer `report_url`, which includes the editing entry point. `share_url` is the underlying read-only `/share/iframe/<share_id>?b=report` share address; provide it separately only when the user requests sharing or embedding. Use the exact returned URL without inserting spaces or rewriting it.
- When `get_report` returns a nonempty HTTP/HTTPS `report_url`, use the original returned URL in a Markdown link. At completion, reply with the equivalent of `Report generated: [View report](actual report_url)` in the user's language. If the report title is known, it may be used as the link label. `actual report_url` is an explanatory placeholder and must be replaced with the real returned URL.
- If the backend returns a valid `report_url` during generation, include `[View report](actual report_url)` in progress updates and state that generation is still in progress. Claim completion only when `status` is `completed`; the existence of a link does not prove completion.
- If `report_url` is empty, show only actual progress. Do not construct a link from `job_id`, `report_id`, or a domain. If the job has completed without a link, explain that the report is complete but the service did not return an opening link, retain the job ID for investigation, and stop waiting for generation.
- Claim that the report has opened inside the client only after actually calling the built-in browser tool and confirming success. If no call was made or it failed, provide the clickable entry point and explain that the user needs to open it; do not claim automatic display.

## Editing Through the Frontend

MCP does not provide a report editing tool. If the user requests changes to an existing report, provide its returned `report_url` and direct them to the preview's Edit button. The frontend verifies the signed-in account and editing permissions before opening the editor. Do not invent an editing tool or silently create a replacement report. Create a new report only when the user requests a separate report.

## Error Recovery

- `NOT_FOUND`: distinguish `job_id` from `report_id`, then check the current user's access and workspace permissions.
- Authorization failure: guide the user to reconnect ExcelDashboard AI in the current client. Do not request or display tokens.
- Job failure or timeout: query the existing `job_id` first to confirm its final status. Submit a new creation job only after failure is confirmed and its cause has been addressed.
