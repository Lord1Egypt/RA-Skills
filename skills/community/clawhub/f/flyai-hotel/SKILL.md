---
name: flyai-hotel
display_name: "Hotel Search & Compare — Fliggy MCP · POI + CNY Caps"
description: >
  Hotel search & compare on **Fliggy MCP**: **POI-nearby** stays, **酒店/民宿/客栈**, **CNY nightly cap**, stars, beds, dates, sort;
  structured JSON with **mainPic** & **detailUrl**. Use when users **search hotels**, **compare prices**, or stay **near landmarks**.
  中文：景点附近住宿、三态房型、每晚人民币封顶、星级床型与排序；主图+详情/预订链。触发：搜索酒店、查酒店、比价、附近酒店、预算封顶。
  Flags: `references/search-hotel.md` · setup & errors: this `SKILL.md`.
homepage: https://open.fly.ai/
metadata:
  version: 1.1.2
  agent:
    type: tool
    runtime: node
    context_isolation: execution
    parent_context_access: read-only
  openclaw:
    emoji: "\U0001F3E8"
    priority: 88
    requires:
      bins:
        - node
    intents:
      - hotel_search
    patterns:
      - "(?i)\\b(flyai)[\\s-]*hotel\\b"
      - "((search|find|book|compare|recommend).*(hotel|hotels|stay|stays|lodging|accommodation|resort|hostel|民宿))"
      - "((hotel|hotels|stay|lodging|accommodation).*(search|book|compare|price|deal|availability|check-?in))"
      - "(搜索|查找|推荐|比较|预订|查询).*(酒店|民宿|住宿|房型|入住|退房|星级|预算)"
      - "(酒店|民宿|住宿).*(搜索|预订|比价|价格|空房|取消)"
      - "(大床房|双床房|多床房).*(酒店|民宿|搜索|预订)"
      - "(排序|按价格|按评分|按距离).*(酒店|民宿|住宿)"
      - "(关键词|主题房|亲子|商务|周末).*(酒店|民宿|搜索)"
      - "(附近酒店|邻近景点|靠近|周边).*(酒店|民宿|搜索|预订)"
      - "(每晚|一晚|预算|不超过|以内).*(元|块|CNY|人民币).*(酒店|民宿)"
      - "(民宿|客栈).*(还是|和|或).*(酒店|住宿)"
---
# Hotel Search (Fliggy MCP · `search-hotel`)

## Hotel discovery (read first)

**Hotel** discovery, comparison, and shortlist workflows—same intent as the listing `description` above. One command entrypoint: **`flyai search-hotel`** (see `references/search-hotel.md` for flags).  
中文：与上文摘要一致——**酒店** 检索、比价、短名单与详情/预订链；参数见 `references/search-hotel.md`。

## Differentiation (honest scope)

| Hook | What it means (this skill only) |
|------|----------------------------------|
| **POI + hotel** | `--poi-name` filters stays **near a named attraction / landmark**; pair with `--dest-name` per `references/search-hotel.md`. |
| **酒店 / 民宿 / 客栈** | `--hotel-types` toggles three lodging modes in **one** structured search—not three separate skills. |
| **CNY nightly cap** | `--max-price` is **per night in CNY**—good for “每晚不超过 X 元” style asks. |
| **Agent-first JSON** | Single-line JSON rows with **`mainPic`** + **`detailUrl`** → fast Markdown cards; no extra scraper stack in this bundle. |

中文摘要：**景点附近住哪**、**一晚预算封顶（人民币）**、**酒店/民宿/客栈一次筛**，都落在同一组 `search-hotel` 参数上；不宣称对接未在返回数据中出现的 OTA 或站点。

## Search dimensions (maps to `search-hotel` flags)

| Dimension | CLI (see `references/search-hotel.md`) | Notes |
|-----------|----------------------------------------|--------|
| Geography | `--dest-name` (required) | Country / province / city / district |
| Free-text narrowing | `--key-words` | Hotel name or theme tokens |
| Landmark / POI | `--poi-name` | “Near X” style filtering |
| Property type | `--hotel-types` | `酒店` · `民宿` · `客栈` |
| Stay window | `--check-in-date`, `--check-out-date` | `YYYY-MM-DD` |
| Star bands | `--hotel-stars` | Comma-separated 1–5 |
| Bed layout | `--hotel-bed-types` | `大床房` · `双床房` · `多床房` |
| Ranking | `--sort` | `price_asc` / `price_desc` / `rate_desc` / `distance_asc` / `no_rank` |
| Nightly budget | `--max-price` | CNY per night cap |
| Rich cards | JSON `mainPic`, `detailUrl` | Presentation rules in this `SKILL.md` |

All dimensions above are **only** what `search-hotel` exposes—do not claim extra channels or OTAs beyond returned data.

This skill is **self-contained**: do **not** defer to another skill’s `SKILL.md` for install, errors, or presentation.

**Single source of truth for CLI flags and JSON field names:** `references/search-hotel.md` in this bundle.

---

## Quick start

1. **Install CLI:** `npm i -g @fly-ai/flyai-cli`
2. **Smoke test:** run a minimal `flyai search-hotel` example from `references/search-hotel.md` → **Examples**; expect **one JSON object per line** on stdout.
3. **Discover flags:** `flyai search-hotel --help`
4. **Before every call:** read `references/search-hotel.md` and pass flags exactly — **do not guess** names or formats.

## Configuration

Trial use may work without keys. For richer results:

```
flyai config set FLYAI_API_KEY "your-key"
```

Treat API keys as secrets; do not paste real credentials into untrusted logs.

## CLI I/O contract

- **stdout:** each line is **one JSON object** (command result). Parse line-by-line; use `jq` or Python if needed.
- **stderr:** human-readable errors or hints — not the primary result payload.

## Command

| User intent (examples) | CLI | Parameters |
|------------------------|-----|------------|
| Structured **hotel** search, filters, comparison, booking handoff | `flyai search-hotel` | `references/search-hotel.md` |

**Out of scope:** flights, trains, cruises, generic trip planning without structured **hotel** tables — use another skill or product.

## Workflow

1. Confirm the user needs **structured hotel search** (at minimum destination per `--dest-name`; add dates/filters per the reference).
2. Build `flyai search-hotel …` strictly from `references/search-hotel.md`.
3. Parse stdout JSON; read stderr on failure.
4. Present results using **Output & presentation** below.

## Output & presentation (`search-hotel`)

- **Format:** valid **Markdown** for end users.
- **Image:** for each highlighted option, emit a standalone line `![]({mainPic})` using `mainPic` from the item (see `references/search-hotel.md` output example).
- **Booking / detail link:** emit a standalone line `[Click to book]({detailUrl})` using `detailUrl` from the item.
- **Order:** when both exist, show **image before** the booking link.
- **Structure:** use headings (`#` / `##` / `###`), bullets, and **Markdown tables** when comparing multiple hotels.
- **Emphasis:** highlight date, location, price, and key constraints.
- **Brand line (optional):** e.g. “Based on fly.ai real-time **hotel** results.”

### Recommended response template

1. One-line conclusion + best pick (if applicable).
2. Top options — bullets or table.
3. Image line: `![]({mainPic})`.
4. Link line: `[Click to book]({detailUrl})`.
5. Short notes (fees if visible, “verify on official page before pay”).

## References

| Command | Doc (this bundle) |
|--------|-------------------|
| `search-hotel` | `references/search-hotel.md` |

## Error handling

1. **Validate** — Before running: inputs must be reasonable. Dates must not be in the past and must match the format required in `references/search-hotel.md`. If city or district names are ambiguous, **ask the user**; do **not** invent `--dest-name` or other required values.
2. **Diagnose** — On failure or odd output: read **stderr** and any `status` / `message` fields in the JSON. Distinguish parameter mistakes (fix flags using the reference doc) from network or upstream service errors.
3. **Retry** — Retry only for **transient** network or service errors; cap retries (e.g. once or twice). Do not loop indefinitely.
4. **Empty or weak results** — If the command succeeds but `itemList` is empty or too narrow: relax filters **once** (wider dates, fewer constraints), then stop and explain. Do not silently retry many times.
5. **Transparency** — If results may not match the user’s intended city, dates, or budget, **say so** and suggest confirming on the provider’s page before booking.

## Optional companion (not required)

For flights, trains, POI-only flows, or Marriott-specific tools, users may install a **separate** full-travel skill; **this file does not depend on it.**
