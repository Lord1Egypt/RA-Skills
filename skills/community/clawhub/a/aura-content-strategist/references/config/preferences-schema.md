# Preferences Schema (EXTEND.md)

## Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| version | string | ✓ | "1.0" | Schema version |
| accounts.xiaohongshu | string | ○ | null | XHS account handle |
| accounts.pinterest | string | ○ | null | Pinterest account handle |
| niche | string | ✓ | — | Primary content vertical |
| target_audience | string | ✓ | — | Primary target audience |
| brand_colors | string[] | ○ | [] | Up to 3 hex colors |
| posting_schedule | string | ○ | "不固定" | Posting frequency |
| content_language.xiaohongshu | string | ○ | "zh" | XHS content language |
| content_language.pinterest | string | ○ | "en" | Pinterest content language |
| monetization_goal | string | ○ | null | Revenue strategy |

## Validation

- `niche` and `target_audience` must not be empty
- `brand_colors` entries must be valid hex: `#RRGGBB`
- `content_language` values must be ISO 639-1 codes

## File Locations (Priority Order)

1. `.baoyu-skills/aura-content-strategist/EXTEND.md` (project)
2. `$XDG_CONFIG_HOME/baoyu-skills/aura-content-strategist/EXTEND.md` (XDG)
3. `$HOME/.baoyu-skills/aura-content-strategist/EXTEND.md` (user)

First match wins. Project-level overrides user-level.
