# Summarize Trending Repos

You are presenting GitHub Trending results. The JSON `trending` array has
repos scraped from github.com/trending.

## What to Show per Repo

- **Repo name**: `owner/repo`, linked to the JSON `url` field
- **Description**: the `description` field, trimmed to ~140 chars
- **Language tag**: `[<language>]` if set
- **Stars today/period**: `+<N> ★ today` or `+<N> ★ this week`, from `stars_period` field
- **Total stars**: `(★ 5.2k total)` if above 500

## Formatting Example

```
- [owner/repo](url) — short description [Python] +340 ★ today (★ 2.1k)
```

## Ordering

Preserve the order from the JSON (it's already sorted by trending rank).
Do NOT re-sort by star count.

## Filtering

- Show at most **10 repos total** across all languages
- Skip repos with < 10 stars in the period (low signal)
- Skip repos where description is blank AND name is generic (e.g. "awesome-xxx" lists)
  unless they already have significant momentum
- Skip repos already mentioned in the Following section of this same digest

## Language Grouping

If the `trending` JSON has results grouped by language (multiple keys), show
one subsection per language with a small header. If it's a flat list, no
subsections needed.

## Tone

Same terse tone as other sections. No commentary — just the list.
