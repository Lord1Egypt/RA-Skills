---
name: daily-biotech-briefing
description: 生成每日生物医药早报，包含 GitHub Trending 日榜和5个生物医学方向（干细胞治疗、外泌体治疗、质谱诊断、拉曼诊断、卵巢癌检测）的最新微信文章摘要。每天早上10点通过 cron 触发，发送到用户 QQ 邮箱。使用 web_fetch 抓取 github.com/trending 和 wechat-article-search 技能搜索微信文章，curl 阅读正文。
---

# Daily Biotech Briefing

Generate and send a daily biotech morning briefing to the user's QQ email.

## Prerequisites

- `wechat-article-search` skill installed (with cheerio)
- `qqmail` skill installed (QQMAIL_USER, QQMAIL_AUTH_CODE configured)
- curl, python3 available

---

## 🚨 CRITICAL: Content Source Rules (READ BEFORE ANYTHING ELSE)

### ❌ ABSOLUTELY FORBIDDEN — VIOLATION = BROKEN BRIEFING

1. **NEVER use `web_search`** to find biotech articles. All WeChat articles MUST come from `wechat-article-search` only.
2. **NEVER use `web_fetch`** on non-WeChat URLs (news sites, blogs, journals, etc.) for article content.
3. **NEVER fabricate or supplement** article summaries from the model's own knowledge base.
4. **NEVER add content** for a topic that has zero valid articles after filtering — write "今日无相关前沿动态" instead.

### ✅ ALLOWED DATA SOURCES

| Source | Allowed? | Notes |
|--------|----------|-------|
| `web_fetch` on `github.com/trending` | ✅ | Only for GitHub section |
| `search_wechat_curl.sh` JSON output | ✅ | The ONLY source for all 5 topic sections |
| `web_search` for any biotech content | ❌ | NEVER |
| `web_fetch` on non-GitHub URLs | ❌ | NEVER |
| Model knowledge / training data | ❌ | NEVER use to "fill in" content |

### 🔍 VALIDATION CHECKLIST (must pass before sending email)

When composing the email body, verify EVERY article entry:
- [ ] The article URL starts with `https://mp.weixin.qq.com/` (resolved from sogou via `resolve_urls.py`)
- [ ] The article title + summary match a record in the wechat-article-search JSON output file
- [ ] The article's `datetime` field is within the last 48 hours
- [ ] The article passed both time and content filters
- [ ] If ANY article fails any check → DELETE it from the email, do not substitute

---

## Workflow

### Step 1: GitHub Trending

Fetch the GitHub trending daily page:

```
web_fetch url="https://github.com/trending" maxChars=20000
```

Parse the top 15 repos from the markdown output. For each repo:
- Extract: owner/repo, description, language, stars today, total stars
- DO NOT visit repo pages — use the description from the trending page directly
- Write a 2-3 line Chinese introduction based on the description
- Use Markdown hyperlink format: `[owner/repo](https://github.com/owner/repo)`

### Step 2: WeChat Article Search

**🚨 CRITICAL: Use `search_wechat_curl.sh` only. DO NOT use `node search_wechat.js` — it is BLOCKED by Sogou anti-spider (Node.js TLS fingerprint detected).**

See [topics.md](references/topics.md) for exact commands and keyword configurations.

**🔄 多关键词轮换策略（Topic 3 质谱诊断 & Topic 4 拉曼诊断）**

These niche topics need multiple keyword variants. See [topics.md](references/topics.md) for the full merge script.

| Topic | Keywords |
|-------|----------|
| 质谱诊断 | `临床质谱`, `质谱 临床 检测` |
| 拉曼诊断 | `拉曼 临床 检测`, `SERS 检测 临床`, `表面增强拉曼 检测` |

**Wait 3-5 seconds between each search.** Curl-based searches are less likely to trigger anti-spider but still need spacing.

**If a topic returns 0 articles → mark as empty.** Use "今日无相关前沿动态".

### Step 3: Time Filter (CRITICAL — must execute manually in Python)

**Do NOT rely on eyeballing datetimes.** You MUST run this exact Python script on every topic's JSON. The script prints every article with its datetime so you can verify the filter is working, and discards articles with missing/bogus datetimes.

```python
import json
from datetime import datetime, timedelta, timezone

TZ = timezone(timedelta(hours=8))

# Load articles
with open('/tmp/wx_<topic>.json') as f:
    data = json.load(f)

now = datetime.now(TZ)
cutoff = now - timedelta(hours=48)

print(f"Current time: {now.isoformat()}")
print(f"Cutoff (48h ago): {cutoff.isoformat()}")
print(f"Total articles in file: {len(data['articles'])}")
print()

recent = []
for a in data['articles']:
    dt_str = a.get('datetime', '')
    
    # Skip articles with no datetime or clearly wrong datetime
    if not dt_str or len(dt_str) < 16:
        print(f"  ❌ SKIP (no/bad datetime: '{dt_str}'): {a.get('title','?')}")
        continue
    
    # Parse datetime in Asia/Shanghai timezone
    try:
        dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S').replace(tzinfo=TZ)
    except ValueError:
        print(f"  ❌ SKIP (parse failed: '{dt_str}'): {a.get('title','?')}")
        continue
    
    # Check against cutoff
    age = now - dt
    age_hours = age.total_seconds() / 3600
    status = "✅" if dt >= cutoff else f"❌ OLD ({age_hours:.0f}h ago)"
    print(f"  {status} [{dt_str}] {a.get('title','?')}")
    
    if dt >= cutoff:
        recent.append(a)

print(f"\n✅ After 48h filter: {len(recent)} articles kept out of {len(data['articles'])}")
print(f"❌ Discarded: {len(data['articles']) - len(recent)} articles")
```

**Verify the output before proceeding.** If you see articles from last month/last year being kept, STOP — the filter is broken and must be fixed before continuing.

### Step 4: Content Filter (Pop-Sci / Clickbait)

Apply filter rules from [filter-rules.md](references/filter-rules.md) using this Python script:

```python
import json, re

REJECT_PATTERNS = [
    r'震惊', r'不为人知', r'你绝对想不到', r'太神奇了',
    r'！！', r'!!',
    r'让.*年轻', r'逆龄', r'冻龄', r'返老还童',
    r'点击购买', r'限时优惠', r'免费领取',
    r'^什么是', r'^一文读懂', r'^科普', r'^带你了解',
]

with open('/tmp/wx_<topic>.json') as f:
    data = json.load(f)

# recent = [...from step 3...]

filtered = []
for a in recent:
    title = a.get('title', '')
    summary = a.get('summary', '')
    text = title + ' ' + summary
    
    if any(re.search(p, text) for p in REJECT_PATTERNS):
        print(f"  ❌ REJECT: {title}")
        continue
    
    filtered.append(a)
    print(f"  ✅ KEEP: {title}")

print(f"\n✅ After content filter: {len(filtered)} articles")
filtered = filtered[:5]  # top 5
```

**If filtered is empty → this topic is EMPTY. Proceed to next topic. Do NOT search for content elsewhere.**

### Step 5: Resolve Article URLs

**⚠️ Sogou redirect links are AES-encrypted. Must resolve to real mp.weixin.qq.com URLs before including in email.**

Use the `resolve_urls.py` script which gets a fresh SNUID cookie from v.sogou.com, then parses JS redirects to extract real WeChat URLs.

```bash
python3 ~/.openclaw/workspace/skills/wechat-article-search/scripts/resolve_urls.py \
  /tmp/wx_<topic>.json > /tmp/wx_<topic>_resolved.json
```

The resolved JSON will have a `url_mp` field for each article with the real mp.weixin.qq.com link.

**If resolution fails → this is a hard blocker. Report to user. Do NOT send email with broken sogou links.**

### Step 6: Compose Article Summaries

**⚠️ Sogou redirect links CANNOT be resolved to mp.weixin.qq.com URLs.** The sogou redirect service also triggers anti-spider. Use the search result summaries as the content source.

For each filtered article, compose a 2-3 sentence summary in Chinese based on the `title` + `summary` fields from the JSON output. The search summaries are detailed enough to create informative briefs.

For the article link, use the sogou redirect URL from the search results (users can open it in a browser where the CAPTCHA is manually solvable). Format as:
```
📎 [原文链接](https://weixin.sogou.com/link?url=...)
```

### Step 6: Compose Email

Follow the email template in [email-template.md](references/email-template.md).

**Critical rules:**
- Compose summaries based on the search result `title` + `summary` fields
- Every article entry MUST include the resolved `url_mp` link: `📎 https://mp.weixin.qq.com/s/...`
- Empty topics MUST say `> 今日无相关前沿动态`

### Step 7: Pre-Send Validation (MANDATORY)

**Before sending, run this Python validation:**

```python
import re

body = """<paste full email body here>"""

# Check all non-GitHub URLs are mp.weixin.qq.com
urls = re.findall(r'https?://[^\s\u4e00-\u9fff\u3000-\u303f\uff00-\uffef\)]+', body)
for u in urls:
    if 'github.com' in u:
        continue
    if 'mp.weixin.qq.com' not in u:
        print(f"❌ NON-WECHAT URL FOUND: {u[:100]}")
        print("REMOVE this entry before sending!")
        exit(1)

print("✅ All article links are mp.weixin.qq.com (GitHub links OK)")

# Check every topic section has either articles or "无动态"
topics = ['干细胞治疗', '外泌体治疗', '质谱诊断', '拉曼诊断', '卵巢癌检测']
for topic in topics:
    idx = body.find(f'🧬 {topic}')
    if idx == -1:
        print(f"⚠️  Missing topic section: {topic}")
        continue
    next_idx = min(
        [body.find(f'🧬 {t}', idx + 1) for t in topics if body.find(f'🧬 {t}', idx + 1) > 0] + [len(body)]
    )
    section = body[idx:next_idx]
    has_article = '📄' in section
    has_empty = '今日无相关前沿动态' in section
    if has_article:
        print(f"✅ {topic}: has articles")
    elif has_empty:
        print(f"ℹ️  {topic}: correctly marked empty")
    else:
        print(f"❌ {topic}: no articles AND no '无动态' notice!")

print("\n✅ Validation complete")
```

If validation shows any ❌ → **FIX THEM before sending.** Don't force-send a broken email.

### Step 8: Send Email

Send promptly — links expire in ~15 minutes.

```bash
python3 ~/.openclaw/workspace/skills/qqmail/scripts/qqmail.py send \
  --to "$QQMAIL_USER" \
  --subject "生物医药每日早报｜YYYY-MM-DD" \
  --body "<full_email_body>"
```

**🚨 CRITICAL: 收件人硬性约束**
- **必须使用** `$QQMAIL_USER` 环境变量作为收件人
- **绝对禁止**编造或猜测任何其他邮箱地址
- 发送前用 `echo "收件人: $QQMAIL_USER"` 确认环境变量已加载
- 如果 `$QQMAIL_USER` 为空，STOP — 不要发送

### Step 9: Post-Send Verification (MANDATORY)

**发送后必须验证邮件已到达收件箱：**

```bash
export $(grep -v '^#' ~/.openclaw/.env | xargs)
python3 ~/.openclaw/workspace/skills/qqmail/scripts/qqmail.py inbox --limit 5
```

检查前 5 封邮件中是否存在刚刚发送的"生物医药每日早报｜YYYY-MM-DD"。

- ✅ 如果找到 → 任务完成
- ❌ 如果未找到 → 邮件发送失败，立即重新发送一次
- ❌ 如果 `$QQMAIL_USER` 为空导致无法发送 → 记录为失败，不伪造成功

### Step 10: Report Statistics

Include in email footer:
- WeChat articles searched (by keyword): X per topic, total ~250
- After 48h time filter: X
- After content filter: X
- GitHub repos: 15

---

**⚠️ About search links:**
- Curl-based search returns sogou redirect links (cannot be resolved — sogou anti-spider blocks URL resolution)
- Article summaries come from search result `summary` field (detailed enough for briefing)
- Users can open sogou links in browser — captcha is solvable manually

## Note

- This skill is triggered by a cron job at 10:30 AM daily (Asia/Shanghai).
- Running model: opencode-go/deepseek-v4-pro.
- All intermediate files go to /tmp/, clean up after sending.
- Search tool: `search_wechat_curl.sh` (NOT `node search_wechat.js`)
