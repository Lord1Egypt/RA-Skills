---
name: alaska-air
description: Scrape Alaska Airlines award calendar and flight data. Use when user asks about Alaska Air miles, award availability, mileage booking, or flight prices on alaskaair.com. Triggers on: "alaska air", "alaska airlines", "alaska 里程", "alaska 機票", "alaska 查票", "award calendar", "里程兌換".
allowed-tools: Bash(curl:*), Bash(python3:*), message
compatibility: macOS, Linux
metadata:
  author: Josh
  version: "4.0"
---

# Alaska Airlines Scraper

Alaska Air uses **SvelteKit SSR** — all flight/award data is embedded in the raw HTML response. **No Playwright or JS rendering needed.**

> ⚠️ 目前只支援**單程查詢**（RT=false）。來回票請分兩次查詢。

---

## ⚠️ 日期陷阱（CRITICAL — 必讀）

用戶說「2月14日」或「2/14」→ 查**整個2月**，但結果只顯示**有位子**的日期。
**絕對不能把「2/4」當「2/14」！** 日期要精確對應，`2027-02-04` ≠ `2027-02-14`。

如果用戶指定的日期沒有位子（`awardPoints: null`），明確告知：
```
❌ 2月14日 無可用里程票
✅ 本月最近有位：2月15日 (15,000 里程)
```
**不要默默換成別的日期後說「我找到了」。**

---

## 查詢多路線/多月份 → 平行 Sub-Agents（MANDATORY）

**2 個以上路線或月份，必須同時 spawn，絕不串行。**

每個 sub-agent 查完後**立刻用 message 工具發 Telegram** — 不要等其他 agent，有結果馬上發：

```
# 每個 Worker sub-agent 的任務模板：
spawn model=openrouter/anthropic/claude-haiku-4-5
allowedTools=exec,read,message

"用 alaska-air skill 查 {ORIGIN}→{DEST} {YYYY}年{MM}月里程行事曆。
查完後立刻用 message 工具把結果發給用戶（Telegram to: {chat_id}），
不要等其他查詢，有結果就馬上發。
輸出格式必須含 👉 直連 URL，每個日期一個 URL，URL 單獨一行，前後各空一行。"
```

範例：查 3 條路線 → 同時 spawn 3 個 Worker，每個跑完就各自發 Telegram，不等彼此。

---

## 單一路線查詢

### Step 1: 抓 HTML

`OD=` 填目標月份內**任何一天**即可，API 回傳整月資料。

```bash
curl -s -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36" \
  "https://www.alaskaair.com/search/calendar?O={ORIGIN}&D={DEST}&OD={YYYY-MM-01}&A=1&RT=false&RequestType=Calendar&ShoppingMethod=onlineaward&locale=en-us" \
  -o /tmp/alaska_{ORIGIN}_{DEST}_{YYYYMM}.html
```

### Step 2: 錯誤處理

抓完後先確認 HTML 是否含有效資料：

```bash
if ! grep -q 'awardPoints' /tmp/alaska_{ORIGIN}_{DEST}_{YYYYMM}.html; then
  echo "抓取失敗：HTML 不含 awardPoints，可能被封鎖或路線無效"
  exit 1
fi
```

若抓取失敗，直接回報用戶「抓取失敗，請稍後再試」，不繼續執行。

### Step 3: 提取資料（含直連 URL）

將以下內容寫入 `/tmp/parse_alaska.py`，再執行：

```python
# /tmp/parse_alaska.py
import re, json, sys

def scrape_alaska(origin, dest, yyyymm, adults=1):
    html = open(f'/tmp/alaska_{origin}_{dest}_{yyyymm}.html').read()
    pat = r'\{date:"([^"]+)",price:([\d.]+|null),awardPoints:(\d+|null),isDiscounted:(true|false),flightSegments:\[.*?\],solutionId:"([^"]*)"\}'
    results = []
    for date, price, miles, disc, sol in re.findall(pat, html):
        avail = miles != 'null'
        entry = {
            'date': date,
            'available': avail,
            'miles': int(miles) if avail else None,
            'price_usd': float(price) if avail else None,
            'discounted': disc == 'true',
        }
        if avail:
            entry['book_url'] = (
                f"https://www.alaskaair.com/search/?O={origin}&D={dest}"
                f"&D1={date}&A={adults}&RT=false&ShoppingMethod=onlineaward&locale=en-us"
            )
        results.append(entry)
    # 按日期排序（保留所有日期，含 N/A）
    return sorted(results, key=lambda x: x['date'])

origin, dest, yyyymm = sys.argv[1], sys.argv[2], sys.argv[3]
results = scrape_alaska(origin, dest, yyyymm)
available = [r for r in results if r['available']]
print(json.dumps(available, indent=2, ensure_ascii=False))
```

執行方式：

```bash
python3 /tmp/parse_alaska.py {ORIGIN} {DEST} {YYYYMM}
```

例如：`python3 /tmp/parse_alaska.py KIX TPE 202702`

---

## 輸出格式（MANDATORY）

每次查詢完成後**立刻發 Telegram**（用 message 工具），格式：

```
📅 KIX → TPE | 2027年2月
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 有位日期（按里程排序）：

2月4日 (四)   7,500 里程 + $48.3  ⭐

👉 https://www.alaskaair.com/search/?O=KIX&D=TPE&D1=2027-02-04&A=1&RT=false&ShoppingMethod=onlineaward&locale=en-us

2月2日 (二)  10,000 里程 + $45.1

👉 https://www.alaskaair.com/search/?O=KIX&D=TPE&D1=2027-02-02&A=1&RT=false&ShoppingMethod=onlineaward&locale=en-us

（若用戶指定日期無位）
❌ 2月14日 無可用里程票
```

規則：
- 按里程數**由少到多**排序
- 最便宜加 ⭐
- 每個日期必須有 👉 直連 URL，**URL 單獨一行，前後各加空行**
- 用戶指定日期無位時明確說 ❌，不要偷換成其他日期
- **查完即發，不等其他 agent**
- **Telegram chat ID 由呼叫方提供，不寫死在此**

---

## URL 參數

```
O=KIX          # 出發 IATA
D=TPE          # 目的地 IATA
D1=2027-02-04  # 指定日期（直連訂票頁）
OD=2027-02-01  # 月份任意日（行事曆 API，回傳整月）
A=1            # 大人數
RT=false       # 單程
ShoppingMethod=onlineaward
locale=en-us
```

## 已知開放 API

```bash
curl https://www.alaskaair.com/search/api/citySearch/getAllAirports
curl https://www.alaskaair.com/search/api/discounts
curl https://www.alaskaair.com/account/token
```
