---
name: fork-it
description: Before the user starts coding a new project idea, search GitHub for an existing repo to fork as a starting point. Skip for debugging, learning, or a specific algorithm/function.
metadata:
  openclaw:
    emoji: ""
    category: "research"
    tags: ["github", "opensource", "fork", "remix", "jumpstart"]
invoke: /fork-it
---

# fork-it

Method: search GitHub before building from scratch, fork the closest match, then make it yours.

## Language
Reply in the user's language. Script output is language-neutral (English repo data); translate names, descriptions, and your commentary when presenting.

## When to use
- User wants to build / create / make something new (any language), or invokes `/fork-it`.
- **Skip** when: debugging or fixing existing code, learning/teaching, asking about a specific function/algorithm/regex, or they've already chosen a base project.

## Workflow
1. **Search** with their keywords:
   ```bash
   node scripts/github-search.mjs "keywords" --language js --min-stars 50 --limit 5
   ```
2. **Analyze** each result by fit:
   - Great match → fork & customize
   - Partial match → fork & extend (add the missing piece)
   - Reference only → study the approach, then build your own
   - Nothing fits → build fresh
3. **Recommend** the best 1–3 candidates (stars / language / what it gives them) with the suggested path. If nothing fits, say so and encourage a from-scratch build.
4. **Details on demand** — when the user leans toward one repo, fetch more with:
   ```bash
   node scripts/repo-detail.mjs "owner/repo"
   ```

## Notes
- Format `stars` as `12.3k`, `pushed_days_ago` as "3 days ago". Full JSON shape and all flags: `references/schema.md`.
- Rate limit: 60/hr unauthenticated, 5000/hr with `GITHUB_TOKEN`. Set it if searches start failing.
