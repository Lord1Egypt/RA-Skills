# Segmentation Theory — Framework

Loaded when the conversation involves audience segmentation, targeting, list strategy, or "who should I send to?" questions. Connects segmentation theory to AC-specific implementation.

## Core principle

Send the right message to the right people at the right time. Segmentation is how you define "right people." Everything else in email marketing is downstream of this.

## AC segmentation primitives

AC has three mechanisms for grouping contacts. They serve different purposes:

| Primitive | Use when | Example |
|---|---|---|
| **Lists** | Broad permission groups. A contact opted in to receive a category of email. | "Newsletter", "Product Updates", "Event Invites" |
| **Tags** | Flexible labels. Attach and remove as behavior changes. | "VIP", "Trial User", "Attended Webinar", "Cart Abandoner" |
| **Segments** | Dynamic queries. AC re-evaluates membership continuously. | "Opened email in last 30 days AND has tag Customer" |

### When to use each

- **Lists** = consent boundary. Use for things the contact chose ("I want your newsletter"). Don't use for behavioral grouping.
- **Tags** = behavioral or categorical labels. Use for things YOU observe ("this person is a customer", "this person abandoned cart"). Tags are fast to apply/remove via API.
- **Segments** = compound conditions. Use when you need AND/OR logic across multiple attributes. Segments are read-only in the API — build them in the AC UI.

### Common anti-pattern

Using lists for everything ("Engaged List", "VIP List", "Re-engagement List"). This creates management overhead and double-subscription issues. Use tags for behavioral labels, lists for permission groups.

## RFM segmentation

Recency, Frequency, Monetary — the classic segmentation framework. Maps directly to AC data:

| Dimension | AC data source | How to compute |
|---|---|---|
| **Recency** | Last email open date, last site visit, last conversion | Query contacts, sort by last activity. API: filter by `updated_after`. |
| **Frequency** | Number of conversions, email opens over time | Ecommerce API for conversions. Campaign activity for engagement counts. |
| **Monetary** | Deal values, order totals | Deals API (`value` field, in cents). Ecommerce API for order totals. |

### RFM scoring in AC

Score each dimension 1-5 (5 = best). Combine into a composite:

| Score | Recency | Frequency | Monetary |
|---|---|---|---|
| 5 | Active in last 7 days | 10+ interactions in 90 days | Top 20% by value |
| 4 | Active in 8-30 days | 5-9 interactions | 60-80th percentile |
| 3 | Active in 31-60 days | 3-4 interactions | 40-60th percentile |
| 2 | Active in 61-90 days | 1-2 interactions | 20-40th percentile |
| 1 | 90+ days inactive | 0 interactions in 90 days | Bottom 20% |

Implementation: use AC's built-in lead scoring to approximate RFM, or compute externally and store as a custom field (e.g., "RFM Score" = "5-4-3").

## Lifecycle segmentation

Where is the contact in their journey?

| Stage | Definition | AC implementation |
|---|---|---|
| **Subscriber** | Signed up, hasn't converted or started trial | Tag: `subscriber`, no `customer` or `trial` tag |
| **Lead** | Showing intent (visited pricing, downloaded content) | Tag: `lead` or score above threshold |
| **Trial** | Active trial user | Tag: `trial-active` + custom field: trial start date |
| **Customer** | Paying customer | Tag: `customer` + deal in Won status |
| **Advocate** | High NPS, referrals, case study participant | Tag: `advocate` |
| **Churned** | Former customer, canceled | Tag: `churned` + deal in Lost status |
| **Dormant** | No engagement in 90+ days regardless of stage | Computed by `scripts/audit_list_health.py` |

Use automations to move contacts between lifecycle stages based on triggers (deal won → add `customer` tag, remove `trial-active` tag).

## Engagement-based segmentation

The most important segmentation for deliverability. Group by how recently they engaged:

| Tier | Definition | Action |
|---|---|---|
| **Hot** | Opened/clicked in last 30 days | Full send frequency |
| **Warm** | Opened in 31-60 days | Standard frequency, watch for decay |
| **Cool** | Opened in 61-90 days | Reduced frequency, high-value content only |
| **Cold** | No opens in 91-180 days | Re-engagement campaign, then suppress |
| **Dead** | No opens in 180+ days | Suppress. They're hurting deliverability. |

This tiering maps directly to the `scripts/audit_list_health.py` output.

**Implementation:** AC doesn't expose per-contact "last open date" reliably via API. Workarounds:
1. Use AC's built-in engagement scoring (if enabled) — available via `scoreValues` endpoint
2. Use automation + tags: automation triggers on email open → applies `engaged-30d` tag, removes after 30 days
3. Use webhooks to capture opens in real-time and store the timestamp as a custom field

## Pre-built segment recipes

These are the segments every marketer rebuilds. Parameterized for your account using `state.json` taxonomy.

### Engagement segments

```
# Engaged last 30 days (use AC segment builder or tag-based)
Tag: engaged-30d

# Dormant 90+ days
NOT tag: engaged-30d AND NOT tag: engaged-60d AND NOT tag: engaged-90d

# Never engaged (signed up 90+ days ago, never opened)
Created before [90 days ago] AND score < [threshold]
```

### Customer segments

```
# Active customers
Tag: customer AND NOT tag: churned

# High-value customers
Tag: customer AND deal value > [threshold from state.json baselines]

# At-risk customers (customer + engagement dropping)
Tag: customer AND NOT tag: engaged-30d

# Recently churned (lost deal in last 30 days)
Tag: churned AND deal status: lost AND deal mdate: last 30 days
```

### Prospect segments

```
# Hot leads
Score > [p75 from state.json] AND NOT tag: customer

# Trial users about to expire
Tag: trial-active AND custom field "trial_end_date" within 7 days

# Pricing page visitors (requires automation + tag)
Tag: viewed-pricing AND NOT tag: customer AND created in last 30 days
```

### Lifecycle triggers

```
# New subscribers (first 14 days)
Created after [14 days ago] AND tag: subscriber AND NOT tag: customer

# Win-back candidates
Tag: churned AND last activity 30-90 days ago

# Upsell candidates
Tag: customer AND custom field "Plan" = "Pro" AND deal value > [median]
```

## Combining segments with recipes

| If user asks... | Segment to build | Then use recipe |
|---|---|---|
| "Who should I send the newsletter to?" | Engaged last 60 days | — (direct send) |
| "Who should get a re-engagement email?" | Cold tier (91-180 days) | `recipes/welcome-series.md` variant |
| "Who are my best upsell targets?" | Customers on lower plan with high engagement | — (manual outreach) |
| "Clean up my list" | Dead tier (180+ days) + hard bounces | `recipes/list-health-audit.md` |
| "Who are my hottest leads?" | High score, recent activity, not yet customer | `scripts/find_hot_leads.py` |

## Segmentation anti-patterns

- **Over-segmenting**: Don't create 50 micro-segments with 20 contacts each. Minimum viable segment: 200+ contacts.
- **Static-only**: Tags without automation = stale labels. Use automations to keep tags current.
- **Ignoring engagement**: Sending to your "full list" including dormants will kill deliverability. Always filter by engagement.
- **Demographic-only**: "All VPs in California" ignores intent. Combine demographic + behavioral.
- **Third-party lists**: Acquired lists destroy sender reputation. Period. No segment design fixes this.

## Related files

- `scripts/audit_list_health.py` — computes engagement tiers
- `scripts/find_hot_leads.py` — scores and ranks leads
- `recipes/list-health-audit.md` — full list diagnostics
- `frameworks/email-best-practices.md` — what to send once you know who
- `references/contacts.md` — contact filtering API
