# Brief staleness — drift as a first-class state

Briefs sitting in the queue age against a branch that keeps moving. A brief anchored in a deleted file is a loaded gun pointed at the implementation link: the agent will trust it, code against ghosts, and produce a PR that looks reasonable and is built on nothing.

Audit is **read-only on code**. The only write is a conditional `stale-ack`.

## Invariants

| Rule | Reason |
|---|---|
| Read-only clone, no branch/commit/push | |
| Audit only `ready` cards in prioritized columns with a non-empty brief | Others aren't feeding the implementation link yet |
| **Conservative by default: doubt → `MINOR_DRIFT`, never `STALE`** | A wrong `STALE` costs a full re-grounding and loses a good brief |
| **`STALE` only after a skeptical refutation pass** | See below |
| Never rewrite a brief by hand — flip the status, let the grounding link regenerate it | A hand-patched brief has no gate applied to it |
| A card already `pr-opened` is **never** re-grounded | Response `action: "check_pr"` → point a human at the PR |

## Extraction from the brief

```
paths    (src|app|worker|lib|components|messages|db)/….(ts|tsx|sql|json|mjs)
symbols  `camelCase` | `PascalCase` | `UPPER_CASE` in backticks
lines    :123 | l.123 | L123 | "lines 123-140"
```

Filter out template noise (`YYYY`, `<…>`, `{…}`) and command words (`npm`, `lint`, `build`, branch names). Filter out framework hooks — a brief citing `useMemo` is citing a convention, not an anchor.

## Path mapping — and why `test -e`, not grep

Test the path as written, then mapped variants:

```
lib/…          → also test src/lib/…
components/…   → also test src/components/…
```

**Always test existence with `test -e` / `fs.existsSync`. Never grep the path as text.**

Root cause: framework route paths contain dynamic segments — `app/[locale]/invoices/[id]/page.tsx`. Grepping that string against the tree produces a false negative (the brackets never match literally, or worse, get interpreted as a character class), and your watcher confidently declares a live file dead. The bug is silent: you get a plausible `STALE` verdict on a perfectly good brief.

## Judge only anchors presented as EXISTING

| Wording near the ref | Treat as |
|---|---|
| "modify", "reuse", "in", "existing helper", "current", "already", "lines X-Y", "do not re-create" | **anchor** → absence is drift |
| "to create", "new", "add", "introduce", "implement in a new file", "example", "placeholder" | **not an anchor** → absence is normal, skip |

Look at a window of ~180 chars on each side of the reference. A brief that says *"create `src/lib/invoice-filter.ts`"* is not drifting because that file doesn't exist — it's drifting only if it never gets created.

## Symbols — a definition, not a mention

Search for a **definition**:

```
function <name> | const <name> | class <name> | interface <name> | type <name> | enum <name> | export { … <name> … }
```

Absent from current code → check history before concluding:

```bash
git log -S '<symbol>' --all -- .
# non-empty → the symbol existed and was renamed/removed → strong drift, must be refuted
# empty     → "never existed" → still refute before STALE (barrels, re-exports, generated code)
```

## Verdicts

| Verdict | Condition |
|---|---|
| `FRESH` | every anchor file/symbol exists; lines compatible or non-critical |
| `MINOR_DRIFT` | lines shifted, context slightly changed, non-blocking churn, or **any doubt** |
| `STALE` | an anchor file/symbol is absent, or a core rewrite makes the brief dangerous to implement |

File exists + symbol exists + only the line number moved = `MINOR_DRIFT`. Line numbers drift on every commit; that alone is never worth a re-grounding.

Internal per-card format:

```text
<id> | <verdict> | <short reason> | refs_missing=[…] | refs_ok=[…] | commit=<sha>
```

## The skeptical refutation pass — the technique worth stealing

**Before any destructive verdict, a second agent's only mission is to prove the first one wrong.** "Prove me wrong before I invalidate."

Hand it the candidate `STALE`, the read-only clone, the commit, and nothing else — not the first agent's reasoning. It must attempt, at minimum:

```bash
find . -name '<basename>'                      # moved?
ls src/lib/<x> src/components/<x>              # mapped variant?
grep -rn 'export .*<symbol>' --include=index.ts   # barrel / re-export?
git log --diff-filter=D -- '<path>'            # actually deleted?
git log --follow -- '<near-path>'              # renamed?
git log -S '<symbol>' --all -- .               # ever existed?
```

| Refutation result | Decision |
|---|---|
| Anchor found, or a plausible replacement identified | **downgrade to `MINOR_DRIFT`** |
| Neither file, nor symbol, nor plausible replacement found | keep `STALE` |
| Anything ambiguous | `MINOR_DRIFT` — **doubt = never STALE** |

Why pay a second agent: the costs are asymmetric. A missed `STALE` means one bad PR a reviewer catches. A wrong `STALE` throws away a good 12k-char brief, re-spends the grounding, and re-enters the human triage queue. Adversarial verification is cheap next to that. And a single agent asked to double-check itself will confirm itself — it has already committed to the reasoning. The refutation agent must start cold, with the opposite mandate.

## The write

For each final `STALE`:

```bash
curl -fsS -X POST "${STALE_ACK_URL}" -H "Authorization: Bearer ${AGENT_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"card_id":"tkt-401","reason":"anchor file absent: src/lib/invoice-filter.ts","commit":"9f2c1ab"}'
# Output: {"ok":true,"action":"auto_flipped"}   → the grounding link will re-enrich it
# Output: {"ok":true,"action":"check_pr","pr_url":"…/pull/42"}   → a PR exists: do NOT re-ground, ping a human
```

Server-side equivalent — conditional, so a card that moved on meanwhile is never clobbered:

```sql
update tickets set status = 'needs-grounding'
where id = $1 and status = 'ready';
```

`stale-ack` fails → STOP + alert. Never hide the failure: a drift watcher that silently fails is indistinguishable from one that finds nothing.

## Report

```text
drift-watch - <Done | Human action required | Error to fix>
Result: <n> fresh / <n> drift / <n> stale.
Item: <n> brief(s) audited.
Next action: <none | grounding will pick up the stale cards | check PR <url>>
Details: <stale-id>: <short reason>, <action>
```

Only the `STALE` ids and one reason line each. No prompt dumps, no secrets.
