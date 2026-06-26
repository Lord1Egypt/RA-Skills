# Commands

## Trigger

Input must start with `mail` (case-insensitive) to be parsed by this skill.

## Quick syntax

```text
mail <query> [keyword|semantic|hybrid] [max N|top N|limit N|limite N] [label <prefix>|tag <prefix>] [after <date>] [before <date>] [between <date> and <date>] [resume]
```

## Useful examples

```text
mail invoice max 5
mail on-demand cargo label finance/receivables
mail crew roster between 2025-01 and 2025-03 resume
mail recents top 10
mail status
mail labels
mail sync
```

## Date formats

Accepted date formats:

- `YYYY`
- `MM/YYYY`
- `YYYY-MM`
- `YYYY-MM-DD`

`between` converts to `after` + exclusive `before` bounds:

- `between 2025 and 2025` -> `after=2025-01-01`, `before=2026-01-01`
- `between 2025-02 and 2025-03` -> `after=2025-02-01`, `before=2025-04-01`

## Operational commands

- `mail help`
- `mail recents [max N|top N|limit N|limite N]`
- `mail status` (`mail stat` also accepted)
- `mail labels` (`mail label` also accepted)
- `mail sync`

## Sender/recipient operators

Dedicated parser flags `from` and `to` are not implemented.

Use backend query operators inside `<query>` when available, e.g.:

```text
mail from:alice@example.com to:me subject:contract max 5
```

## Output style

For search results, include:

1. Date
2. Sender
3. Subject
4. Short snippet
5. Stable reference/permalink (if available)
