---
name: cpbl
description: Query CPBL 中華職棒 scores schedules live games standings player stats news and Taiwan baseball history for Taiwan users Use when the user asks about CPBL 戰績 賽程 即時比分 球員數據 排行榜 新聞 年度獎項 二軍 熱身賽 總冠軍賽 or historical CPBL facts
metadata:
  openclaw:
    emoji: ⚾
    requires:
      bins:
        - uv
      anyBins:
        - python3
    clawhub:
      link: https://clawhub.ai/ichendong/cpbl
---

# CPBL

Use the bundled scripts for official-site data first.
Use `web_search` for recent news.
Use Scrapling `StealthyFetcher` for 台灣棒球維基館 (awards history, player career data) — the site uses Anubis protection that blocks standard fetch tools, but Scrapling's stealth browser can access it.
Do NOT use `web_fetch` or Playwright for twbsball — they will be blocked by Anubis.

## Primary workflow

1. Pick the narrowest script that matches the request.
2. Prefer text output for user-facing answers and JSON output for chaining or debugging.
3. If the official source cannot provide the requested historical fact, use Scrapling `StealthyFetcher` to fetch 台灣棒球維基館.
4. If a result looks empty or partial, check `references/api-endpoints.md` before assuming the data does not exist.

## Script map

- `scripts/cpbl_live.py`  即時比分 今日賽況 指定日期賽況
- `scripts/cpbl_games.py`  已完賽結果 歷史比賽
- `scripts/cpbl_schedule.py`  賽程
- `scripts/cpbl_standings.py`  戰績 排名
- `scripts/cpbl_stats.py`  球員與排行榜數據

## Common commands

```bash
uv run skills/cpbl/scripts/cpbl_live.py --output text
uv run skills/cpbl/scripts/cpbl_live.py --date 2026-04-01 --team 兄弟
uv run skills/cpbl/scripts/cpbl_games.py --year 2025 --limit 10
uv run skills/cpbl/scripts/cpbl_schedule.py --month 2026-04 --all
uv run skills/cpbl/scripts/cpbl_standings.py
uv run skills/cpbl/scripts/cpbl_stats.py --year 2025 --category batting --top 10
```

## Game type codes

- `A` 一軍例行賽 預設
- `B` 一軍明星賽
- `C` 一軍總冠軍賽
- `D` 二軍例行賽
- `E` 一軍季後挑戰賽
- `F` 二軍總冠軍賽
- `G` 一軍熱身賽
- `H` 未來之星邀請賽
- `X` 國際交流賽

## Live score notes

- Live data is polled from the official source and is not push-based.
- API data may lag by a few minutes.
- When `PresentStatus` shows "比賽中" but `/box/getlive` returns `GameStatus=3`, the script corrects the status to "已結束" automatically.
- Finished games now include detailed Box Score: pitcher lines (IP/H/ER/K/BB/HR/H/SV/speed) and key batter lines (AB/H/RBI/HR/R/SB).
- Game duration is displayed in `Xh Xm` format (e.g. 3h23m).
- Monday often has no games unless adjusted by holidays or makeup scheduling.

## Schedule cache

If a request is about schedule, check `memory/cpbl_schedule_YYYY.md` first.
Refresh the cache when the file is missing, stale, or the requested range extends beyond the cached range.

Recommended refresh command

```bash
uv run skills/cpbl/scripts/cpbl_schedule.py --month YYYY-MM --all
```

## Postponement info

To check today's postponement announcements, fetch the official news page:
```
https://cpbl.com.tw/news
```
Look for the latest "延賽公告" entry. The live script now auto-detects postponed games (0:0 + no winning/losing pitcher).

## History and awards

台灣棒球維基館 (twbsball) 自 2026-05 起啟用 Anubis v1.25.0 防護機制。
`web_fetch`、`tavily_extract`、Playwright 無法存取該站。
**使用 Scrapling `StealthyFetcher` 可以正常存取（已驗證）。**

### 查詢維基館的方法（優先順序）

1. **Scrapling StealthyFetcher** — 使用 CPBL venv 裡的 `scrapling` 直接抓取維基館頁面（已驗證可用）
2. `web_search` / `tavily_search` — 搜尋引擎快照
3. 維基百科 (zh.wikipedia.org)
4. 請使用者手動查詢

### Scrapling 查詢維基館

使用 `skills/cpbl/.venv` 裡的 scrapling，**不要用 `web_fetch` 或 Playwright**。

**安裝（首次使用前）：**
```bash
# 1. 建立 venv 並安裝依賴（如果 .venv 不存在）
cd skills/cpbl && uv venv && uv pip install -e .
# 2. 安裝 stealth browser（Scrapling StealthyFetcher 需要）
.venv/bin/scrapling install --force
```

```python
from scrapling.fetchers import StealthyFetcher

page = StealthyFetcher.fetch(
    "https://twbsball.dils.tku.edu.tw/wiki/index.php?title=中華職棒年度最有價值球員",
    headless=True,
    wait=10000,
)
text = page.css("#mw-content-text")[0].get_all_text()
print(text)
```

CLI 替代方案（適合一次性查詢，需先執行安裝步驟 2）：
```bash
skills/cpbl/.venv/bin/scrapling extract stealthy-fetch \
  "https://twbsball.dils.tku.edu.tw/wiki/index.php?title=中華職棒年度最有價值球員" \
  result.md --ai-targeted --wait 10000
```

注意事項：
- `wait=10000` (毫秒) 讓 Anubis PoW 挑戰完成，頁面載入後才抓
- headless=True 即可，不需 headful
- 啟動較慢（要啟動 stealth browser），約需 10-15 秒
- 如果要查多個頁面，使用 `StealthySession` 複用同一個 browser 實例：

```python
from scrapling.fetchers import StealthySession

with StealthySession(headless=True) as session:
    page1 = session.fetch("https://twbsball.dils.tku.edu.tw/wiki/index.php?title=中華職棒年度最有價值球員")
    text1 = page1.css("#mw-content-text")[0].get_all_text()
    page2 = session.fetch("https://twbsball.dils.tku.edu.tw/wiki/index.php?title=中華職棒年度最佳新人獎")
    text2 = page2.css("#mw-content-text")[0].get_all_text()
```

### 常用維基館頁面

- `中華職棒年度最有價值球員` (MVP)
- `中華職棒年度最佳新人獎` (新人王)
- `球員姓名` (球員生涯資料)
- URL 格式：`https://twbsball.dils.tku.edu.tw/wiki/index.php?title=頁面標題`

## References

Read these only when needed

- `references/api-endpoints.md`  official-site endpoint behavior and quirks
- `references/summary.md`  project background and current limitations
- `references/test-report.md`  prior investigation details

## Known limits

- Some official endpoints return HTML fragments instead of JSON.
- Some standings and schedule flows are brittle because the site relies on AJAX plus CSRF.
- If a script returns partial data, do not invent missing values. State the limit and fall back to another source when possible.
- **台灣棒球維基館 (twbsball) 自 2026-05 起啟用 Anubis 防護機制。** `web_fetch`/Playwright 無法存取，使用 Scrapling `StealthyFetcher` 可以正常讀取（見上方 History and awards 段落）。