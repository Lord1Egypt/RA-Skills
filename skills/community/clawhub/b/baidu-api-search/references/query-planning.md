# Query Planning

Use this reference before changing query expansion behavior.

## Principle

Do not rely on free-form AI guessing alone. Use a priority-ordered query plan:

```text
seed templates
-> coverage templates
-> platform templates
-> optional AI/user expansions
-> result-driven second pass
-> coverage feedback
```

## Modes

```text
fast:
  1 query
  low-cost discovery

normal:
  5-12 queries
  default mode

deep:
  10-30 queries
  add second-pass terms when available
```

The planner assigns every query an `intent`, `stage`, and `priority`. It must select by diversity slots first, then fill remaining slots by priority. Do not simply append templates and truncate; that wastes calls on similar intents while missing official/platform/complaint coverage.

## Template Classes

Base queries cover:

```text
overview
review
complaint
price
experience
forum
platform
comparison
service
```

High-priority default order:

```text
overview
review
complaint
official
platform-specific sources early enough for normal mode
experience / owner reports
quality
price
forum
comparison
```

Product-like topics add:

```text
owner reports
fuel/range/specs
used market
maintenance
quality/common defects
```

Event-like topics add:

```text
latest
timeline
official notice
follow-up
controversy
cause/impact
```

Project/API-like topics add:

```text
official docs
GitHub
issues
bugs
alternatives
tutorials
```

## Result-Driven Expansion

After a first pass, extract terms from titles/snippets:

```text
entities
competitors
platform names
failure words
organization names
model/version names
regions
```

Then create second-pass queries:

```text
{topic} {new_entity}
{topic} {new_issue}
{topic} {competitor} 对比
{topic} {platform}
```

The v1 script accepts `--extra-terms` as a JSON list. Later versions can add automatic term extraction.

`adaptive_search.py` already performs lightweight term extraction in deep mode and inserts a small number of result-driven expansion queries.

## Coverage Feedback

Stop expanding a query family when the unique URL yield drops below roughly 20%. Add targeted queries when an intent is missing, for example no official source, no complaints, or no forum source.
