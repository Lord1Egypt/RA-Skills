# eonik — tool reference

The live catalog comes from the user’s eonik account (`tools/list`). This file is a human map, not a second schema.

The public connector ([eonik-mcp](https://github.com/eonik-ai/eonik-mcp)) **does not offer** `record_validation_decision` or `save_creative_read` (those stay in the Mac app).

## Gather (read-only facts)

| Tool | Role |
|------|------|
| `get_brand_briefing` | Orientation: brand, rails, verbatim memory, what changed, corpus inventory |
| `get_brand_context` | Brand DNA |
| `get_context_ledger` | Truths, dated plans, recent corrections — verbatim |
| `get_account_condition` | live / dark / not_connected |
| `get_recent_slates` | Monday considerations + receipts |
| `get_account_memory` | Own-account tested / won / lost by dimension; two horizons (`craft_profile` vs `craft_standing`); `held` = separates, check delta **sign** |
| `get_watch_activity` | Recent competitor / category activity |
| `get_competitor_channels` | Watched competitors × channel counts |
| `get_competitor_assets` | One competitor, one channel, paged (`channel`: meta_ad_library \| tiktok_ad_library \| google_ads_transparency \| instagram_organic \| instagram_hashtag) |
| `get_category_topics` | Hashtag topic bundles |
| `get_my_competitor_ads` | Ads from configured competitors |
| `search_competitor_ads` | Global library search |
| `search_swipe` | Marketer's own swipe file |
| `lookup_ad_performance` | One **own** ad |
| `list_my_ads` | Own ads dashboard (facts) |
| `get_campaign_performance` | One **own** campaign breakdown |
| `sync_my_ads` | Queue read-only Meta insights sync (never writes to Meta) |

## Research (labor; agent reasons)

| Tool | Role |
|------|------|
| `deconstruct_ad` | Queue scene-split + transcript + structure (public ads) |
| `get_ad_deconstruction` | Read the breakdown |
| `get_competitor_patterns` | Counts across deconstructed ads |
| `get_competitor_timeline` | Chronological archive + lifespans |
| `get_craft_playbook` | How surviving ads are made — descriptive pointers, not causation |
| `probe_asset_duration` | Measure archived creative length |
| `get_ad_for_clone` | Resolve one archived ad to clonable media (structure clone, not asset theft) |
| `get_validation_grounding` | Pre-export norms pack for a **draft signature** — facts + arithmetic, never predictions |

## Remember (verbatim notes)

| Tool | Role |
|------|------|
| `save_context_note` | One-off correction / preference |
| `save_brand_truth` | Durable truth: objective \| value_gradient \| creative_truth \| economics |
| `save_plan` | Dated sale / launch / seasonal — read the date back |
| `remember` | subject + relation + fact (supersedes prior same relation) |
| `recall` | Semantic search over brand memory |

## Produce

| Tool | Role |
|------|------|
| `get_brief_grounding` | **Preferred.** Receipt-bound data; **you** author the brief |
| `generate_creative_brief` | Deprecated server-authored brief |

## Authentication

`X-API-Key` or `Authorization: Bearer`. Agents do not embed secrets in skill text.

## Hard bans

No pause / scale / kill / launch. No performance predictions. No "budget leak" / Spyder / autonomous pipeline language.
