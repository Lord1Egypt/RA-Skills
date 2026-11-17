# Fresh source-to-answer run — 2026-09-28

Version under test: cue-omni-ontology 0.2.0. Scope: selected Microsoft FY2026 Q3/Q4 public earnings disclosures. This is a development validation on two sources, not an extraction-accuracy benchmark or cross-client onboarding certification. Because this run used `detail: text`, its sources carry text ranges, not page spans; since 0.3.0, `ontology.py omni-source` turns a saved grounded result into page spans (see [verification.md](verification.md)).

## What ran

1. Read current official cue-omni-reader instructions; existing Bridge 1.8.4 matched the published setup pin. Its silent update probe returned `unavailable`; no upgrade was performed.
2. Called official MCP `parse` twice concurrently with `detail: text`, `result_delivery: artifact`; preserved the two distinct operations and polled them. These are fresh operations, not replayed parser output.
3. Read complete artifacts: 39,925 and 42,744 UTF-8 bytes, each without a continuation cursor. Saved exact text locally, then received confirmed discard for both temporary result artifacts.
4. The host read the source text and authored selected financial claims, including period/unit/basis headers and adjustment footnotes. The bundled `prepare` resolved exact quotes; `build`, `update`, `brief` and evidence queries completed.
5. Result: 2 sources, 2 entities, 8 candidate definitions, 21 source assertions / fact scopes. Q4 added 10 scopes; all 11 baseline assertions remain. No same-scope conflict was present in this selected real sample; conflicts remain covered by separate synthetic scenarios.

The service returned 0.938 and 1.005 credits charged for these two operations (sum 1.943). This is an observed charge for this run, not a price quote, rate or future-cost guarantee. No account balance, key, operation handle or private endpoint is published here.

## Business questions checked

| Question | Result |
|---|---|
| Q4 Microsoft 365 Commercial cloud growth without a basis? | `needs_scope`: reported 14% and adjusted-comparator 16% remain separate. |
| Select reported or adjusted-comparator basis? | `found`: 14% / 16% respectively, each with the disclosure and comparator explanation. |
| Q4 net income without accounting basis? | `needs_scope`: GAAP USD 35,766 million / non-GAAP USD 35,286 million. OpenAI adjustment definition remains attached. |
| Did a named cause produce Azure growth? | `not_found` for the unextracted causal relation; the workflow does not invent it. |

## Sources and reproducibility

- [Microsoft FY26 Q3 release](https://www.microsoft.com/en-us/investor/earnings/fy-2026-q3/press-release-webcast), published 2026-04-29; accessed 2026-09-28. Parsed text SHA-256: `38ef94314de1f1b842cf418cb6ebaf4eb123a7383c610d8ed0737906c675850d`.
- [Microsoft FY26 Q4 release](https://www.microsoft.com/en-us/investor/earnings/fy-2026-q4/press-release-webcast), published 2026-07-29; accessed 2026-09-28. Parsed text SHA-256: `f2dc85192a4dca1de7139f2656f5aa1ff38b7379e6bf715b482ad93e9b9c2138`.

These are HTML sources with text-range evidence; no PDF page grounding or geometry is claimed for this run. Webpages and parser rendering may change, so future snapshots need not share these hashes. The repository includes source links and selected factual distinctions, not the full parsed releases. A fully offline reproduction uses the explicitly synthetic `demo` command. Repeating the real-source test requires an authorized official parser connection, fresh snapshots and host extraction under the same small task scope.

Remaining limits: arbitrary document families, newly installed third-party clients, independent financial expert review, complete-report coverage, enterprise-local deployment, automatic schema promotion, downstream business writeback, paid demand and measured user time savings remain unestablished.
