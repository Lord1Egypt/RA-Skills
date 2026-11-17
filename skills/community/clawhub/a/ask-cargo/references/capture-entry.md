# The capture

What `@Cargo capture this` writes (§5 of the prompt), and what the thread sees.

## Raw file — `cadence/log/raw/slack/<YYYY-MM-DD>-<slug>.md`

```text
---
title: Northwind procurement pushback
date: 2026-10-07
channel: "#deal-rooms"
permalink: https://northwind.slack.example/archives/C0DEAL/p1759830000000100
source: slack:C0DEAL/1759830000.000100@1759834200.000400
---
2026-10-07 09:40 Dana Ruiz: Procurement asked why not Globex, it's already in their stack
2026-10-07 09:52 Sam Okafor: Same thing Fabrikam said last month
2026-10-07 10:50 Dana Ruiz: @Cargo capture this
```

The date is the thread's first message. The slug is the account (reusing the slug
`cadence/log/calls/` uses for it) or a short topic. Never edited, moved or deleted.

## Entry — `cadence/log/slack/<YYYY-MM-DD>-<slug>.md`

Same frontmatter and `source:` line. Then:

- two sentences on what the thread was about
- `## Objections`, `## Competitors mentioned`, `## Buying or expansion signals`, `## Product asks`,
  each item quoted and marked first-hand or interpretation
- `## Actions` as checkboxes, with the owner the thread names

## Re-mentions

| The archive already holds                          | Ask Cargo                                                       |
| -------------------------------------------------- | --------------------------------------------------------------- |
| the same `source:` line                            | writes nothing and replies with the existing entry              |
| the same channel and parent, older newest-reply ts | writes a new raw file and entry for the replies after it        |
| nothing for this thread                            | captures the whole thread                                       |

## Reply

At most three lines, as the turn's final text: the entry path, the context file promoted or
"nothing promoted: first occurrence", and the pull request URL. A :white_check_mark: on the
summoning message only when the push landed.
