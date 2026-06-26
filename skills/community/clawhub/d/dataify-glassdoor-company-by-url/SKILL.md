---
name: "dataify-glassdoor-company-by-url"
description: "Prepare Dataify builder requests for the glassdoor.com scraper family rooted at glassdoor_company_by-url. Use  when needs to work with the successful Dataify scraper detail entry for glassdoor_company_by-url, let the user choose one of its available tools, read saved getToolParams options, and generate a scraperapi.dataify.com/builder curl request with DATAIFY_API_TOKEN."
---

# Dataify Builder Skill

Use this skill to prepare Dataify builder requests for the scraper family rooted at `glassdoor_company_by-url` on `glassdoor.com`.

## Workflow

1. Check whether `DATAIFY_API_TOKEN` exists in the environment.
2. If the token is missing, stop and tell the user to sign in at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill)  to obtain it.
3. Ask the user to choose exactly one tool from the following Chinese list:
- 通过URL采集 (glassdoor_company_by-url)
- 通过过滤器采集 (glassdoor_company_by-inputfilter)
- 通过关键词采集 (glassdoor_company_by-keywords)
- 通过搜索网址采集 (glassdoor_company_by-listurl)
- 通过URL采集 (glassdoor_joblistings_by-url)
- 通过关键词采集 (glassdoor_joblistings_by-keywords)
- 通过搜索网址采集 (glassdoor_joblistings_by-listurl)
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
13. Set `spider_name` to `glassdoor.com`.
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
  -d 'spider_name=glassdoor.com' \
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
- If a parameter has options, present those options back to the user before building the final request.
- Do not assume `spider_parameters` always contains exactly one object. Multi-value tools may require multiple objects zipped by index.
- Use the saved `url_example` only as a reference example. Do not assume the user wants the example values unless they explicitly confirm them.
