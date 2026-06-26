# Publish Runbook

## Pre-Publish Checklist

- [ ] Draft assembled in `publications/social/draft.md`
- [ ] Human stakeholder reviewed and approved
- [ ] Factual claims verified (no drift)
- [ ] Tone and voice consistent with SOUL.md
- [ ] Target platforms identified

## Publish Steps

1. Format for target platform (blog, social thread, article link)
2. Publish via platform-specific scripts
3. Update `ops/social/published_posts.json` with:
   - Platform(s)
   - URL(s)
   - Timestamp
   - Metrics placeholders
4. Close the source GitHub Issue with a summary comment

## Post-Publish Tracking

All published content is tracked in `ops/social/published_posts.json`:

```json
{
  "posts": [
    {
      "title": "",
      "date": "",
      "platforms": ["Moltbook", "GitHub"],
      "url": "",
      "metrics": {
        "views": null,
        "engagement": null
      }
    }
  ]
}
```
