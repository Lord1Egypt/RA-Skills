# Standup Formatting Reference

## Standard Template

```markdown
# Daily Standup — YYYY-MM-DD

## ✅ Completed
- **Alice**: Finished the login API migration
- **Bob**: Fixed the caching bug in the search service

## 📋 Planned
- **Alice**: Start work on the profile settings page
- **Bob**: Investigate the intermittent timeout issue

## 🛑 Blockers
- **Carol**: Waiting on design specs for the new dashboard
```

## Conventions

- Use one sentence per bullet.
- Attribute every item to a person (use "unknown" if unparseable).
- Merge near-duplicate items; when merged, keep the earliest/most specific phrasing.
- If a message contains both progress and a plan, split into two bullets.
- If a message contains a blocker AND completed work, extract both.

## JSON Schema

```json
{
  "completed": [{ "author": "string", "content": "string" }],
  "planned":   [{ "author": "string", "content": "string" }],
  "blockers":  [{ "author": "string", "content": "string" }]
}
```

## Slack / Discord Export

When pasting a Slack or Discord export, the parser handles lines like:

```
2024-03-15 09:01 Alice: Finished the auth refactor ✅
[09:02] Bob > Will deploy the hotfix after lunch
```

## Edge Cases

- **Emoji markers** (✅, 🚧, 🔄) are respected as signal.
- **Mixed-language messages** are handled by keyword matching in English; non-English content defaults to "completed."
- **Very long paragraphs** (>280 chars) should be manually trimmed before feeding into the script.
