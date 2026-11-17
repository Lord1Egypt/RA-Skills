# Report Data Schema

This is the JSON shape that `scripts/render_pdf.py` expects. The schema is also
mirrored in the docstring at the top of `render_pdf.py` — keep both in sync.

## Top-level

```jsonc
{
  "meta":          { /* see below */ },
  "key_takeaways": [ "string", "string", "..." ],
  "sections":      [ /* 12 entries, see below */ ]
}
```

## `meta` (cover band + footer)

| Field | Type | Notes |
|---|---|---|
| `title` | string | e.g. `"乳制品市场行情报告"` |
| `period` | string | human-readable, e.g. `"2023年10月"` |
| `generated_at` | string | ISO date, e.g. `"2026-06-26"` |
| `sources` | list[string] | appears on the cover band and footer; order matters |

## `key_takeaways` (cover card)

A list of 3–6 short Chinese strings. Each is rendered as a bulleted line in the
米色 "CORE TAKEAWAYS" card on the cover page. Keep them to one line each
(≤ 40 characters). Each must be backed by a number from the data, not a vibe.

## `sections` (12 entries, in order)

The 12 sections are described in `report-template.md`. Each entry has:

| Field | Type | Required | Notes |
|---|---|---|---|
| `title` | string | yes | Chinese section title |
| `kpis` | list[KPI] | optional | 3–4 KPI cards at the top of the section |
| `tables` | list[Table] | optional | 1–N data tables |
| `callout` | string | optional | one-liner 解读, becomes the gold-bar callout box |
| `source` | string | required for data sections | "数据来源: …" footer line |
| `events` | list[Event] | section 12 only | corporate / policy news cards |
| `sparkline` | list[(date, value)] | optional | inline time-series, rendered as small bars |

### `KPI`

```jsonc
{ "label": "生鲜乳均价", "value": "3.73 元/kg", "change": "-10.0% YoY" }
```

- `label` (string): small label above the value.
- `value` (string): the big number, include the unit (元/kg, 元/吨, 美元/吨, %, etc.).
- `change` (string): free-form change string. The renderer parses the first
  sign character to pick the pill color:
  - `+` or `↑` → red (涨)
  - `-` or `↓` → green (跌)
  - anything else → grey (flat)
  - Examples: `"+3.8%"`, `"-9.4% YoY"`, `"↑ 12.0"`, `"基本持平"`

### `Table`

```jsonc
{
  "header": ["项目", "数值", "同比"],
  "rows": [
    ["生鲜乳收购价", "3.73 元/kg", "-10.0%"],
    ["玉米", "2.99 元/kg", "-0.8%"]
  ]
}
```

- `header` (list[string]): column titles.
- `rows` (list[list[string]]): each row is a list of cell strings. Right-align
  numeric columns by leaving them as bare strings — the renderer auto-detects
  numeric columns (cells starting with a digit or `-`).

### `Event` (section 12 only)

```jsonc
{ "date": "2023-10-25", "title": "伊利收购澳优完成", "body": "..." }
```

- `date` (string): ISO date or `"YYYY-MM"` if day unknown.
- `title` (string): short headline.
- `body` (string): 1–2 sentence detail. Keep to one paragraph.

## Worked example (minimal)

```jsonc
{
  "meta": {
    "title": "乳制品市场行情报告",
    "period": "2023年10月",
    "generated_at": "2026-06-26",
    "sources": ["艾格农业《中国乳业研究月报》202310", "农业农村部"]
  },
  "key_takeaways": [
    "国内生鲜乳均价 3.73 元/kg, 同比 -10.0%, 奶价连降末端信号已现",
    "GDT 三连升, 整体指数收 994, 全脂奶粉拍卖价 3,059 美元/吨",
    "乳制品进口 YTD 全面收缩, 大包粉/乳清/奶酪/黄油同比 -15% ~ -32%",
    "国内乳制品产量 2,286 万吨 YTD, 同比 +3.8%, 龙头扩产 + 中小去产能",
    "AI 预判 2024Q1 奶价阶段性反弹, 但缺乏向上突破驱动"
  ],
  "sections": [
    {
      "title": "乳业整体形势概览",
      "kpis": [
        { "label": "国内奶价", "value": "3.73 元/kg", "change": "-10.0% YoY" },
        { "label": "国内乳制品产量 YTD", "value": "2,286 万吨", "change": "+3.8% YoY" },
        { "label": "GDT 拍卖指数", "value": "994", "change": "+1.7%" }
      ],
      "callout": "国内奶价连降末端 + GDT 反弹 + 进口全线收缩 三重背离共存, 行业进入再平衡窗口期。",
      "source": "艾格农业《中国乳业研究月报》202310; 农业农村部"
    }
  ]
}
```

## Validation checklist before running `render_pdf.py`

- [ ] `meta.title`, `meta.period`, `meta.generated_at` are present.
- [ ] `key_takeaways` has 3–6 entries, each ≤ 40 characters.
- [ ] `sections` has exactly 12 entries in the order from `report-template.md`.
- [ ] Every section with numbers has a non-empty `source`.
- [ ] Every `change` string starts with `+`/`-`/`↑`/`↓` or is intentionally
      neutral (e.g. `"基本持平"`).
- [ ] No `PageBreak`, no `KeepInFrame`, no per-section forced breaks in the
      data — that is the renderer's job.
