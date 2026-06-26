---
name: city-rental-hunt
description: Search and triage rental listings from Chinese social platforms, especially Xiaohongshu via TikHub and optionally Douyin, for apartment hunting. Use when a user wants to find currently listed rentals, compare neighborhoods, build area-specific search keywords, de-duplicate posts, shortlist viable options, or create a contact brief under constraints like budget, rooms, commute, pet policy, building age, elevator, and landlord-vs-agent preference.
---

# City Rental Hunt

Turn fuzzy apartment-hunting requests into a repeatable workflow:
1. normalize constraints
2. generate zone-aware search keywords
3. search social listings
4. extract listing facts
5. filter red flags
6. produce a shortlist and contact brief

## Quick start

When the user asks to hunt rentals in a Chinese city:

1. **Normalize requirements first**
   - city
   - target zones
   - budget range
   - room count
   - must-have constraints
   - one-vote vetoes

2. **Generate search keywords**
   - Run:
     ```bash
     python3 skills/city-rental-hunt/scripts/keyword_plan.py \
       --city 北京 \
       --zones "北苑,霍营,清河" \
       --budget "6000-9000" \
       --rooms "两居" \
       --must "整租,电梯,次新" \
       --optional "可养猫,房东直租,转租"
     ```
   - This produces reusable search phrases for each zone.

3. **Search platforms in this order**
   - **First:** Xiaohongshu via TikHub
   - **Second:** Douyin via TikHub
   - Use the existing social-media skill/tooling instead of inventing new scraping flows.

4. **Collect only listing-relevant facts**
   - platform
   - post id / URL
   - title / short summary
   - price if present
   - neighborhood / subway / zone
   - freshness
   - landlord / agent / unclear
   - pet policy if present
   - likely keep / maybe / discard

5. **Output a shortlist, not a dump**
   - Keep the result decision-oriented.
   - Separate high-confidence leads from weak leads.

## Workflow

### Step 1 — Normalize the requirement brief

Use this compact schema:

```yaml
city: 北京
zones: [北苑, 霍营, 清河]
budget: 6000-9000
rooms: 两居
must_have:
  - 整租
  - 电梯
  - 次新/不要老小区
soft_preferences:
  - 客厅大
  - 房东直租
  - 靠近地铁
  - 宠物友好
vetoes:
  - 老小区
  - 合租
  - 商住
  - 非民水民电
```

If the user gives vague input, infer only the search structure, not the final preference.

### Step 2 — Build search buckets by zone

Do **not** search one giant keyword first. Split by zone.

For each zone, create 3 buckets:
1. **broad**: `北苑 整租 两居`
2. **quality**: `北苑 次新 电梯 两居`
3. **conversion**: `北苑 房东直租 两居` / `北苑 转租 两居` / `北苑 可养猫`

If a known neighborhood appears repeatedly, promote it into its own bucket.

### Step 3 — Search Xiaohongshu first

Use TikHub endpoints exposed by the existing social-media skill. Typical flow:
- check `help`
- check `list-endpoints xiaohongshu` when needed
- search notes with short, high-signal phrases

Prefer short Chinese queries over long natural-language queries. TikHub/XHS search often degrades on long keyword strings.

### Step 4 — Search Douyin as a supplement

Use Douyin only after XHS has produced a first-pass pool.

Douyin is useful for:
- video walk-throughs
- “刚空出来” style posts
- transfer/转租 leads

Do not let Douyin dominate the run unless XHS is thin in that city/zone.

### Step 5 — Extract and classify leads

For every lead, classify:
- **keep**: fresh, plausibly matches constraints, enough information to contact
- **maybe**: missing price / pet policy / building age, but still promising
- **discard**: clear red flag

Use the red-flag checklist in `references/playbook.md`.

### Step 6 — Produce two outputs

#### Output A: analyst-facing search record
Include:
- keywords used
- leads found
- keep/maybe/discard reasoning
- repeated neighborhoods worth deeper follow-up

#### Output B: user-facing morning brief
Include only:
- top leads
- why they matter
- what to contact first
- key uncertainties to verify

## Scoring heuristics

Use these dimensions:
- **freshness**: today / yesterday / within 7 days / stale
- **constraint fit**: rooms, budget, elevator, new-enough community
- **contactability**: landlord direct > personal transfer > unclear > obvious agent spam
- **risk**: old community, no elevator, price missing, ad tone, commercial apartment, shared rental smell
- **special upside**: pet-friendly, unusually concrete price, exact move-in date, strong transit fit

A listing with incomplete price can still rank high if it is very fresh and structurally fits.

## What to avoid

- Do not treat every social post as a real listing.
- Do not present stale posts as active inventory.
- Do not bury the user in 30 weak links.
- Do not confuse “cheap” with “good fit”.
- Do not publish or embed private commute addresses or personal names when turning a private search workflow into a reusable skill.

## Default report shape

Use this structure unless the user asks otherwise:

```markdown
# Rental hunt brief

## Requirement snapshot

## Zones searched

## Top leads
- lead
- lead
- lead

## Backup leads

## Repeated neighborhoods worth deeper checking

## Risks / unknowns to verify
- price
- pet policy
- landlord vs agent
- building age / elevator

## Contact-first order
1. ...
2. ...
3. ...
```

## When to read the reference

Read `references/playbook.md` when you need:
- a fuller keyword-building pattern
- a reusable evidence schema
- a red-flag checklist
- a morning-brief template
