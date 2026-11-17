# Deliver: hand-offs, the audit map, and tickets

Read this when the audit reaches step 6, or when resuming work from an audit map.

## Hand-off notes

Every phase ends by rewriting `<out>/HANDOFF.md`, so a fresh session (or the next skill) resumes without this conversation:

```markdown
# Audit hand-off
- phase done: <scan | recon | hunt | verify | report | deliver | fix>
- next: <the next phase, or the next ticket on the map>
- approved: <ticket numbers the user approved for source changes, with who and when; empty means ask first>
- run: <commit and arguments, as in RUN.md>
- artifacts: <paths: SCAN.md, RECON.md, findings/, REPORT.md, the map>
- open questions: <decisions waiting on the user>
- suggested skills: <the skills the next session should call, e.g. tdd, grill-with-docs>
```

Reference artifacts by path; a hand-off restates nothing they already hold. Redact secrets and personal data.

## The audit map

Delivery charts the report onto the repo's issue tracker as a map plus child tickets, the way `wayfinder` charts an effort. The map is an **index, not a store**: each decision or fix lives in exactly one ticket, and the map gists it and links.

Where it goes: the tracker in `docs/agents/issue-tracker*.md` when `setup-matt-pocock-skills` has configured one; otherwise the local-markdown tracker below. Publishing to a remote tracker (GitHub, GitLab, Linear) posts for others to see, so confirm with the user first; the local tracker needs no confirmation.

Local-markdown layout:

- Map: `.scratch/audit-<date>/map.md`
- Tickets: `.scratch/audit-<date>/issues/NN-<slug>.md`, numbered from `01`
- A ticket's header lines: `Type:`, `Status:` (`open` | `claimed` | `resolved`), `Blocked by: NN, NN`

The map body:

```markdown
## Destination
Every CONFIRMED critical and high finding fixed, its repro green, and a re-audit with `--since <audit commit>` that verifies clean.

## Notes
Report: <path to REPORT.md>. Skills to consult: tdd, grill-with-docs, codebase-design. House rules: <ADRs, glossary>.

## Decisions so far
<!-- one line per resolved ticket: [title](link): gist -->

## Not yet specified
<!-- PLAUSIBLE findings that need a repro or more reading before they can be ticketed precisely -->

## Out of scope
<!-- accepted risks, each with the ADR that records it -->
```

## Tickets

One ticket per fix in `REPORT.md` (a fix, not a finding: the findings it solves are listed inside it), sized to one agent session. Refer to tickets by title in everything a human reads.

| Type | When | Worked by |
|---|---|---|
| `fix` | a `local` or one-session `structural` fix, the way is clear | AFK: `tdd` from the repro, or `UNTANGLE.md` for structural |
| `grilling` | the fix needs a decision only the user can make | HITL: `grill-with-docs` |
| `research` | a fact outside the repo is needed (a provider's behavior, a store rule) | AFK: `research` |
| `task` | manual work blocks a decision (provision a staging database, get sandbox credentials) | AFK where possible, else a checklist for the user |

A `fix` ticket body:

```markdown
Type: fix
Status: open
Blocked by: <NN, NN>

## Fix
<the fix, in the report's words>

## Findings
- <LENS-n> `<where>`: <claim>

## Done when
<the repro path> goes from red to green, and the full suite stays green.
```

Blocking edges come in a second pass, once every ticket has a number: a structural fix blocks the local fixes in the same modules; a decision ticket blocks the fixes that depend on its answer; a wide refactor goes expand–contract (expand ticket, migrate batches blocked by it, contract ticket blocked by every batch).

## Working the map

One ticket per session (research tickets may run in parallel):

1. Load the map, then take the first **frontier** ticket: open, unblocked, unclaimed. Claim it (`Status: claimed`) before any work.
2. Resolve it as its type says.
3. Record the resolution: append `## Answer` (what changed, commit, the repro now green), set `Status: resolved`, add a line to the map's Decisions so far, and rewrite `HANDOFF.md` with the next frontier ticket.
4. Graduate whatever the answer made specifiable from Not yet specified into new tickets; close tickets the answer made moot.

When the frontier is empty, run the audit again with `--since <the audit commit>` on the touched lenses. The map reaches its destination when that re-audit verifies with no surviving critical or high finding.
