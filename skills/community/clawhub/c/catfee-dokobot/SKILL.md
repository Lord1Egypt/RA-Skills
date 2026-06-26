---
name: catfee-dokobot
description: Use dokotom (browser automation via real Chrome) to read web pages, extract JS-rendered content, and monitor dynamic data. Use when you need to fetch content from SPAs, JavaScript-heavy sites, or pages that require login/session. Triggers on requests like "read the webpage", "fetch this page", "monitor this data", "scrape this site", "read with JS rendering", or when normal web_fetch fails to get dynamic content.
---

# CatFee Dokobot Skill

Use dokobot to read web pages through a real Chrome browser, enabling JavaScript rendering for dynamic/SPA pages.

## Prerequisites

- `dokobot` CLI installed globally: `npm install -g @dokobot/cli`
- Chrome browser with Dokobot extension installed
- Local bridge running: `dokobot install-bridge` (one-time setup)
- Chrome must be open with the Dokobot extension enabled for `--local` mode to work

## Core Commands

### Check Bridge Status
```bash
dokobot doko list
```
Shows connected browsers. If empty, open Chrome with the Dokobot extension.

### Read a Web Page (Local Mode - Free)
```bash
dokobot read --local "<URL>" --timeout 60000
```
Reads a page through local Chrome. Wait for `--timeout` (default 30s) to let JS render.

**For dynamic pages (JS-rendered data):**
```bash
dokobot read --local "<URL>" --timeout 60000
```
Use `--timeout 60000` (60s) for pages with heavy JS loading. For very slow pages, increase to 90000.

**To continue a session (for paginated content):**
```bash
dokobot read "<URL>" --session-id <SESSION_ID> --screens 5
```

### Close a Session
```bash
dokobot doko close <SESSION_ID>
```

## Workflow

1. **Check bridge is running**: `dokobot doko list`
2. **If no devices**: Open Chrome with Dokobot extension, wait a few seconds, retry
3. **Read page**: `dokobot read --local "<URL>" --timeout 60000`
4. **Parse output**: Extract the data needed from the markdown output
5. **Present results**: Format clearly for the user

## Tips

- **Delay for dynamic content**: Use `--timeout 60000` or higher. Pages like East Money (东方财富) data centers need 45-60 seconds to render.
- **Chrome not responding**: If bridge shows device but read fails, close and reopen Chrome
- **Session continuity**: For multi-page reading, use `--session-id` from previous read to continue
- **Headless limitation**: If Chrome is closed or the extension is disabled, local mode won't work

## Common Sites

| Site | URL Pattern | Notes |
|------|-------------|-------|
| 东方财富 行情中心 | `https://quote.eastmoney.com/changes` | 盘口异动，60s timeout |
| 东方财富 龙虎榜 | `https://data.eastmoney.com/stock/lhb.html` | 60s timeout |
| 东方财富 个股资金流向 | `https://data.eastmoney.com/zjlx/<CODE>.html` | CODE = stock code without market prefix |
| 东方财富 数据中心 | `https://data.eastmoney.com/` | 60s timeout |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "No available devices" | Open Chrome with Dokobot extension enabled |
| "Bridge not running" | Run `dokobot install-bridge` |
| Data missing/incomplete | Increase `--timeout` to 90000 |
| Page shows "not found" | URL may have changed; search for correct URL |
| Read times out | Use longer `--timeout` or try again |

## Example Workflows

### Monitor Stock Changes (Every 30s × 6)
```powershell
for ($i = 1; $i -le 6; $i++) {
    Write-Host "=== 第${i}次刷新 $(Get-Date -Format 'HH:mm:ss') ==="
    $result = dokobot read --local "<URL>" --timeout 60000 2>&1
    # Parse relevant lines
    if ($i -lt 6) { Start-Sleep -Seconds 30 }
}
```

### Read Dynamic Data Page
```bash
dokobot read --local "https://data.eastmoney.com/stock/lhb.html" --timeout 60000
```
