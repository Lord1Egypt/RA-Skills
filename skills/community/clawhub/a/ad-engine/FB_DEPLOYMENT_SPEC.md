# Facebook Ads Deployment Spec — Ad Engine → Meta Ads Manager

**Status:** Spec complete, ready to execute
**Campaign:** 43 (ClawAgents.dev)
**Ad Account:** TBD (needs FB Business Manager setup)
**Starting Budget:** $5/day (demand validation)

---

## PHASE 0: $5/DAY DEMAND VALIDATION

**Goal:** Prove people want OpenClaw setup help. That's it. No fancy funnels, no complex structure. One ad, one audience, do people respond?

### Why DM Trigger at $5/day

At $5/day you can't optimize for conversions — Facebook needs ~50 conversions/week per ad set to exit learning phase, and $5/day won't get you there. But **Messages campaigns are cheap** ($0.50-2.00 per conversation started) and give you:
- Direct conversations with potential buyers
- Zero landing page needed
- Proof of demand in DM volume
- At $5/day you could get 3-10 DMs/day

### The Setup (15 minutes)

```
📁 CAMPAIGN: "CA43 | Validation | Messages"
 │   Objective: MESSAGES
 │   Budget: $5/day (ad set level)
 │
 └── 📁 AD SET: "CA43 | Setup Help | Broad"
      │   Budget: $5/day
      │   Audience: Broad — interests: AI, automation, chatbots, OpenClaw
      │   Age: 25-55
      │   Geo: US (single country, keeps it simple)
      │   Placements: Automatic
      │   Optimization: Maximize conversations
      │
      ├── AD: "CA43 | 8556-v2 | Security Audit | DM AUDIT"
      └── AD: "CA43 | 8558-v1 | Setup Checklist | DM SETUP"
```

### Why These 2 Ads

**Security Audit (DM "AUDIT")** — Fear-driven, zero friction. "Is your OpenClaw exposed? DM me AUDIT and I'll check for free." Costs you nothing to deliver, proves demand for security concerns.

**DM Trigger (DM "SETUP")** — Value-first. "I've set up OpenClaw 50+ times. DM SETUP for my checklist." Lead magnet without a landing page.

Both drive DMs. You respond manually. If people are DMing, there's demand. If nobody DMs after $35 (1 week), the angle is wrong or the audience is wrong.

### Validation Metrics (7 Days = $35 Total)

| Result | What It Means | Next Step |
|--------|--------------|-----------|
| 0 DMs | No demand at this targeting/angle | Try different hook or broader audience |
| 1-3 DMs | Weak signal | Tweak copy, run another week |
| 4-10 DMs | Demand validated | Ask what they need, offer to set up for $149 |
| 10+ DMs | Strong demand | Bump to $10-15/day, add Leads campaign |

### DM Response Script

When someone DMs "AUDIT":
```
Hey! Happy to check your setup.

Quick Qs:
1. Is your OpenClaw on a VPS, local machine, or hosted service?
2. Do you know if authentication is enabled?

I'll run a quick check and let you know what I find.
```

When someone DMs "SETUP":
```
Hey! Here's the checklist I use for every setup: [link to PDF/doc]

Quick Q — have you already started setting up OpenClaw, or still deciding?
```

Then qualify:
- "Still deciding" → "What's your use case? I can tell you if it's the right tool."
- "Started but stuck" → "Where'd you get stuck? Usually step 3 or 7."
- "Want someone to do it" → "I do that. 30 min call, $149. Want the booking link?"

### Creative Needed (2 images only)

| # | Image | Quick Canva Brief |
|---|-------|------------------|
| 1 | Security Audit | Dark bg, red glow, "135,000" big number, "Is yours exposed?" |
| 2 | Setup Checklist | Dark bg, partial checklist with lock icon, "DM SETUP" |

### Scaling Path

```
$5/day   → Validate (are people DMing?)
$10/day  → Add the "Setup Is Hell" angle as a Leads campaign
$20/day  → A/B test copy variants within winning angle
$50/day  → Add retargeting + niche campaigns
$100/day → Full structure from spec below
```

---

## FULL SPEC (For When You're Ready to Scale)

---

## Facebook Ads Hierarchy (How Meta Structures It)

```
📁 AD ACCOUNT
 └── 📁 CAMPAIGN (objective + budget strategy)
      └── 📁 AD SET (targeting + budget + schedule)
           └── 📄 AD (creative + copy + CTA + landing URL)
```

**Rules:**
- 1 Campaign = 1 objective (Leads, Messages, Conversions, etc.)
- 1 Ad Set = 1 audience definition + 1 budget
- 1 Ad = 1 creative + 1 copy combo
- Facebook rotates ads within an ad set and auto-optimizes to the winner
- To truly isolate a test variable, you either use separate ad sets or Facebook's A/B test tool

---

## Our Campaign Structure

### Phase 1: Testing (Week 1-2) — Use ABO

ABO (Ad Set Budget Optimization) = you control how much each ad set spends. This is critical during testing because CBO would let Facebook dump 90% of budget into one ad set before the others collect enough data.

```
📁 CAMPAIGN: "CA43 | ABO | Testing | Leads | Cold"
 │   Objective: LEADS (or MESSAGES for DM trigger ads)
 │   Budget: Ad Set Level (ABO)
 │
 ├── 📁 AD SET: "CA43 | Setup Is Hell | Cold | US-UK-AU-CA"
 │    │   Budget: $25/day
 │    │   Audience: Interests (AI, automation, OpenClaw, chatbots)
 │    │   Age: 25-55
 │    │   Exclude: Software engineers, DevOps
 │    │   Placements: Automatic (FB + IG feed, stories, reels)
 │    │
 │    ├── AD: "CA43 | 8555-v1 | hook_terminal | cr_terminal_horror | long"
 │    ├── AD: "CA43 | 8555-v2 | hook_yc_quote | cr_time_wasted | short"
 │    ├── AD: "CA43 | 8555-v3 | hook_terminal | cr_the_quote | long"
 │    └── AD: "CA43 | 8555-v4 | hook_yc_quote | cr_terminal_horror | short"
 │
 ├── 📁 AD SET: "CA43 | Security Audit | Cold | US-UK-AU-CA"
 │    │   Budget: $25/day
 │    │   Audience: Same + cybersecurity, data privacy, VPS, Docker, Linux
 │    │
 │    ├── AD: "CA43 | 8556-v1 | hook_135k | cr_red_alert | long"
 │    ├── AD: "CA43 | 8556-v2 | hook_quick_q | cr_exposed | short"
 │    ├── AD: "CA43 | 8556-v3 | hook_135k | cr_cve_warning | long"
 │    └── AD: "CA43 | 8556-v4 | hook_quick_q | cr_red_alert | dm"
 │
 └── 📁 AD SET: "CA43 | DM Trigger | Cold | US-UK-AU-CA"
      │   Budget: $15/day
      │   Audience: Same as Setup Is Hell
      │   Optimization: MESSAGES (not leads)
      │
      ├── AD: "CA43 | 8558-v1 | hook_dozens | cr_checklist | dm"
      └── AD: "CA43 | 8558-v2 | hook_50_setups | cr_simple_bold | dm"

DAILY TOTAL: ~$65/day ($25 + $25 + $15)
WEEKLY TOTAL: ~$455
```

### Phase 2: Retargeting (Week 2+) — Separate Campaign

```
📁 CAMPAIGN: "CA43 | ABO | Retargeting | Leads | Warm"
 │   Objective: LEADS
 │
 └── 📁 AD SET: "CA43 | Anti-Wrapper | Retarget | Engaged-Not-Booked"
      │   Budget: $10-15/day
      │   Audience: Custom — engaged with Ad 1/2 but didn't convert
      │
      ├── AD: "CA43 | 8557-v1 | hook_17k | cr_graveyard | long"
      ├── AD: "CA43 | 8557-v2 | hook_17k | cr_hosted_vs_own | long"
      └── AD: "CA43 | 8557-v3 | hook_3_sale | cr_graveyard | short"
```

### Phase 3: Niche (Week 3+) — After First Client

```
📁 CAMPAIGN: "CA43 | ABO | Niche | Leads | Real Estate"
 │   Objective: LEADS
 │
 └── 📁 AD SET: "CA43 | Real Estate | Cold | US-FL"
      │   Budget: $15-25/day
      │   Audience: Job titles (realtor, broker) + interests (Zillow, RE/MAX)
      │
      ├── AD: "CA43 | 8559-v1 | hook_30sec | cr_speed_lead | long"
      └── AD: "CA43 | 8559-v2 | hook_showing | cr_agents_day | long"
```

### Phase 4: Scale Winners (Week 3+) — Switch to CBO

```
📁 CAMPAIGN: "CA43 | CBO | Scale | Leads | Proven"
 │   Objective: LEADS
 │   Budget: $100-200/day CAMPAIGN level (CBO)
 │   Note: Only put PROVEN winners in here
 │
 ├── 📁 AD SET: "CA43 | Scale | Broad-US" (winning ads from testing)
 ├── 📁 AD SET: "CA43 | Scale | LAL-Converters" (lookalike of people who booked)
 └── 📁 AD SET: "CA43 | Scale | Broad-UK-AU" (geo expansion)
```

---

## Naming Convention

### Format

```
{CampaignCode} | {Level-Specific Info} | {Key Details}
```

### Campaign Names
```
CA43 | {Budget_Type} | {Phase} | {Objective} | {Audience_Temp}
```
Examples:
- `CA43 | ABO | Testing | Leads | Cold`
- `CA43 | ABO | Retargeting | Leads | Warm`
- `CA43 | CBO | Scale | Leads | Proven`

### Ad Set Names
```
CA43 | {Angle} | {Audience_Type} | {Geo}
```
Examples:
- `CA43 | Setup Is Hell | Cold | US-UK-AU-CA`
- `CA43 | Anti-Wrapper | Retarget | Engaged-Not-Booked`
- `CA43 | Real Estate | Cold | US-FL`

### Ad Names
```
CA43 | {MessageID}-v{Num} | {Hook_Short} | {Creative_Short} | {Copy_Length}
```
Examples:
- `CA43 | 8555-v1 | hook_terminal | cr_terminal_horror | long`
- `CA43 | 8556-v4 | hook_quick_q | cr_red_alert | dm`

**Why this works:**
- `CA43` = instantly know it's campaign 43 (ClawAgents.dev)
- `8555-v1` = maps directly to message ID 8555, variation 1 in Supabase
- Hook + Creative short names = know what's being tested at a glance
- `long`/`short`/`dm` = copy format

---

## Upload Methods (Ranked by Speed-to-Launch)

### Option 1: Manual in Ads Manager (RECOMMENDED FOR LAUNCH)

**Why:** You have 10 ads across 3 ad sets. That's totally manageable manually. Gets you live fastest. Learn the platform before automating.

**Steps:**
1. Go to Ads Manager → Create Campaign
2. Select objective: **Leads** (for booking ads) or **Messages** (for DM trigger ads)
3. Set budget type: **Ad Set Budget** (ABO)
4. Create ad sets with targeting from the spec
5. Create ads using copy assembled from `ad_components`
6. Upload image creatives (Canva → export → upload)
7. Set to **Review** → Facebook approves → Go live

**Time:** ~1-2 hours for all 10 ads across 3 ad sets.

### Option 2: Bulk Import via Spreadsheet (WEEK 2+)

**Why:** When you need to create 20+ variants or spin up new angles fast.

**Steps:**
1. In Ads Manager → **Export & Import** → **Download Template**
2. Fill in the CSV with campaign/ad set/ad rows
3. Upload → Facebook creates everything as drafts
4. Review → Publish

**Key CSV columns:**

| Column | Maps To | Example |
|--------|---------|---------|
| Campaign Name | — | `CA43 \| ABO \| Testing \| Leads \| Cold` |
| Campaign Objective | — | `OUTCOME_LEADS` |
| Buying Type | — | `AUCTION` |
| Campaign Status | — | `PAUSED` (start paused, review first) |
| Ad Set Name | — | `CA43 \| Setup Is Hell \| Cold \| US-UK-AU-CA` |
| Daily Budget | budget.daily_start | `25` |
| Start Date | — | `02/18/2026` |
| Countries | targeting.geo | `US,GB,AU,CA` |
| Age Min | — | `25` |
| Age Max | — | `55` |
| Interests | targeting.interests | `artificial intelligence,automation` |
| Optimization Goal | — | `OFFSITE_CONVERSIONS` or `REPLIES` |
| Ad Name | — | `CA43 \| 8555-v1 \| hook_terminal \| cr_terminal_horror \| long` |
| Body | assembled primary text | (full ad copy from components) |
| Title | headline component | `Stop Fighting Docker...` |
| Link Description | description component | `OpenClaw setup done right...` |
| Call To Action | cta_button component | `BOOK_NOW` |
| Website URL | landing page | `https://calendly.com/...` |
| Image File Name | creative asset | `setup-is-hell-terminal-horror.png` |

**Future automation:** The `ad-engine` skill can auto-generate this CSV from the database using the assembly query in `AD_ENGINE_SPEC.md`.

### Option 3: Marketing API (MONTH 2+)

**Why:** Full programmatic control. Auto-create variants, auto-pause losers, auto-scale winners.

**Requirements:**
- Facebook Developer Account + App
- `ads_management` + `ads_read` permissions
- Access token (long-lived)
- Python SDK: `pip install facebook-business`

**API Object Creation Order:**
```python
# 1. Create Campaign
campaign = AdAccount.create_campaign(
    name="CA43 | ABO | Testing | Leads | Cold",
    objective="OUTCOME_LEADS",
    status="PAUSED",
    special_ad_categories=[]
)

# 2. Create Ad Set (per angle)
ad_set = campaign.create_ad_set(
    name="CA43 | Setup Is Hell | Cold | US-UK-AU-CA",
    daily_budget=2500,  # cents
    billing_event="IMPRESSIONS",
    optimization_goal="LEAD_GENERATION",
    targeting={
        "geo_locations": {"countries": ["US","GB","AU","CA"]},
        "age_min": 25,
        "age_max": 55,
        "interests": [{"id": "...", "name": "Artificial intelligence"}],
        "exclusions": {"interests": [{"id": "...", "name": "DevOps"}]}
    }
)

# 3. Upload Image → Get image_hash
image = AdAccount.create_ad_image(filename="terminal-horror.png")

# 4. Create Ad Creative
creative = AdAccount.create_ad_creative(
    name="8555-v1-creative",
    object_story_spec={
        "page_id": "YOUR_PAGE_ID",
        "link_data": {
            "message": "ASSEMBLED_PRIMARY_TEXT",
            "link": "https://calendly.com/...",
            "name": "Stop Fighting Docker...",
            "description": "OpenClaw setup done right...",
            "call_to_action": {"type": "BOOK_NOW"},
            "image_hash": image["hash"]
        }
    }
)

# 5. Create Ad (links creative to ad set)
ad = ad_set.create_ad(
    name="CA43 | 8555-v1 | hook_terminal | cr_terminal_horror | long",
    creative={"creative_id": creative["id"]},
    status="PAUSED"
)
```

**This becomes the `ad-engine` skill later.**

---

## Campaign Objective Selection

| Ad Type | Objective | Optimization | Why |
|---------|-----------|-------------|-----|
| Setup Is Hell | **Leads** | Conversions (booking) | We want Calendly bookings |
| Security Audit (LP version) | **Leads** | Conversions (booking) | Same — book a call |
| Security Audit (DM version) | **Messages** | Replies | We want "AUDIT" DMs |
| Anti-Wrapper | **Leads** | Conversions (booking) | Retarget to booking |
| DM Trigger | **Messages** | Replies | We want "SETUP" DMs |
| Real Estate | **Leads** | Conversions (booking) | Book a call |

**Important:** The DM-based ads (Security Audit v4, DM Trigger) need a **Messages** objective, not Leads. This means they need their own campaign (you can't mix objectives within a campaign).

### Updated Campaign Split

```
Campaign 1: "CA43 | ABO | Testing | Leads | Cold"
  → Ad Sets: Setup Is Hell, Security Audit (LP versions only)

Campaign 2: "CA43 | ABO | Testing | Messages | Cold"
  → Ad Sets: DM Trigger, Security Audit (DM versions only)

Campaign 3: "CA43 | ABO | Retargeting | Leads | Warm"
  → Ad Sets: Anti-Wrapper

Campaign 4: "CA43 | ABO | Niche | Leads | Real Estate" (week 3+)
  → Ad Sets: Real Estate
```

---

## Testing Protocol

### Week 1: Launch & Learn

| Day | Action | Budget |
|-----|--------|--------|
| 1 | Launch Campaign 1 (Leads) + Campaign 2 (Messages) — all ads PAUSED | $0 |
| 1 | Review everything, then unpause | ~$65/day |
| 2-3 | Monitor: CTR, CPC, CPM. Don't touch anything yet | ~$65/day |
| 4 | **Kill** any ad with <0.8% CTR after $30+ spend | ~$55/day |
| 5-6 | **Increase** budget 20% on ad sets with >1.5% CTR | ~$70/day |
| 7 | Full review: DMs received, calls booked, cost per lead | — |

### Week 1 Kill/Scale Rules

| Metric | Action |
|--------|--------|
| CTR < 0.8% after $30 spend | Kill the ad |
| CTR > 1.5% | This is a winner — keep running |
| CPC > $5 | Kill unless CTR is high (audience might be expensive) |
| CPM > $30 | Audience too expensive or too narrow — broaden targeting |
| 0 leads after $50 spend | Kill the entire ad set |
| 3+ leads from an ad set | This angle works — create more variants |

### Week 2: Optimize & Retarget

| Day | Action |
|-----|--------|
| 8 | Launch Campaign 3 (Anti-Wrapper retargeting) |
| 8 | Create 2-3 new variants of winning ads (swap one component) |
| 9-12 | Run new variants alongside winners |
| 13-14 | Identify the single best ad per angle |

### Week 3+: Scale

| Action | How |
|--------|-----|
| Move winners to CBO campaign | Create Campaign 5 with CBO, move winning ads |
| Increase budget gradually | 20% every 2-3 days (don't spike — resets learning phase) |
| Build lookalikes | Create LAL audience from people who booked calls |
| Launch niche campaign | Campaign 4 (Real Estate) if first client closed |
| Expand geo | Add new ad sets for different countries |

---

## Creative Asset Requirements

### Image Specs

| Spec | Requirement |
|------|------------|
| Format | JPG or PNG |
| Resolution | 1080 × 1080 (square — works on FB + IG feed) |
| Alt: | 1080 × 1920 (stories/reels — create separate if budget allows) |
| Text on image | Keep under 20% (no longer enforced but affects delivery) |
| File size | Under 30 MB |

### Quick Creative Workflow

1. Open Canva → FB Ad template (1080×1080)
2. Use the `creative_direction` text from `ad_components` as the brief
3. Export as PNG
4. Name file: `{ad_angle}-{creative_key}.png` (e.g., `setup_is_hell-cr_terminal_horror.png`)
5. Upload to Ads Manager

### Creatives Needed for Launch (10 images)

| # | File Name | Creative Key | Ad Angle |
|---|-----------|-------------|----------|
| 1 | `setup_is_hell-cr_terminal_horror.png` | cr_terminal_horror | Setup Is Hell |
| 2 | `setup_is_hell-cr_time_wasted.png` | cr_time_wasted | Setup Is Hell |
| 3 | `setup_is_hell-cr_the_quote.png` | cr_the_quote | Setup Is Hell |
| 4 | `security_audit-cr_red_alert.png` | cr_red_alert | Security Audit |
| 5 | `security_audit-cr_exposed.png` | cr_exposed | Security Audit |
| 6 | `security_audit-cr_cve_warning.png` | cr_cve_warning | Security Audit |
| 7 | `dm_trigger-cr_checklist_preview.png` | cr_checklist_preview | DM Trigger |
| 8 | `dm_trigger-cr_simple_bold.png` | cr_simple_bold | DM Trigger |
| 9 | `anti_wrapper-cr_graveyard.png` | cr_graveyard | Anti-Wrapper |
| 10 | `anti_wrapper-cr_hosted_vs_own.png` | cr_hosted_vs_own | Anti-Wrapper |

---

## Pixel & Tracking Setup

### Before Any Ads Go Live

1. **Facebook Pixel** — Install on Calendly thank-you page (or redirect page after booking)
2. **Conversions API (CAPI)** — Server-side tracking for iOS accuracy (Calendly supports this natively)
3. **Custom Conversions** — Create event for "booking_confirmed"
4. **UTM Parameters** — Append to every landing URL:
   ```
   ?utm_source=facebook&utm_medium=paid&utm_campaign=ca43_testing&utm_content={{ad.name}}
   ```
   The `{{ad.name}}` dynamic parameter auto-inserts the ad name, which maps back to your message ID.

5. **URL Parameter Template** in Ads Manager:
   ```
   utm_source=facebook&utm_medium=cpc&utm_campaign={{campaign.name}}&utm_content={{ad.name}}&utm_term={{adset.name}}
   ```

### Tracking Loop: Facebook → Supabase

After ads run, update performance data back to the database:

```sql
-- Update the message with FB metrics
UPDATE messages SET
    quality_scores = '{"ctr": 1.82, "cpc": 2.14, "cpl": 22.50, "impressions": 8500, "clicks": 155, "leads": 7}',
    status = 'active'
WHERE id = 8555;

-- Update individual component performance
UPDATE ad_components SET
    performance_data = '{"impressions": 8500, "ctr": 1.82, "wins": 1, "losses": 0, "last_updated": "2026-02-24"}'::jsonb
WHERE component_key = 'hook_terminal_stare';
```

This closes the loop: **DB components → assembled ads → Facebook → performance data → back to DB → inform next variants.**

---

## Pre-Launch Checklist

### Must Have (Day 0)

- [ ] Facebook Business Manager account
- [ ] Ad Account created inside Business Manager
- [ ] Facebook Page connected (page to run ads from)
- [ ] Payment method added to ad account
- [ ] Facebook Pixel created
- [ ] Calendly booking page live (or Cal.com)
- [ ] Pixel installed on booking confirmation page
- [ ] 10 image creatives designed in Canva (see list above)

### Nice to Have (Day 1-3)

- [ ] Conversions API (CAPI) set up for server-side tracking
- [ ] Custom conversion event for "booking_confirmed"
- [ ] Simple landing page between ad and Calendly (for pixel + copy)
- [ ] ManyChat connected for DM automation ("SETUP" and "AUDIT" triggers)

### Later (Week 2+)

- [ ] Custom audiences built from pixel data
- [ ] Lookalike audiences from converters
- [ ] Video versions of winning image ads
- [ ] Retargeting campaign launched

---

## Quick-Start: Fastest Path to Ads Live

**If you want ads running TODAY, here's the minimum path:**

1. Open Facebook Business Manager → create ad account if needed
2. Create a Facebook Page for ClawAgents (if not already)
3. Set up Calendly booking page (free tier works)
4. Design 4 images in Canva (2 for Setup Is Hell, 2 for Security Audit) — 30 min
5. In Ads Manager, create Campaign 1 (Leads, ABO)
6. Create 2 ad sets (Setup Is Hell + Security Audit) at $25/day each
7. Create 2 ads per ad set using copy from `ad_components`
8. Set status to PAUSED → review everything → unpause
9. Total: 4 ads, $50/day, live in ~2 hours

**Skip for now:** DM Trigger (needs Messages campaign), Anti-Wrapper (needs retargeting data), Real Estate (needs proof).

---

## Sources

- [CBO vs ABO Best Practices 2026](https://adsuploader.com/blog/abo-vs-cbo)
- [Facebook Campaign Structure Best Practices](https://www.adstellar.ai/blog/facebook-campaign-structure-best-practices)
- [Facebook Ad Naming Conventions Guide](https://motionapp.com/blog/facebook-naming-conventions)
- [Bulk Facebook Ad Creation Guide](https://adsuploader.com/blog/facebook-ads-bulk-uploads)
- [Meta Ads API Complete Guide](https://admanage.ai/blog/meta-ads-api)
- [Ad Creative Naming Conventions](https://admanage.ai/blog/ad-creative-naming-conventions)
