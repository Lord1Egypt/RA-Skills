# Eir Interest Rules

> **Eir Mode Only** — This document describes curation behavior when connected to the Eir API.

Curation guidelines for the content curator agent.

## Your Job

1. **Read directives**: `GET /oc/curation` → topics to find content for
2. **Find content**: Search using `searchHints` from each directive
3. **Push content**: `POST /oc/content`
4. **Discover interests**: From conversations → `POST /oc/interests/add`

## Curation Tiers

| Tier | Description | Quality Expectation |
|------|-------------|---------------------|
| **tracked** | User explicitly follows | Highly relevant, timely |
| **focus** | Strong interest signal | Relevant + quality |
| **explore** | Moderate interest | Quality threshold applies |
| **seed** | Discovery topics | Must be excellent to justify |

The API returns a curated subset of topics per tier. Server-side filtering already applied:
- Topics in cooldown are excluded
- Quotas adjusted based on user engagement history

## Content Selection

For each candidate, evaluate:
- **Relevance** to the directive's topic
- **Source authority** — trusted, primary sources preferred
- **Freshness** — match the directive's `freshness` (1d = within 24h, 7d = within week)
- **Depth** — substantial, not thin listicles
- **Novelty** — not duplicating recently pushed content

**Quality bar by tier:**
- tracked: relevant + timely
- focus/explore: relevant + quality source
- seed: must be exceptional to earn attention

## Using Directives

Each directive contains:
- `slug` — topic identifier (use as `interests.anchor`)
- `label` — display name
- `tier` — priority level
- `freshness` — recency requirement ("1d", "2d", "3d", "7d", "14d")
- `searchHints` — 2-3 search queries to find content
- `userNeeds` — guidance on what the user wants (may be null)
- `trackingGoal` — specific goal for tracked topics (may be null)

**Search strategy:**
- Use `searchHints` directly as search queries
- For freshness "1d"-"3d": prioritize news, announcements, releases
- For freshness "7d"+: mix news with analysis, insights, perspectives
- Respect `userNeeds` when selecting content angles

## Interest Anchors on Content

Every content item MUST include:

```json
"interests": {
  "anchor": ["ai-agents"],
  "related": [
    { "slug": "a2a-protocol", "label": "A2A Protocol" }
  ]
}
```

**Anchor rules:**
- 1-3 slugs from the curation directives
- Must match user's interests (API validates, rejects 400 if mismatch)

**Related topics:**
- 2-5 adjacent topics
- Unknown topics auto-created as candidates
- Drive "Explore More" on detail pages

## Exclusions

The API returns `exclude.disliked` — slugs to filter out during content selection.

## Adding Interests

From conversations:
```
POST /oc/interests/add
{ "labels": ["AI Agents", "MCP"], "lang": "en" }
```

Server matches to dictionary. Unknown labels flagged for review.

## Best Practices

1. **Quality over quantity** — if nothing good, push nothing
2. **Max 2 items per topic group** unless exceptional
3. **Seed topics**: adjacent to existing interests, not random
4. **Use `GET /oc/sources`** for URL dedup
5. **Never override** user's explicit tracking decisions
