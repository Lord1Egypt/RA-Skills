# Ad Engine — Modular A/B Testing System

**Status:** Schema live, skill build pending
**Database:** Supabase (public schema)
**Tables:** `ad_components`, `messages`, `frameworks`, `campaigns`

---

## Overview

The Ad Engine is a database-driven system for assembling, testing, and scaling Facebook/Instagram ads using modular components. Instead of writing full ads from scratch, you build ads by combining interchangeable parts (hooks, pains, solutions, guarantees, headlines, etc.) stored in `ad_components`.

Each ad is a `messages` row with an `extra_data` JSON that references component keys. Variants share a `parent_id` and swap specific components to isolate what's being tested.

---

## Architecture

```
campaigns (what product/offer)
    │
    ├── messages (parent ads — one per angle)
    │       │
    │       ├── messages (variant A — variation_num=2)
    │       ├── messages (variant B — variation_num=3)
    │       └── messages (variant C — variation_num=4)
    │
    ├── ad_components (modular parts pool)
    │
    └── frameworks (template structures)
```

### Data Flow

```
1. Pick a framework (long_form, short_form, dm_trigger)
2. Select components by key from ad_components
3. Slot components into framework's script_template using {{merge_tags}}
4. Result = assembled ad copy
5. To A/B test: create variant message, swap 1-2 component keys
```

---

## Tables

### `ad_components`

Stores individual ad building blocks. Each row is one interchangeable piece.

| Column | Type | Description |
|--------|------|-------------|
| `id` | bigserial | Primary key |
| `created_at` | timestamptz | Auto |
| `campaign_id` | bigint (FK) | Which campaign this belongs to |
| `component_type` | text | `hook`, `pain`, `bridge`, `solution`, `proof`, `guarantee`, `cta_text`, `headline`, `description`, `cta_button`, `creative_direction`, `differentiator` |
| `component_key` | text | Short identifier for referencing (e.g., `hook_terminal_stare`, `guar_48hr_no_pay`) |
| `text` | text | The actual copy or creative direction |
| `tags` | text[] | Filtering tags: `cold`, `retargeting`, `long_form`, `short_form`, `niche`, `fear`, `authority`, `dm_trigger`, etc. |
| `ad_angle` | text | Which ad angle: `setup_is_hell`, `security_audit`, `anti_wrapper`, `dm_trigger`, `niche_real_estate`, `universal` |
| `active` | boolean | Whether this component is in rotation |
| `sort_order` | integer | Ordering within type |
| `performance_data` | jsonb | CTR, CPC, CPL, impressions — updated as ads run |

**Indexes:** `campaign_id`, `component_type`, `ad_angle`, `active`

### `messages` (existing table, extended usage)

Parent ads and their variants. Key columns for ad engine:

| Column | Usage |
|--------|-------|
| `campaign_id` | Links to campaign (e.g., 43 = ClawAgents.dev) |
| `content_type` | Set to `fb_ad` for ad engine records |
| `media_type` | `image` or `video` |
| `status` | `draft` → `active` → `paused` → `killed` |
| `seq` | Ad number within campaign (1-5 for 5 angles) |
| `framework_id` | Which framework template to use |
| `parent_id` | NULL for parent ads, parent's ID for variants |
| `variation_num` | NULL for parent, 2/3/4/... for variants |
| `extra_data` | JSON with component references, targeting, budget, test metadata |

### `frameworks` (existing table, extended usage)

| Column | Usage |
|--------|-------|
| `name` | Template name (e.g., "FB Ad — Long Form") |
| `framework_type` | Set to `fb_ad` |
| `script_template` | Template with merge tags: `{{hook}}\n\n{{pain}}\n\n{{solution}}\n\n{{cta_text}}` |

---

## Component Types

| Type | Purpose | Example |
|------|---------|---------|
| `hook` | First 1-2 lines that stop the scroll | "You've been staring at a terminal for 3 hours." |
| `pain` | Problem amplification after hook | "Docker won't start. Node.js version is wrong..." |
| `solution` | What you get / the offer | "One call. 30-45 minutes. Your OpenClaw running..." |
| `differentiator` | Anti-competitor positioning | "No monthly hosting fees that vanish..." |
| `guarantee` | Risk reversal | "If it's not running within 48 hours — you don't pay." |
| `cta_text` | In-copy call to action | "$149 setup call. Book below." |
| `headline` | Facebook headline field | "Stop Fighting Docker. Start Using Your AI Agent." |
| `description` | Facebook description field | "Done-for-you setup on YOUR server." |
| `cta_button` | Facebook CTA button | `BOOK_NOW`, `LEARN_MORE`, `SEND_MESSAGE` |
| `creative_direction` | Image/video concept description | "Dark background, terminal with red errors..." |

---

## extra_data JSON Schema

### Parent Message

```json
{
  "ad_angle": "setup_is_hell",
  "ad_name": "Setup Is Hell",
  "launch_priority": "LAUNCH FIRST",
  "format": "image",
  "targeting": {
    "interests": ["artificial intelligence", "automation", "OpenClaw"],
    "demographics": "25-55, business owners",
    "exclude": ["software engineers", "DevOps"],
    "geo": ["US", "UK", "AU", "CA"]
  },
  "budget": {
    "daily_start": 20,
    "daily_max": 100,
    "kill_threshold": "$50 no clicks"
  },
  "components": {
    "hook": "hook_terminal_stare",
    "pain": "pain_docker_node",
    "solution": "sol_one_call_full",
    "differentiator": "diff_no_monthly",
    "guarantee": "guar_48hr_no_pay",
    "cta_text": "cta_149_book",
    "headline": "hl_stop_docker",
    "description": "desc_done_right",
    "cta_button": "btn_book_now",
    "creative": "cr_terminal_horror"
  }
}
```

### Variant Message

```json
{
  "variant_name": "Short Form + Time Wasted",
  "components": {
    "hook": "hook_yc_quote",
    "pain": "pain_youtube_tutorials",
    "solution": "sol_done_50_times",
    "cta_text": "cta_149_short",
    "headline": "hl_30min_guaranteed",
    "description": "desc_no_docker",
    "cta_button": "btn_book_now",
    "creative": "cr_time_wasted"
  },
  "test_variable": "copy_length"
}
```

The `test_variable` field documents what's being isolated in the test:
- `copy_length` — long vs short form
- `creative_only` — same copy, different image
- `hook_and_creative` — different opening + image
- `hook_and_guarantee` — different risk reversal
- `cta_type` — BOOK_NOW vs SEND_MESSAGE

---

## Assembling an Ad

### Query: Get full ad copy for a message

```sql
-- Get parent ad with all component texts
SELECT
    m.id,
    m.extra_data::json->>'ad_name' as ad_name,
    m.extra_data::json->'components'->>'hook' as hook_key,
    m.extra_data::json->'components'->>'creative' as creative_key,
    hook.text as hook_text,
    pain.text as pain_text,
    sol.text as solution_text,
    diff.text as differentiator_text,
    guar.text as guarantee_text,
    cta.text as cta_text,
    hl.text as headline_text,
    desc_c.text as description_text,
    btn.text as cta_button,
    cr.text as creative_direction
FROM messages m
LEFT JOIN ad_components hook ON hook.component_key = m.extra_data::json->'components'->>'hook' AND hook.campaign_id = m.campaign_id
LEFT JOIN ad_components pain ON pain.component_key = m.extra_data::json->'components'->>'pain' AND pain.campaign_id = m.campaign_id
LEFT JOIN ad_components sol ON sol.component_key = m.extra_data::json->'components'->>'solution' AND sol.campaign_id = m.campaign_id
LEFT JOIN ad_components diff ON diff.component_key = m.extra_data::json->'components'->>'differentiator' AND diff.campaign_id = m.campaign_id
LEFT JOIN ad_components guar ON guar.component_key = m.extra_data::json->'components'->>'guarantee' AND guar.campaign_id = m.campaign_id
LEFT JOIN ad_components cta ON cta.component_key = m.extra_data::json->'components'->>'cta_text' AND cta.campaign_id = m.campaign_id
LEFT JOIN ad_components hl ON hl.component_key = m.extra_data::json->'components'->>'headline' AND hl.campaign_id = m.campaign_id
LEFT JOIN ad_components desc_c ON desc_c.component_key = m.extra_data::json->'components'->>'description' AND desc_c.campaign_id = m.campaign_id
LEFT JOIN ad_components btn ON btn.component_key = m.extra_data::json->'components'->>'cta_button' AND btn.campaign_id = m.campaign_id
LEFT JOIN ad_components cr ON cr.component_key = m.extra_data::json->'components'->>'creative' AND cr.campaign_id = m.campaign_id
WHERE m.id = 8555;
```

### Query: List all variants for an ad angle

```sql
SELECT
    m.id,
    COALESCE(m.extra_data::json->>'ad_name', m.extra_data::json->>'variant_name') as name,
    m.parent_id,
    m.variation_num,
    m.extra_data::json->>'test_variable' as testing,
    m.extra_data::json->'components'->>'hook' as hook,
    m.extra_data::json->'components'->>'creative' as creative
FROM messages m
WHERE m.campaign_id = 43
  AND m.content_type = 'fb_ad'
  AND (m.id = 8555 OR m.parent_id = 8555)
ORDER BY m.variation_num NULLS FIRST;
```

### Query: Get all components for an angle

```sql
SELECT component_type, component_key, text, tags
FROM ad_components
WHERE campaign_id = 43 AND (ad_angle = 'setup_is_hell' OR ad_angle = 'universal')
ORDER BY component_type, sort_order;
```

---

## Creating New Variants

To test a new hook against the "Setup Is Hell" parent:

```sql
INSERT INTO messages (campaign_id, content_type, media_type, status, seq, framework_id, parent_id, variation_num, extra_data)
VALUES (43, 'fb_ad', 'image', 'draft', 1, 46, 8555, 5, '{
  "variant_name": "Cost Reframe Hook",
  "components": {
    "hook": "hook_6hrs_youtube",
    "pain": "pain_docker_node",
    "solution": "sol_one_call_full",
    "differentiator": "diff_no_monthly",
    "guarantee": "guar_48hr_no_pay",
    "cta_text": "cta_149_book",
    "headline": "hl_stop_docker",
    "description": "desc_done_right",
    "cta_button": "btn_book_now",
    "creative": "cr_terminal_horror"
  },
  "test_variable": "hook_only"
}');
```

## Adding New Components

```sql
INSERT INTO ad_components (campaign_id, component_type, component_key, text, ad_angle, tags, sort_order)
VALUES (43, 'hook', 'hook_new_idea', 'Your new hook copy here.', 'setup_is_hell', ARRAY['cold','test'], 20);
```

---

## Tracking Performance

After ads run, update component performance:

```sql
UPDATE ad_components
SET performance_data = '{
  "impressions": 12500,
  "clicks": 187,
  "ctr": 1.496,
  "cpc": 2.14,
  "leads": 8,
  "cpl": 25.00,
  "last_updated": "2026-02-20"
}'::jsonb
WHERE component_key = 'hook_terminal_stare';
```

Query best-performing hooks:

```sql
SELECT component_key, text,
       (performance_data->>'ctr')::numeric as ctr,
       (performance_data->>'cpl')::numeric as cpl
FROM ad_components
WHERE component_type = 'hook' AND performance_data IS NOT NULL
ORDER BY (performance_data->>'ctr')::numeric DESC;
```

---

## Current State (Campaign 43 — ClawAgents.dev)

### Component Pool: 79 components

| Type | Count |
|------|-------|
| hook | 12 |
| creative_direction | 12 |
| headline | 11 |
| pain | 10 |
| solution | 8 |
| cta_text | 7 |
| description | 7 |
| guarantee | 4 |
| differentiator | 4 |
| cta_button | 4 |

### Ad Messages: 5 parents + 10 variants = 15 total

| Ad Angle | Parent ID | Variants | Launch Priority |
|----------|-----------|----------|-----------------|
| Setup Is Hell | 8555 | 3 (8560, 8561, 8562) | LAUNCH FIRST |
| Security Audit | 8556 | 3 (8563, 8564, 8565) | LAUNCH FIRST |
| Anti-Wrapper | 8557 | 2 (8566, 8567) | WEEK 2 (retargeting) |
| DM Trigger | 8558 | 1 (8568) | PARALLEL TEST |
| Real Estate Niche | 8559 | 1 (8569) | AFTER FIRST CLIENT |

### Frameworks: 3 templates

| ID | Name | Structure |
|----|------|-----------|
| 46 | FB Ad — Long Form (Pain-to-Solution) | hook → pain → solution → differentiator → guarantee → cta |
| 47 | FB Ad — Short Form (Direct) | hook → pain → solution → cta |
| 48 | FB Ad — DM Trigger | hook → pain → checklist → dm_cta |

---

## Future Skill Build

When this becomes a full skill (`ad-engine`), it should:

1. **Assemble** — Pull components by key, slot into framework template, output ready-to-post copy
2. **Variant Generator** — Auto-create N variants by permuting specified component types
3. **Performance Tracker** — Ingest FB Ads API data, update `performance_data` on components
4. **Winner Detector** — Flag statistically significant winners, auto-pause losers
5. **Cross-Campaign** — Reuse universal components across campaigns (different `campaign_id`)
6. **Export** — Output assembled ads in FB Ads API format for bulk upload

### Skill Structure (Planned)

```
skills/ad-engine/
├── AD_ENGINE_SPEC.md          ← this file
├── SKILL.md                   ← skill manifest (when built)
└── scripts/
    ├── assemble_ad.py         ← component → copy assembly
    ├── create_variants.py     ← auto-generate permutations
    ├── track_performance.py   ← FB API → performance_data
    └── export_ads.py          ← bulk export for FB upload
```
