# From exploration to a proposed action

Read this when a concrete action or automation is proposed, rather than at the start of read-only exploration. The agent prepares the technical files; the operator supplies decisions in ordinary language and approves the resulting limits. Existing answers may be reused only when their scope and currency are clear.

## Ask only for missing decisions

Establish the proposed action, amount and unit; whether it is a first action or repeat; whether this is a proposal for approval or delegated execution; and the applicable maximum per action. Ask which larger amounts require stronger review, which evidence or recipient-linkage checks are mandatory, and which legal, jurisdiction, recipient or other operator constraints cannot be waived. Mission fit remains the operator's decision.

Material uncertainty waits unless the operator explicitly opts into a bounded small test and supplies its positive size cap. Ask this separately from the ordinary maximum; willingness to make a small donation does not imply permission to act through uncertainty. Contradictions, missing required checks and fresh repeat support remain blockers under the existing contract. Never supply an answer on the operator's behalf.

For automation, also establish the cadence, cumulative budget and period, paid-access budget, repeat limits, stop conditions and approval scope. The coordinator enforces per-action eligibility and size; it does not enforce a cumulative wallet budget, scheduling, durable payment reconciliation or terms acceptance. Identify the existing wallet/runtime controls that enforce those limits. If they are unavailable, keep execution manual and report the gap rather than claiming the JSON enforces it. No Hermes, CauseClaw or other operator's local minimum is a universal floor.

## Prepare compatible files

Use [policy-template.json](policy-template.json) for field names, not as granted authority. Replace its example amounts, action and required checks with the operator's actual answers. Put non-waivable checks in existing `required_lanes` / `required_lanes_for_serious_action` entries or configured `hard_blocker_codes`, as described in [lane contracts](lane_contracts.md). Keep `uncertainty_action: "monitor"` unless the explicit small-test decision was made. Do not add new coordinator fields and assume they are enforced; notes can retain constraints whose enforcement lives elsewhere.

Create private `policy.json` and lane files in the working directory, outside the installed skill. Produce lane decisions from material actually reviewed using [lane contracts](lane_contracts.md) and the relevant domain adapter. Missing or failed required work stays `missing` or `error`; do not copy favorable decisions from the bundled example. Independent lanes need distinct evidence or review work, not multiple restatements of one source. Keep case-specific evidence and detection detail private.

Summarize the draft in ordinary language: the proposed action, per-action cap, required checks, uncertainty choice, repeat rule, human approval scope, and which external controls enforce cumulative or scheduling limits. Ask the operator to approve or correct that policy summary. A draft, coordinator success, or eligible disposition does not itself authorize a wallet action or accept terms.

## Run the existing gate

With approved policy and current reviews, run from the installed skill directory, using absolute paths for the private files:

```sh
node scripts/credibility-coordinator.mjs --policy /work/policy.json --lane evidence=/work/evidence.json --lane external_context=/work/external-context.json --lane graph_history=/work/graph-history.json --out /work/disposition.json
```

Include every additional required lane. Require a successful exit and a fresh result for this invocation. An error, missing runtime or stale output supplies no eligibility. If Node.js is unavailable in the current environment, explain that the deterministic gate has not run and keep the proposed action pending; do not ask the operator to hand-edit files or substitute a narrative disposition.

Explain the resulting limits and remaining uncertainty before requesting any separate execution approval. Registration and current legal acknowledgement still require their own explicit operator decisions. A walkthrough or request to propose a donation stops before registration, paid evidence, signing or sending funds.
