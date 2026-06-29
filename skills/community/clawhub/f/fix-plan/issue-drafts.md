# Issue Drafts

Lifecycle management for issue / PR draft files staged on disk before publication to GitHub. Without explicit lifecycle ownership, stale draft files accumulate and re-appear as "pending" on every supervisor pass.

## Lifecycle (CRITICAL)

Draft files follow a four-stage lifecycle. Each stage has a defined owner — gaps create residue.

| Stage | Action | Owner |
|-------|--------|-------|
| 1. Write | Create `issue-drafts/<slug>.md` | Author (human or agent) |
| 2. Publish | `gh issue create` / `gh pr create` posts to GitHub | Author |
| 3. **Archive** | `issue-drafts/<slug>.md` → `issue-drafts/.bak/<slug>.md` | **This skill on next invocation (automatic)** |
| 4. Delete from fix_plan | Remove the `[x]` entry from `## Issue Drafts` section | **This skill (immediately after archive)** |

**Order is mandatory**: archive **first**, fix_plan delete **second**. Reverse order leaves the file in `issue-drafts/` and the next supervisor pass mis-reads it as "still pending".

## Archive procedure

When this topic runs, scan the fix_plan `## Issue Drafts` section. Archive any entry matching **all** of these:

1. fix_plan entry is `[x]` or `[DONE]` checked
2. Entry body cites a draft filename (e.g. `web-each-key-duplicate.md`)
3. The file exists in `issue-drafts/` (not already in `.bak`)
4. Entry references `Issue #N` or `PR #N` (publish-trace evidence)

Archive command:

```bash
mkdir -p issue-drafts/.bak
mv issue-drafts/<slug>.md issue-drafts/.bak/
```

After the archive succeeds → delete the fix_plan entry (next section).

## Delete rule

Archived entries are **removed entirely** from `## Issue Drafts`.

- Do not use a `[DONE]` tag — completion = archive + entry removal
- Rationale: `## Merged / Closed` (or the issue body itself on GitHub) already records the Issue / PR number. Leaving a residual entry is duplicate noise

```markdown
# Wrong (forbidden)
- [DONE] cleanup test coverage — Issue #104, PR #105 merged (2026-04-24). Draft → `.bak`

# Right
# → archive (mv issue-drafts/cleanup-test-coverage.md → .bak/) → delete the entry entirely
# `## Merged / Closed` already records PR #105
```

## Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | `[x]`-check the fix_plan entry but leave the file in `issue-drafts/` | Archive (`mv → .bak/`) **first**, then delete the fix_plan entry |
| 2 | Ad-hoc AskUserQuestion "what should I do with this `[x]` entry?" | Invoke this topic — archive + delete is automatic |
| 3 | Keep a `[DONE]` tag in fix_plan | Archive, then remove the entry. The Merged / Closed section (or GitHub itself) is sufficient tracking |
| 4 | Skip archive → next supervisor run re-detects as "pending draft" → noise | Archive every time this topic runs |
| 5 | Archive without verifying the publish trace (`Issue #N` / `PR #N`) | Verify the entry references a real GitHub identifier before archiving. Items without a trace may not have been published yet |

## Self-check before archiving

1. Does the entry reference a real GitHub identifier (`Issue #N` / `PR #N`)?
2. Does the named draft file exist in `issue-drafts/`?
3. Is the fix_plan entry marked `[x]` (or `[DONE]`)?
4. After archive, will the fix_plan entry be deleted in the same pass?

If any answer is no, do not archive.

## See also

- [format.md](./format.md) — fix_plan section semantics
- [github-flow](../github-flow/) — `gh issue create` / `gh pr create` conventions
