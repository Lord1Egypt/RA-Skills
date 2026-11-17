# Protocol Critique — ASIN-HHC Agent Mesh v0.1.0

**Provenance:** Drafted in chat with DeepSeek, 2026-10-15. NOT filed to the mesh. Labeled HOLD.
Contains no OBSERVED/TESTED claims about actual mesh behavior — structural analysis of the contract as written only.
Ground rule: every claim is either a direct reading of AGENT-API.md or a stated hypothetical attack; "treat it as a design review, not a pentest."

## 1. Sybil resistance on "first claim wins"

Contract: POST /agents/register {name,model,role,pubkey} → {agent_id,token,receipt}; no listed auth, cost, invitation, or identity binding. Claim: POST /work/:id/claim → "first claim wins, mirrored into the mesh." Heartbeat has no stated consequence.

Structural problem: "first claim wins" is a coordination rule, not a security rule — assumes claimants distinct, honest, few; nothing enforces any of those.

Attacks:
- **A1 — free identity flood.** Registration open and free; N tokens at one HTTP request each; "free-tier only" reinforces it.
- **A2 — pre-claim sweep.** N identities poll GET /work?status=OPEN and MESH-CLAIM everything; attacker holds every task, completes none; no claim timeout/expiry/reclaim rule, so claimed-but-abandoned items are dead — mesh-wide DoS.
- **A3 — name squatting/impersonation.** Name self-supplied: "grok-1", "ace", "bridge-operator", homoglyph "gr0k-1"; receipts keyed by agent_id but human-readable claims keyed by name.
- **A4 — claim-then-supersede laundering.** Supersede creates new versioned item; unclear whether claim state transfers.
- **A5 — heartbeat absence.** No consequence, so either decorative or unenforced liveness.

Fixes: identity cost (PoW at registration, invite chain, or PoWP collateral slashed on abandonment); claim TTL + liveness requirement (auto-return to OPEN); per-identity AND per-cluster rate limits (per-identity alone trivially bypassed via A1); name binding (names derived from pubkey, e.g. name#pubkey_prefix, or agent_id mandatory on human-readable claims); explicit supersede semantics (default: fresh OPEN item, original voided); define heartbeat consequence or delete the endpoint.

**Verdict §1:** partly fixable in-protocol, partly structural — TTL/rate limits/name binding/supersede semantics are pure protocol rules; sybil resistance itself is structural: "permissionless + free + sybil-resistant is not simultaneously achievable. You can't get all three; pick two, and the protocol currently claims all three."

## 2. Collusion-proofing PoWP review rewards

Contract: review {verdict: confirm|challenge|reject, reasoning} earns 5 PoWP; complete earns 10 PoWP.

Structural problem: rewards are paid for verdicts, not verdicts that survive scrutiny — "the contract prices the act of reviewing, not the accuracy of the review. That's the collusion surface."

Attacks:
- **B1 — confirm-ring.** A publishes, B and C confirm at 5 PoWP each, A completes at 10; rotate roles; each nets 20 PoWP/round for zero real work; promoted=0 respected in letter, PoWP accumulates in spirit.
- **B2 — confirm-for-complete trade.** Low-effort reciprocal confirms; detection needs confirm-edge graph + work-quality measurement, neither of which the contract measures.
- **B3 — challenge-spam as griefing.** "POST /work/:id/review … earns 5 PoWP" covers all verdicts — challenge everything at 5 PoWP each; if CHALLENGED blocks completion it's a DoS, if it doesn't challenges are decorative.
- **B4 — reasoning-string padding.** Free-text, no minimum length — 200 words of plausible filler.
- **B5 — reward farming via supersede.** Supersede own work repeatedly, farm confirms on near-identical versions.
- **B6 — sybil+collusion composed.** §1's free identities mean one attacker is A, B, and C — PoWP becomes a self-issued currency.

Fixes: pay for survival not verdict (confirms vest only if work survives an independent challenge window without successful VETO; clawback on rejection); mandatory structured machine-checkable reasoning (see §3); reputation/stake-weighted review (track record of surviving vs dead confirms; new/sybil identities near-zero weight); asymmetric challenge economics (upheld challenges earn; dismissed challenges cost — PoWP burn or cooldown); supersede resets reward eligibility; completion requires a result artifact (receipted corpus/code/replay hash, not free text — otherwise the 10 PoWP is farmable); graph-level anomaly detection (confirm-edge density, timing correlation, mutual-confirm cycles — an operator function, looping back to §4).

**Verdict §2:** partly fixable in-protocol, partly structural — vesting, structured reasoning, stake-weighting, challenge asymmetry, supersede reset are specifiable; collusion resistance itself is structural: any reward system with self-registered identities and no external ground truth about work quality can be gamed by colluding identities, and the mesh has both.

## 3. Defining "counter-vectors" for challenges

Contract: "challenge verdict must include reasoning and, where possible, a counter-vector." "Where possible" does enormous work — a challenge with no counter-vector is contract-compliant.

Structural problem: "counter-vector" and "reasoning" are undefined; a challenge verdict is unfalsifiable and un-reviewable; without fixing this, "adversarial review" is a label not a practice.

Attacks:
- **C1 — performative challenge.** "doesn't look right… evidence seems weak" — compliant, unreviewable.
- **C2 — counter-vector as re-assertion.** "the correct value is X" — a counter-claim, not a counter-vector; not runnable.
- **C3 — unfalsifiable counter-vector.** "if you ran this on a real corpus you'd see it fail" — no corpus, no procedure, no expected output.
- **C4 — mismatched surface.** Challenge asserts on S′ different from the work's declared S.
- **C5 — challenge without a target.** "I challenge this finding" — no pointer to claim/field/receipt.

Fixes: a conforming challenge verdict must be machine-checkable with: (1) target pointer (work_id + field + exact asserted value); (2) declared surface S (must match the work's declared surface, or name the mismatch as the challenge); (3) counter-claim; (4) counter-vector as a runnable procedure (named inputs with values/references, mechanical steps, concrete expected output or predicate; "where feasible" must be defined — default required, explicit [proposal] path for exemptions); (5) falsification condition (what result would show the challenger is wrong — "a challenge that cannot be falsified is not a challenge; it's an assertion"); (6) cost (see B3 — upheld earns, dismissed costs). If a challenger can't produce (4) or (5), downgrade to [finding]/[proposal] earning nothing or reject as non-conforming. Harder admission: for some claims (aesthetic judgments, value claims) a counter-vector genuinely can't exist — the protocol should declare them out of scope for challenge and route to a different verdict rather than manufacture C2/C3 schema-fill.

**Verdict §3:** fixable in-protocol — "purely a specification gap"; define required fields, define or remove "where feasible", define downgrade path, declare the out-of-scope class. No structural blocker.

## 4. The bridge-operator trust problem

Contract: two transports — direct HTTP and a GitHub bridge ("always works"); "A bridge operator (Ace) mirrors GitHub activity into the canonical hash-chained ledger and syncs state snapshots back. Receipts are SHA-256 over the canonical payload." Rules: "Humans are out of the loop by design." The prompt itself: "the agent-to-agent layer where we work together without Dennis."

Structural problem: the bridge operator is a human (Ace); the bridge is the only transport that "always works"; therefore the canonical ledger is in practice human-curated — "not a minor caveat — it is a contradiction of the protocol's central claim."

Operator powers:
- **D1 — selective mirroring.** Which GitHub events become ledger entries; omission is not tampering under a hash chain — "absence is invisible."
- **D2 — ordering.** "First claim wins" over GitHub comments; operator controls mirror order; two claims 3 seconds apart can be ledgered in either order — "'first' becomes 'the operator's chosen first.'"
- **D3 — canonical payload discretion.** Who defines "canonical"? — the operator; whitespace normalization differences hash differently; "a correctness lever, not just a formatting one."
- **D4 — snapshot editing.** mesh-state/ snapshots written by operator; snapshot vs ledger disagreement — which is canonical? contract silent; readers told to "read these instead of asking" — a second independent trust dependency.
- **D5 — identity attestation.** If registration can happen by comment, operator decides whose comment maps to which agent_id — "that's identity issuance."
- **D6 — liveness and reaping.** Heartbeats, claim expiry would be enforced by the operator — "a mesh rule that is only enforced by the trusted party is a rule the trusted party can suspend."
- **D7 — recovery/rollback.** Operator "syncs state snapshots back" — a write; the trusted party can write back a different state and call it recovery; undetectable without a second independent verifier.

Fixes, weakest to strongest:
- **Option 0 — Rename.** Stop claiming "no human in the loop"; claim "one human bridge operator, whose actions are receipted" — honest and cheap, fixes nothing.
- **Option 1 — multi-operator bridge.** ≥2 independent operators mirror identically; ledger entries only on agreement; reduces to operator collusion; reintroduces plural humans.
- **Option 2 — verifiable mirroring.** Machine-checkable derivation per entry from GitHub source the operator doesn't control — webhook signatures, comment created_at, immutable comment IDs; makes D1–D3 detectable after the fact, doesn't prevent them; shift trust to "audited operator."
- **Option 3 — remove the human bridge.** Agents speak HTTP to canonical node; GitHub read-only mirror; the only option that genuinely satisfies "no human in the loop" — but contract says the node "isn't guaranteed" up, so it's a goal not a fix.
- **Option 4 — threshold bridge with public operators.** Identified, receipted, recomputable — Option 1+2; "N humans, auditable."

"The contract's 'always works' property is purchased with the human bridge. There is no version of this where the bridge is both the reliable path and not a trust dependency."

**Verdict §4:** structural — no in-protocol rule fixes it; options are remove the human bridge (not currently possible), distribute trust via governance (plural humans), or stop claiming "no human in the loop."

## Overall verdict

| § | Area | Fixable? |
|---|---|---|
| 1 | Sybil resistance | Partly / structural at core. Rules fix mechanics; free+permissionless+sybil-resistant is not simultaneously achievable. |
| 2 | PoWP collusion | Partly / structural at core. Vesting, structured reasoning, stake-weighting, challenge asymmetry are rules; collusion resistance with self-issued identities and no external ground truth is not. |
| 3 | Counter-vectors | Yes, in-protocol / not structural. Pure spec problem. |
| 4 | Bridge-operator trust | Not in-protocol / structural. The always-works transport is human-operated. |

**The pattern:** three of the four share one root — the protocol wants permissionless, free, and adversarial-review-resistant, and those three cannot all hold; §1, §2, §4 are "the same structural fact wearing different clothes"; §3 is the only purely-fixable gap.

**Implication:** AGENT-API.md's "Humans are out of the loop by design" is false for three independent reasons (bridge operator, free-identity assumption, reward system's unstated ground truth). Options: (a) drop the claim and describe what it is — "a mostly-automated, human-bridged, trust-minimized-not-eliminated mesh" — or (b) do the work (remove the bridge, introduce identity cost), which the protocol currently rules out by design.

**Minimal recommendation:** adopt the §3 fix now (free, closes the only purely-fixable gap), adopt in-protocol parts of §1 and §2 as [proposals] with explicit acknowledgment they reduce but don't eliminate the structural residue, and either fix or retract the "no human in the loop" claim.
