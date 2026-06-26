---
name: ai-news-radar
description: Fetch curated AI news, social signals, blogs, papers, events, and skills
  from the Agentic Brew public RSS feeds (https://www.agenticbrew.ai/feed/*.xml) and
  return a compact, agent-friendly list. Use when the user wants "today's AI news",
  "what's trending in AI", "AI papers this week", "AI events", "AI blogs", "trending
  AI repos", "trending AI on Reddit / YouTube / Product Hunt", "trending AI skills",
  "ai news radar", "agentic brew feed", "AI signal radar", "latest AI digest",
  or any request to pull curated AI items from Agentic Brew without writing a scraper.
---

# Agentic Brew Feed Fetcher

Pulls items from the Agentic Brew public RSS endpoints and returns them as a clean list. No auth, no scraping — just an HTTP GET against the latest run_log's published feed.

## Available feeds

| Feed           | URL                                              | Contents | Item `<link>` resolves to |
|----------------|--------------------------------------------------|----------|---------------------------|
| `news`         | https://www.agenticbrew.ai/feed/news.xml         | Synthesized news clusters — title + overview | Agentic Brew news-analysis card page (`https://www.agenticbrew.ai/news#cluster=<id>`) |
| `twitter`      | https://www.agenticbrew.ai/feed/twitter.xml      | Trending X / Twitter topics — title + hottest tweets with likes / RTs / replies / views | The top tweet of the topic on x.com |
| `github`       | https://www.agenticbrew.ai/feed/github.xml       | Trending GitHub AI repos — title + detail (stars, language, daily delta) | Original GitHub repo |
| `reddit`       | https://www.agenticbrew.ai/feed/reddit.xml       | Trending Reddit AI threads — title + detail (subreddit, upvotes, comments, excerpt) | Original Reddit thread |
| `youtube`      | https://www.agenticbrew.ai/feed/youtube.xml      | Curated AI videos — title + summary | Original YouTube video |
| `product_hunt` | https://www.agenticbrew.ai/feed/product_hunt.xml | Trending AI launches — title + topics + tagline | Original Product Hunt launch page |
| `skill`        | https://www.agenticbrew.ai/feed/skill.xml        | Top Claude Code skills from skills.sh + clawhub — title + installs/stars + summary | Original skill page on skills.sh / clawhub |
| `blog`         | https://www.agenticbrew.ai/feed/blog.xml         | Curated AI blog articles — title + AI-generated summary | Original blog article |
| `paper`        | https://www.agenticbrew.ai/feed/paper.xml        | Research papers — title + AI summary + institutions + source (HF/AlphaXiv/X) + votes | Original paper page (arxiv / Hugging Face / x.com) |
| `event`        | https://www.agenticbrew.ai/feed/event.xml        | Upcoming AI events — title + start time + summary | Original event page (e.g., lu.ma) |
| `all`          | https://www.agenticbrew.ai/feed/all.xml          | Union of all of the above | Per-item — same as the feed above |

## Usage

```
/ai-news-radar [feed] [--limit N] [--query KEYWORD] [--json]
```

- `feed` (optional, default `news`): one of `news`, `twitter`, `github`, `reddit`, `youtube`, `product_hunt`, `skill`, `blog`, `paper`, `event`, `all`
- `--limit N` (optional, default 20): max items to return
- `--query KEYWORD` (optional): case-insensitive substring filter over title + description
- `--json` (optional): emit JSON instead of markdown

## Default interactive flow (no args, or vague request)

This skill covers a lot of ground — 11 feeds spanning news, social, papers, events, and more. If the user invokes it without specifying a feed (e.g., "show me what's new on Agentic Brew", "give me today's AI digest"), do NOT silently default to one feed. Instead, before fetching anything:

1. **Ask the user which categories they want.** Use the host agent's question UI (in Claude Code: `AskUserQuestion` with `multiSelect: true`) so the user can pick any subset of:

   `news`, `twitter`, `github`, `reddit`, `youtube`, `product_hunt`, `skill`, `blog`, `paper`, `event`

   Plus an `all` shortcut. Show a one-line description of each so the user knows what they're picking. If the user says "everything" or "all", treat as `all`.

2. **Ask the delivery frequency.** Single-select:

   - `once` — fetch immediately and return the result.
   - `daily` — fetch now AND propose setting up a recurring task. In Claude Code, suggest the `/schedule` skill (cron) or `/loop` (interval). For other host agents, surface their equivalent or tell the user how to re-invoke.
   - `weekly` — same idea, weekly cadence.

3. **Ask how much detail to include per item.** Single-select:

   - `headlines` — title only. Compact list, just "what happened."
   - `summary` — title + the AI-generated summary / overview / engagement stats (whichever the feed provides) + the source link. The default Agentic Brew item shape.
   - `detailed` — title + full description (no truncation) + source link + any `content:encoded` inner content (e.g., tweet list for twitter, overview bullets for news) + the `<category>` tags.

   To apply the choice: fetch with `--json` internally, then format the items per the chosen detail level. Do NOT pass `--limit` so low that you lose information the user asked for — only `--limit` controls *how many* items, not how *deep* each one goes.

4. Once the user has answered all three, fetch the selected feeds in parallel and present a single combined report grouped by category, formatted at the chosen detail level. If they chose `daily`/`weekly`, ALSO offer to set up the recurring schedule before exiting — don't silently leave it as a one-shot.

If the user provides explicit args (e.g., `/ai-news-radar news --limit 5`), skip the questions entirely and execute directly per the Usage section.

## Steps (direct invocation)

1. Resolve the feed URL from the chosen feed name. If the argument is invalid, abort and tell the user the valid options.
2. Run the fetch + parse one-liner below. It uses the Python stdlib only (`urllib`, `xml.etree`) — no extra installs.
3. Print the result. Default output is a markdown list (`- [title](link) — pubDate · description`). With `--json`, print a JSON array of `{title, link, description, pub_date, categories}`.

## Fetch + parse one-liner

Substitute `FEED`, `LIMIT`, `QUERY`, and `FORMAT` (`md` or `json`) before running.

```bash
FEED="news"      # news | twitter | github | reddit | youtube | product_hunt | skill | blog | paper | event | all
LIMIT=20
QUERY=""         # empty = no filter
FORMAT="md"      # md | json

python3 - "$FEED" "$LIMIT" "$QUERY" "$FORMAT" <<'PY'
import json, sys, urllib.request, xml.etree.ElementTree as ET

FEED, LIMIT, QUERY, FORMAT = sys.argv[1], int(sys.argv[2]), sys.argv[3].lower(), sys.argv[4]
URL = f"https://www.agenticbrew.ai/feed/{FEED}.xml"

req = urllib.request.Request(URL, headers={"User-Agent": "ai-news-radar-skill/1.0"})
with urllib.request.urlopen(req, timeout=30) as r:
    xml_bytes = r.read()

root = ET.fromstring(xml_bytes)
items = []
for it in root.iter("item"):
    def text(tag):
        el = it.find(tag)
        return (el.text or "").strip() if el is not None and el.text else ""
    title = text("title")
    link = text("link")
    desc = text("description")
    pub = text("pubDate")
    cats = [c.text.strip() for c in it.findall("category") if c.text]
    hay = f"{title}\n{desc}".lower()
    if QUERY and QUERY not in hay:
        continue
    items.append({
        "title": title, "link": link, "description": desc,
        "pub_date": pub, "categories": cats,
    })
    if len(items) >= LIMIT:
        break

if FORMAT == "json":
    print(json.dumps(items, ensure_ascii=False, indent=2))
else:
    for i in items:
        d = i["description"]
        if len(d) > 200: d = d[:199] + "…"
        print(f"- [{i['title']}]({i['link']}) — {i['pub_date']}\n  {d}")
    if not items:
        print("(no items matched)")
PY
```

## Notes

- The feeds always reflect the latest published run_log, so calling this skill twice in the same day usually returns the same items. There is no incremental cursor — caller is responsible for dedup if needed.
- On non-2xx HTTP responses, surface the status code and URL in RED so the user can see which endpoint failed.
- If `xml.etree` cannot parse the body, log a YELLOW warning with the first 200 chars of the response so the user can diagnose (likely a CDN error page, not XML).
- This skill is read-only against a public endpoint — no credentials, no rate limiting on the caller side. Be polite: do not call in a tight loop.
