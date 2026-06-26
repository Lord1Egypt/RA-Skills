---
name: blog-embargo
version: 1.0.1
description: Coordinate publishAt embargo timing across blog index visibility and
  social post scheduling. Ensures blog posts don't appear in the index before social
  posts are queued, and social posts don't fire before the post is indexed.
author: loki
tags:
- content
- publishing
- buffer
- social
- embargo
created: 2026-04-03
lesson-source: ollama-embeddings + portkey-patterns PRs merged without publishAt,
  posts live before social was scheduled
metadata:
  openclaw:
    emoji: 🚦
---

# Blog Embargo Skill

## Why This Exists

The blog uses a `publishAt` frontmatter field to support soft embargoes: post deploys to Vercel immediately on merge but is hidden from the blog index (`/blog` listing) until `publishAt` passes. The index revalidates hourly.

Without this field, posts are indexed immediately on deploy. If social posts aren't already in Buffer before the merge, you get a window where the post is live but no social amplification is queued.

**This skill coordinates the three moving parts:**
1. `publishAt` in MDX frontmatter (blog index gate)
2. `--publish-at` in `convert-to-mdx.py` (how to set it)
3. Buffer scheduling at `publishAt + 15 min` (social timing)

---

## The Rule

> **Blog index visibility and social posts must be coordinated. Always decide `publishAt` before raising the PR.**

| Scenario | publishAt | Buffer timing |
|---|---|---|
| Want coordinated launch (blog + social together) | Set to future slot | Schedule Buffer at publishAt + 15 min |
| Post can go live now, social later same day | Set to now + 30 min | Schedule Buffer at publishAt + 15 min |
| No embargo needed (emergency fix, no social) | Omit or set to now | Post immediately |

---

## Step-by-Step

### 1. Decide the publish time

Before raising the PR, decide a specific AEST datetime:
- Check Buffer queue for conflicts (use Buffer dashboard or GraphQL query)
- Align with content calendar (LinkedIn 10am AEST, X 8-9am AEST preferred slots)
- Minimum: now + 30 min (enough time to schedule Buffer before deploy)

```
publishAt = "2026-04-04T09:00:00+11:00"   # AEDT
publishAt = "2026-04-04T09:00:00+10:00"   # AEST
```

### 2. Set publishAt in MDX

Pass `--publish-at` to `convert-to-mdx.py`:

```bash
python3 scripts/blog/convert-to-mdx.py \
  --input projects/blog-pipeline/converted/<slug>.md \
  --output projects/blog-pipeline/converted/<slug>.mdx \
  --slug <slug> \
  --title "<title>" \
  --description "<description>" \
  --tags "<tags>" \
  --author "Nissan Dookeran" \
  --publish-at "2026-04-04T09:00:00+11:00"
```

**Check:** MDX frontmatter should contain `publishAt: "2026-04-04T09:00:00+11:00"`.

### 3. Raise PR and merge

Post deploys immediately. Direct URL (`/blog/slug`) resolves. Blog index (`/blog`) hides the post until publishAt.

### 4. Schedule Buffer at publishAt + 15 min

After merge, schedule social posts with `dueAt = publishAt + 15 min`:

```bash
# X/Twitter — at publishAt + 15 min
node scripts/buffer-post.mjs \
  --text "$(cat projects/social-growth/thread-<slug>.md | ...)" \
  --channel twitter \
  --publish-at "2026-04-04T09:15:00+11:00"

# LinkedIn — same time or later slot
node scripts/buffer-post.mjs \
  --text "$(cat projects/social-growth/linkedin-<slug>.md | ...)" \
  --channel linkedin \
  --publish-at "2026-04-04T09:15:00+11:00"
```

Or use the batch file approach with `scripts/buffer-post.mjs --file posts.json`.

### 5. Verify

- Direct URL resolves immediately after merge ✅
- Blog index shows post only after publishAt ✅
- Buffer shows posts scheduled at publishAt + 15 min ✅

---

## Recovery: Post Already Live Without publishAt

If a post was merged without `publishAt` and is already indexed:

1. The embargo window is gone — post is already visible
2. Schedule social posts for the next appropriate slot (same day if possible)
3. Don't backdate social posts to before the post went live
4. Note the gap in the daily memory log

This happened with:
- `ollama-embeddings` (2026-04-03) — live, no social queued
- `portkey-patterns` (2026-04-03) — live, no social queued

---

## How publishAt Works (Technical)

- `publishAt` is an ISO8601 field added to MDX frontmatter
- The blog index page (`/blog`) filters posts where `publishAt > now`
- The `export const revalidate = 3600` means the index updates hourly
- Direct slug URL (`/blog/slug`) always resolves — no gate at the page level
- `convert-to-mdx.py` sets both `publishAt` and aligns the `date` field when `--publish-at` is provided

---

## Integration Points

- **Playbook:** `playbooks/blog-publish/PLAYBOOK.md` — Step 0b (Embargo Gate) uses this skill
- **Script:** `scripts/blog/convert-to-mdx.py` — `--publish-at` flag
- **Script:** `scripts/buffer-post.mjs` — `--publish-at` flag or `publishAt` in batch JSON
- **Buffer channels:** X `69c29939af47dacb694d3d1f`, LinkedIn `69c29382af47dacb694d24b4`

---

## Lessons Learned

**2026-04-03:** Two posts (ollama-embeddings, portkey-patterns) merged without publishAt. Both immediately indexed. Social copy existed but hadn't been approved yet, so nothing was in Buffer. Result: posts live with no social amplification window. Fix: this skill + mandatory Step 0b in blog-publish playbook.
