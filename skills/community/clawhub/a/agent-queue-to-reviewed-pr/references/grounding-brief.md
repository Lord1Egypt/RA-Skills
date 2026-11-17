# Grounding — raw request → anchored brief

The grounding link **feeds** the queue. It never writes code, never opens a PR, never pushes. Read-only on the target repo, one card per run, FIFO by `created_at`.

**The brief is the product.** The implementation link is a consequence of it. A thin brief produces off-scope code no amount of review discipline recovers.

## Invariants

| Rule | Consequence if broken |
|---|---|
| One card per run, oldest first | Batch grounding produces shallow briefs — the LLM amortizes attention across cards |
| Read-only: no branch, no commit, no push | A grounding run that writes is an implementation run with no QA |
| **Every anchor verified in real code before being written** | A plausible-but-imaginary path is worse than no path: the implementer trusts it |
| Unverifiable anchor → **no ack** | The card stays in the grounding queue and a human is told why. We never ground on imagined code. |
| The agent ENRICHES, the human PRIORITIZES | Never move a card into a priority column yourself |
| **The brief cites code, not people.** Never copy the requester's name, email address, phone number or any other personal identifier out of the source request and into the payload, the prompt, or the PR description. Refer to a person as "the requester" and to their ask by its content. | The brief is POSTed to `${GROUNDING_ACK_URL}`, stored in the queue, and recopied into a PR description. Personal data that enters here spreads to three systems that had no reason to hold it — and it is never what makes a brief good. |

## Method, in order

1. **Read the whole source request** — body included, not just the title — then write down the *ask*, not the asker. Identity is not an anchor: nothing downstream needs it.
2. **Clean, up-to-date base**: `git fetch origin`, read `origin/<integration-branch>`. Read-only.
3. **Read the conventions**: `CLAUDE.md` + `AGENTS.md` at the repo root, plus any `.claude/` rules. These outrank your habits.
4. **Locate the concerned zone**: grep and read the real files. Identify exact paths, helpers, flags, line ranges.
5. **Verify each anchor you intend to cite**: the file exists, the function exists, the line number is right, the convention applies.
6. **Write the brief**, then run the local gate before the ack.

Repo unreachable, or the request too vague to anchor in real code → **STOP, no ack**, alert with the card id and what blocks. This is a feature: an unanchored card that stays in the grounding queue is visible; a hallucinated brief is invisible until it produces a bad PR.

## The payload — rough sizes per section

These are orders of magnitude, not measurements. **Length is a floor against the empty brief, never a definition of quality** — it catches the one-line card and nothing else. A padded 12k brief still fails the self-sufficiency test below, which is the only test that matters.

| Section | Rough size | Content | Gated |
|---|---|---|---|
| `context` | ~1-2k chars | why this card exists, current state of the product in that zone | |
| `impact` | ~1-2k chars | user/business value, what concretely changes | |
| `definition` | ~1-2k chars | in scope, acceptance criteria, **explicitly out of scope** | **non-empty** |
| `technical` | **~3k+ — the section that carries the value** | **real anchors**: verified paths + line ranges, helpers to reuse, conventions, integration points | **non-empty** |
| `risks` | ~1-2k chars | traps, side effects, dependencies, what can break | |
| `title` | optional | sharpened title if the source had a weak one | |

`technical` is the core of the value. Example of the required register — anchors, not adjectives:

```
Reuse `formatInvoice` from `src/lib/format/invoice.ts` (l.42-71) — do NOT re-create it.
The mapping pass lives in `src/pipeline/invoice-mapping.ts` l.157-381; the filter must
plug in at l.204, after normalization and before dedup.
Types: `InvoiceRow` in `src/types/invoice.ts`. API layer: add the route under
`src/app/api/invoices/` following the typed client in `src/lib/api/`.
```

Not: *"modify the invoice mapping logic to add filtering"*. That sentence could have been written without reading a single file — which is exactly the failure mode.

## The prompt — block structure, 10k–16k chars, never < 3000

Line 1 is **exactly** the mandated prefix (the server checks `startsWith`), then:

| # | Block | Content |
|---|---|---|
| 1 | `Read CLAUDE.md AND AGENTS.md at the root of ${TARGET_REPO} first` | verbatim, first line, no leading whitespace, your repo name substituted |
| 2 | `# Autonomous prompt — Implement "<id>" (<priority> · effort <n>)` | header |
| 3 | `## Guardrails (NON-negotiable)` | branch from a clean integration branch or a worktree; never commit/push to integration or release branches; obey `CLAUDE.md`+`AGENTS.md`; then the repo's own conventions — e.g. i18n keys in every locale, imports through the path alias, the project logger instead of `console.log`, tenant scoping on every query, memoized derived data |
| 4 | `## Verified context (real paths)` | the anchors from step 5 above |
| 5 | `## Steps (in order)` | numbered, each with its file+line anchor |
| 6 | `## Localization to add` | if user-facing strings are touched: keys in **every** locale file |
| 7 | `## Method` | explicit: frame → written plan **before** coding → TDD (red test → code → green) |
| 8 | `## Definition of Done` | concrete, verifiable criteria |
| 9 | `## Mandatory final QA` | the EXACT check commands, in the EXACT order |
| 10 | `## Do NOT do here` | scope bounds: no opportunistic refactor, no mixing with another card |

**The test of a good brief:** hand it to an agent that has never seen the original request. If it needs the request, the brief failed. That is the entire point of the 10k–16k target — not verbosity, self-sufficiency.

## The local gate

Export `BRIEF_GATE_PREFIX` first — the mandated line with your repo name substituted, byte-identical to the server's. The script refuses to run while the `${TARGET_REPO}` placeholder is still in place.

```bash
export BRIEF_GATE_PREFIX="Read CLAUDE.md AND AGENTS.md at the root of app-example first"
python3 scripts/brief-gate.py <card_id> payload.json prompt.txt > body.json
# Output: brief-gate: prompt too short (1180 < 3000 chars). Flesh out the brief: target 10000-16000 -- NOTHING was sent.
echo $?   # Output: 1
```

Exit 1 means nothing left the machine. Flesh out the brief and re-run. Do not "try the endpoint to see" — the server applies the same predicate and returns `400 grounding_too_thin`.

| Exit | Meaning |
|---|---|
| 0 | gate green, `body.json` on stdout, safe to POST |
| 1 | gate red — prompt too short, prefix missing, or `definition`/`technical` empty. Nothing sent. |

After a successful ack, delete the temp files. One card per run.
