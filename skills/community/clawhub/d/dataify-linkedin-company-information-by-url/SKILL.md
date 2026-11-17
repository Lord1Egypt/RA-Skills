---
name: "dataify-linkedin-company-information-by-url"
description: "Collect structured LinkedIn company information from one or more known company URLs. Do not use for personal profiles, jobs, or Crunchbase URLs."
---

# Dataify Builder Skill

Use this skill to prepare Dataify builder requests for the scraper family rooted at `linkedin_company_information_by-url` on `linkedin.com`.


## Quick Start

**Input:** a LinkedIn company URL.

```bash
python3 scripts/build-dataify-request.py --tool-sign linkedin_company_information_by-url --params-json '[{"url":"https://www.linkedin.com/company/openai"}]'
```

This submits the task, waits for completion, downloads the final result, and returns it. Add `--no-wait` only when submission-only behavior is requested.
## Workflow

1. Check whether `DATAIFY_API_TOKEN` exists in the environment.
2. If the token is missing, stop and tell the user: `Dataify requires an API token. New accounts get 50 free credits, enough for about 6,000 trial results, valid for 7 days, and only successful requests are billed. Once registration is complete, tell me and I'll continue the current task.`.
3. Ask the user to choose exactly one tool from the following Chinese list:
- 通过URL采集 (linkedin_company_information_by-url)
- 通过职位列表URL采集 (linkedin_job_listings_information_by-job-listing-url)
- 通过职位URL采集 (linkedin_job_listings_information_by-job-url)
- 通过关键词采集 (linkedin_job_listings_information_by-keyword)
4. Read `references/tool-params.json` and find the chosen tool by `tool_sign` or Chinese tool name.
5. For each parameter in the chosen tool:
   - If `input_mode` is `user_input`, ask the user for the value.
   - If `input_mode` is `select`, present the saved options to the user.
6. Use `scripts/build-dataify-request.py` as the default cross-platform helper.
7. Use `scripts/build-dataify-request.ps1` as the Windows PowerShell helper when needed.
8. When a selectable parameter has a human-readable Chinese label, keep that label in `spider_parameters`. Do not replace it with a code such as `HK` unless the user explicitly asks for the coded value.
9. Build `spider_parameters` as a JSON array.
10. If every parameter has only one final value, build one object such as `[{"searchurl":"...","country":"Hong Kong"}]`.
11. If one or more parameters have multiple aligned values, zip them by index and build one object per row. Example: `[{"search_url":"url1","page_turning":"1","max_num":"15"},{"search_url":"url2","page_turning":"1","max_num":"15"}]`.
12. If a parameter has one value while another parameter has multiple values, reuse the single value across every generated row.
13. Set `spider_name` to `linkedin.com`.
14. Set `spider_id` to the selected tool's `tool_sign`.
15. Always include `spider_errors=true` and `file_name={{TasksID}}`.
16. Return a curl command for `https://scraperapi.dataify.com/builder`.

## Set DATAIFY_API_TOKEN

Prefer a permanent environment-variable setup instead of setting the token only for the current terminal session.

Windows PowerShell, permanent for the current user:
```powershell
[Environment]::SetEnvironmentVariable("DATAIFY_API_TOKEN", "your_token_here", "User")
```

Then reopen PowerShell. If the current session also needs the token immediately, run:
```powershell
$env:DATAIFY_API_TOKEN = "your_token_here"
```

macOS or Linux, permanent for bash:
```bash
echo 'export DATAIFY_API_TOKEN="your_token_here"' >> ~/.bashrc
source ~/.bashrc
```

macOS or Linux, permanent for zsh:
```bash
echo 'export DATAIFY_API_TOKEN="your_token_here"' >> ~/.zshrc
source ~/.zshrc
```

## Script usage

Python:
```bash
python scripts/build-dataify-request.py --tool-sign <selected_tool_sign> --values-file values.json
```

PowerShell:
```powershell
& ".\scripts\build-dataify-request.ps1" -ToolSign "<selected_tool_sign>" -ValuesFile ".\values.json"
```

The `values.json` file should contain either one object or an array of objects. Example:
```json
[{"searchurl":"https://www.airbnb.com/s/Greece/homes?...","country":"Hong Kong"}]
```

## Required output shape

Generate a curl command in this form:

```bash
curl -X POST 'https://scraperapi.dataify.com/builder' \
  -H "Authorization: Bearer $DATAIFY_API_TOKEN" \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'spider_name=linkedin.com' \
  -d 'spider_id=<selected_tool_sign>' \
  -d 'spider_parameters=[{"param":"value"}]' \
  -d 'spider_errors=true' \
  -d 'file_name={{TasksID}}'
```

## Reference usage

- `references/tool-params.json` stores the full saved parameter catalog for every available tool in this scraper family.
- `scripts/build-dataify-request.py` is the portable implementation and should be preferred.
- `scripts/build-dataify-request.ps1` mirrors the same behavior for Windows users.
- If a parameter has no options, the user must provide the value.
- Do not assume `spider_parameters` always contains exactly one object. Multi-value tools may require multiple objects zipped by index.
- Use the saved `url_example` only as a reference example. Do not assume the user wants the example values unless they explicitly confirm them.

## Default completion behavior

The default deliverable is the collected result, not only a `task_id`.

1. Submit the Builder task once and capture its `task_id`.
2. Immediately continue with `$dataify-task-operations` and monitor the same task ID.
   - Use the default 600-second wait for ordinary collections.
   - Use `--timeout 1800` for media downloads or clearly high-volume, multi-page, or multi-input collections.
3. When the task succeeds, download and return the final JSON result. Summarize large payloads while preserving access to the raw result.
4. If monitoring times out or is interrupted, return the task ID and a resume command. Do not resubmit the paid task.
5. Stop after submission only when the user explicitly asks for submission only, a task ID, or `--no-wait` behavior.

## Parameter interaction policy

- For a clear, low-risk, read-only, and low-cost request, apply safe defaults and execute immediately. A short execution summary is optional; do not pause for confirmation.
- Ask only for a missing required input, a material ambiguity, a high-volume or multi-page scope, a media download, a choice that materially changes credit usage, an irreversible action, or an explicit user request to review parameters.
- When confirmation is required, show only user-facing values that affect the target, scope, output, or cost. Prefer one concise sentence; use a compact table only when three or more consequential values are easier to compare.
- Never show fixed fields, empty optional fields, unchanged defaults, credentials, or internal implementation parameters such as engine selectors, response-format flags, offsets, spider IDs, and file-name templates.
- Keep advanced filters hidden unless the user asks for them or they are needed to resolve ambiguity. Never substitute documentation example values for missing required user input.
- After returning results, offer relevant refinements instead of forcing all optional decisions before the first result.

## Account CTA policy

- Show a prominent Dataify account CTA only when the API token is missing, rejected/invalid, or the account has insufficient credits.
- For a missing token, offer https://dashboard.dataify.com/login?utm_source=skill and state: New accounts get 50 free credits, enough for about 6,000 trial results, valid for 7 days, and only successful requests are billed. Never ask the user to paste the token into chat.
- Detect the current operating system and shell. Show only the matching session-scoped setup command first (`export` for macOS/Linux shells, `$env:` for Windows PowerShell, or `set` for Windows Command Prompt). Show other platforms or persistent setup only when detection is ambiguous or the user asks.
- After the user says the token is configured, verify only whether `DATAIFY_API_TOKEN` is present; never print its value. If verification succeeds, continue the original task without asking the user to repeat it.
- Explain that persistent shell changes may require a new terminal or restarting the agent application. Do not recommend a project `.env` unless the execution path explicitly loads it, and ensure `.env` is ignored by version control.
- For an invalid token, direct the user to API-key management without implying that a new registration is required. For insufficient credits, direct the user to balance or recharge management.
- During normal submission, processing, and successful completion, do not promote registration or the Dashboard. Never expose the token or include it in CTA attribution parameters.
