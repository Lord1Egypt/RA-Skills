# Summarize Hot New Projects

You are presenting recently-created repos that are gaining stars fast. The
JSON `hot` array comes from GitHub Search API: repos created in the last
N days with significant stars.

## Signal

This section surfaces "new things worth knowing about" — not established
projects, but genuinely new repos that are taking off. Different from Trending
(which includes old repos having a momentum spike).

## What to Show per Repo

- **Repo name**: `owner/repo`, linked
- **Age**: "created N days ago" if < 14 days old
- **Total stars**: `★ 1.2k` — this matters here because all repos are new
- **Language tag**: `[<language>]` if set
- **Description**: one-sentence description

## Formatting Example

```
- [owner/repo](url) — description of what it does [Rust] ★ 2.1k (created 5 days ago)
```

## Ordering

Sort by `stars` descending (already pre-sorted by the fetcher, just preserve order).

## Filtering

- Show at most **5 repos** in this section
- Skip repos with blank descriptions
- Skip obvious joke/tutorial/template repos (name like "hello-world", "tutorial-xxx",
  "my-project")
- Skip repos already shown in the Following or Trending sections

## Tone

Brief. The point is to introduce the project — one sentence of what it is, not
an explanation of why it's trending.
