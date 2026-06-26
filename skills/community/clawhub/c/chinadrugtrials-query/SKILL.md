---
name: chinadrugtrials-query
description: Query chinadrugtrials.org.cn, the Chinese Drug Clinical Trial Registration and Information Disclosure Platform. Use when asked to search this site or retrieve Chinese clinical trial registration records for a drug, indication, company, CTR number, or keyword, especially when results must include details beyond the list page such as applicant/company, first public disclosure date, trial status, and official detail link.
metadata:
  openclaw:
    requires:
      anyBins:
        - python
        - python3
---

# ChinaDrugTrials Query

## Core Rule

Return one row per registration with these fields:

`序号 | 登记号 | 试验状态 | 药物名称 | 适应症 | 试验通俗题目 | 公司 | 首次公示日期 | 链接`

Treat `公司` as `申请人名称`. Treat `首次公示日期` as `首次公示信息日期` unless the user explicitly asks for another date field. Use official platform list/detail pages as the source whenever possible.

## Fast Path

Use this path first for normal keyword queries. It was tested against `氟比洛芬贴剂` and avoids the site's most common slow/failing routes.

If the bundled script is available, prefer running it before writing new automation. Run it from the skill directory, or substitute the script path with the resolved path to this skill's `scripts/query_chinadrugtrials.py` file:

```powershell
python .\scripts\query_chinadrugtrials.py "氟比洛芬贴剂" --format markdown
```

If the script fails because Playwright points to a missing `chrome-headless-shell.exe`, rerun with `--browser-path` set to the installed Chromium path from `p.chromium.executable_path`.

The script expects the Python `playwright` package and a Playwright-managed or explicit Chromium/Chrome executable. If those are unavailable, use the Browser plugin fallback or write equivalent browser automation from the workflow below.

1. Use a real browser automation session, preferably local Playwright with installed Chromium when available.
2. Set stdout/output encoding to UTF-8 before printing Chinese text.
3. Use a browser-like user agent.
4. Open `https://www.chinadrugtrials.org.cn/` and wait only for navigation commit if full load events hang.
5. Wait for `input[name="keywords"]`.
6. Fill the keyword as a Unicode string, not through a shell/code path that can replace Chinese characters with question marks.
7. Click the visible submit button (`button[type="submit"]` / `搜索`). Do not rely on pressing Enter.
8. Wait for URL `/clinicaltrials.searchlist.dhtml` with `wait_until="commit"`, then wait a short fixed delay such as 3-8 seconds. Do not wait forever for `domcontentloaded` or `networkidle`.
9. Verify the result count from the pagination text: `当前第 ... 页，共 ... 条记录`.
10. Extract result rows from `table tr`, reading each row's `td` text plus the first `a[onclick*=getDetail]` attributes:
    - `id` is the opaque detail id.
    - `name` is the row index / `ckm_index`.
11. For every row, construct and open the detail URL in the same browser context:
    `https://www.chinadrugtrials.org.cn/clinicaltrials.searchlistdetail.dhtml?id=<id>&ckm_index=<name>`
12. Extract `申请人名称` and `首次公示信息日期` from the detail page's visible text.
13. Output a Markdown table unless the user requested another format.

## Playwright Template

Use this as the starting point when local Playwright is available. Adjust only the keyword and optional output handling.

```python
from playwright.sync_api import sync_playwright
import json, re, sys

sys.stdout.reconfigure(encoding="utf-8")
keyword = "\u6c1f\u6bd4\u6d1b\u82ac\u8d34\u5242"  # replace safely, or assign a normal UTF-8 Python string
base = "https://www.chinadrugtrials.org.cn"
chrome = None  # or set to a local Chromium/Chrome executable path when Playwright cannot find one
ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

def pick_after_tab(text, label):
    m = re.search(re.escape(label) + r"\t([^\t\n]+)", text)
    if m:
        return m.group(1).strip()
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for i, line in enumerate(lines):
        if line == label and i + 1 < len(lines):
            return lines[i + 1]
    return ""

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        executable_path=chrome or p.chromium.executable_path,
        args=["--disable-blink-features=AutomationControlled"],
    )
    context = browser.new_context(user_agent=ua)
    page = context.new_page()
    page.goto(base + "/", wait_until="commit", timeout=60000)
    page.wait_for_selector('input[name="keywords"]', timeout=30000)
    page.locator('input[name="keywords"]').fill(keyword)
    page.locator('button[type="submit"]').click(timeout=10000)
    page.wait_for_url("**/clinicaltrials.searchlist.dhtml", wait_until="commit", timeout=60000)
    page.wait_for_timeout(5000)

    body = page.locator("body").inner_text(timeout=10000).replace("\u00a0", " ")
    rows = page.evaluate("""() => Array.from(document.querySelectorAll('table tr')).map(tr => {
      const tds = Array.from(tr.querySelectorAll('td')).map(td => td.innerText.trim().replace(/\u00a0/g, ' '));
      const a = tr.querySelector('a[onclick*=getDetail]');
      return tds.length >= 6 ? {
        seq: tds[0], reg: tds[1], status: tds[2], drug: tds[3],
        indication: tds[4], title: tds[5], id: a && a.id, idx: a && a.name
      } : null;
    }).filter(Boolean)""")

    results = []
    for row in rows:
        link = f"{base}/clinicaltrials.searchlistdetail.dhtml?id={row['id']}&ckm_index={row['idx']}"
        detail = context.new_page()
        detail.goto(link, wait_until="commit", timeout=60000)
        detail.wait_for_timeout(2500)
        text = detail.locator("body").inner_text(timeout=10000).replace("\u00a0", " ")
        row["company"] = pick_after_tab(text, "申请人名称")
        row["date"] = pick_after_tab(text, "首次公示信息日期")
        row["link"] = link
        results.append(row)
        detail.close()

    print(json.dumps({"summary": body[-120:], "rows": results}, ensure_ascii=False, indent=2))
    browser.close()
```

If Playwright raises `Executable doesn't exist ... chrome-headless-shell.exe`, get the actual browser path with:

```powershell
python -c "from playwright.sync_api import sync_playwright; p=sync_playwright().start(); print(p.chromium.executable_path); p.stop()"
```

Then pass that path as `executable_path`. Do not spend time installing browsers unless the installed path is truly absent.

## Official Detail Parsing

The detail page commonly prints the fields in a tab-delimited visible block:

```text
登记号    CTR...    试验状态    ...
申请人联系人    ...    首次公示信息日期    YYYY-MM-DD
申请人名称    ...
```

Prefer tab-aware extraction:

- `首次公示信息日期\t([^\t\n]+)`
- `申请人名称\t([^\t\n]+)`

Fallback to a next-line parser only when the tab pattern is absent.

## Known Traps

Avoid these time sinks:

- Do not start with `Invoke-WebRequest`, `curl`, or plain `requests` for the actual query. They can return TLS errors, `403`, `202`, or obfuscated anti-bot JavaScript instead of results.
- Do not treat an HTTP `202` page with `FxJzG50F...js` as search results.
- Do not rely on the in-app Browser if the page navigation repeatedly times out. Switch to local Playwright with a known Chromium executable path.
- Do not print Chinese query text through a GBK PowerShell pipeline without UTF-8 handling. If the filled input becomes replacement question marks, the site returns the latest global records, not the intended keyword results.
- Do not assume the homepage submit worked. Confirm that the result page body contains the keyword or that every extracted row matches the intended keyword/CTR.
- Do not parse the first table from the unfiltered latest-records page; always verify the pagination count and row content.
- Do not use search-engine fallbacks until the official list/detail path has failed. Fallback pages may be stale and can disagree with current official status.
- Do not click every result manually if the row exposes `id` and `name`; construct the detail URL directly and open it in the same browser context.
- Do not wait for `domcontentloaded` or `networkidle` if navigation is already committed; this site often has long-running scripts.

## Browser Plugin Fallback

If using the Codex in-app Browser:

1. Follow the Browser skill setup.
2. Keep navigation timeouts short and poll URL/title/DOM.
3. If `tab.goto()` hangs twice or the session times out before a DOM snapshot, stop using it and switch to local Playwright.
4. If the site opens but the search produces latest global records, suspect keyword encoding or submit failure.

## Fallback Sources

Use fallback sources only to fill gaps after official browser extraction fails.

Good fallback searches:

- exact `登记号` plus `首次公示信息日期`
- exact `登记号` plus `申请人名称`
- exact trial title plus `药物临床试验登记与信息公示平台`

When using fallback data, state which fields were supplemented from non-official sources.

## Output Checklist

Before finalizing:

- Confirm the official result count from the list page.
- Ensure every row has all 9 required fields.
- Preserve official Chinese status text, for example `进行中 尚未招募`, `已完成`, `主动终止`.
- Use absolute Markdown links for official detail pages.
- State the query date when useful.
- If a detail field cannot be verified, write `未核实` and briefly state the gap.
