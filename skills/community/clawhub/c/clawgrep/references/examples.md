# Examples

## Basic search

Search a directory for a concept:

```bash
clawgrep --no-color "previous discussion about auth flow" ./memory
```

Output:

```
memory/2025-06-12-auth-design.md:8:Decided to use OAuth2 with PKCE for all client auth.
memory/2025-06-12-auth-design.md:14:Token refresh should be transparent to the user.
memory/2025-06-10-planning.md:3:Auth flow is the top priority for the sprint.
memory/archive/2025-05-session-notes.md:42:Discussed moving auth to a separate service.
memory/archive/2025-05-session-notes.md:87:Need to revisit token expiry policy.
```

Results are ordered by relevance (best match first), not by file position.

## Context lines

Show surrounding text with `-C`:

```bash
clawgrep --no-color -C 2 "deployment rollback procedure" ./memory
```

Output:

```
memory/2025-07-01-incident.md-5-The deploy went out at 14:32 UTC.
memory/2025-07-01-incident.md-6-
memory/2025-07-01-incident.md:7:Rollback steps: revert the tag, re-deploy previous image, flush cache.
memory/2025-07-01-incident.md-8-Confirmed service restored at 14:58 UTC.
memory/2025-07-01-incident.md-9-Post-mortem scheduled for Friday.
```

Match lines use `:` as separator. Context lines use `-`. Identical to grep.

## Relevance scores

Append scores with `--show-score`:

```bash
clawgrep --no-color --show-score "rate limiting strategy" ./memory
```

Output:

```
memory/2025-06-20-api-design.md:18:Use token bucket for rate limiting, 100 req/min per user.	(0.912)
memory/archive/2025-05-brainstorm.md:33:Consider sliding window rate limiter.	(0.847)
```

Tab-separated score (0.0–1.0) appended to each line.

## Exact identifier search

Find a specific note ID or tag by shifting weights toward keyword:

```bash
clawgrep --no-color --keyword-weight 0.8 --semantic-weight 0.2 "PROJ-1042" ./memory
```

Output:

```
memory/2025-06-15-standup.md:4:Picked up PROJ-1042, needs design review first.
memory/2025-06-18-review.md:12:PROJ-1042 approved with minor changes.
memory/archive/2025-06-backlog.md:27:PROJ-1042: add webhook retry support.
```

## Concept search

Find notes by intent when you don't know the exact wording:

```bash
clawgrep --no-color "decision about migration strategy" ./memory
```

Output:

```
memory/2025-06-22-architecture.md:9:Agreed to do incremental schema migrations, no big-bang cutover.
memory/2025-06-22-architecture.md:15:Each migration must be reversible and tested in staging first.
memory/archive/2025-05-planning.md:41:Data migration approach still undecided — revisit next week.
```

## Listing matching files

Get only filenames with `-l`:

```bash
clawgrep --no-color -l "deployment" ./memory
```

Output:

```
memory/2025-07-01-incident.md
memory/2025-06-28-release.md
memory/archive/2025-05-deploy-notes.md
```

## Match count

Count matches per file with `-c`:

```bash
clawgrep --no-color -c "performance" ./memory
```

Output:

```
memory/2025-06-25-benchmarks.md:3
memory/2025-06-20-api-design.md:2
memory/archive/2025-05-brainstorm.md:1
```

## Quiet / existence check

Check whether something exists without output:

```bash
clawgrep -q "API key rotation" ./memory
echo $?   # 0 if found, 1 if not
```

Useful in conditionals:

```bash
if clawgrep -q "unresolved action item" ./memory; then
  echo "Outstanding items found"
fi
```

## Boosting path matches

Rank filename matches higher with `--path-boost`:

```bash
clawgrep --no-color --path-boost 2.0 "incident" ./memory
```

Output:

```
memory/2025-07-01-incident.md:1:# Production incident — cache invalidation failure
memory/2025-07-01-incident.md:7:Rollback steps: revert the tag, re-deploy previous image, flush cache.
memory/2025-06-28-release.md:22:No incidents reported after the 2.1 release.
```

The file named `incident.md` is ranked first because `--path-boost 2.0` doubles
the weight of path matches.

## More results

Get more results with `-k`:

```bash
clawgrep --no-color -k 20 "error handling" ./memory
```

Returns up to 20 results instead of the default 5.

## Minimum score threshold

Filter out low-quality results:

```bash
clawgrep --no-color --min-score 0.5 "onboarding checklist" ./memory
```

Only returns results with a combined score of 0.5 or higher.

## Piping stdin

Search piped content (no caching):

```bash
cat session-log.txt | clawgrep --no-color "action item"
git diff | clawgrep --no-color "security"
```

When reading from stdin with a single source, the filename prefix is omitted
(matching grep behavior):

```
12:Action item: finalize the API contract by Friday.
47:Action item: schedule design review with the team.
```

## Custom ignore file

Add project-specific ignore rules:

```bash
clawgrep --no-color --ignore-file .clawgrepignore "todo" .
```

The ignore file uses the same syntax as `.gitignore`.

## Force re-index

If results seem stale after file changes:

```bash
clawgrep --no-color --reindex "meeting notes" ./memory
```

## No-cache mode

Skip the cache entirely for throwaway searches:

```bash
clawgrep --no-color --no-cache "one-off query" ./tmp
```
