# Skill Card — airbnb-gateway

*Format: NVIDIA Skill Card trust format (https://docs.nvidia.com/skills/skill-cards)*

## Description

Standardizes how AI agents operate a live Airbnb host account — reading inbox/reservations/calendar, sending guest messages, and (v0.2+) making operator-approved calendar mutations — with mandatory independent verification of every write.

## Skill Version

0.2.1 (2026-07-09). Repo tag/branch: `feat/airbnb-gateway-skill` in the publisher's source repository; each ClawHub release carries the version in SKILL.md frontmatter. (0.2.1 is a doc-consistency + safety-warning patch over 0.2.0 — no behavior change; see CHANGELOG.)

## Status

Ready for non-commercial and commercial use by rental operators running OpenClaw-style agent environments **with a human operator in the loop**. Not suitable for fully unattended mutation workflows.

## Owner

Jason Vaughan (`Jason-Vaughan` on ClawHub/GitHub). Accountable for content, releases, and the verified procedures shipped in `references/`.

## License / Terms

MIT (see LICENSE). No warranty; operating a revenue-bearing Airbnb account with agents is at the operator's risk.

## Use Case

Vacation-rental hosts/operators who run multi-agent assistants (OpenClaw or similar) and want every agent to handle Airbnb identically and safely: guest messaging with send-verification, reservation/calendar reads, and approval-gated calendar changes (block/open dates, nightly price). Not intended for scraping other hosts' data or for use against accounts you don't own.

## Deployment Geography

Wherever the operator's Airbnb account and infrastructure are legal and operable; developed and verified against a Mexico-based listing operated from the US. No geography-specific logic.

## Requirements / Dependencies

- An OpenClaw-style agent runtime that loads skills and provides an exec tool.
- An Airbnb read/send tool layer and a browser bridge to a **logged-in host browser identity** (reference deployment: ClawBridge HTTP endpoints + host Chrome via CDP). Role→tool mapping is deployment-specific via `references/airbnb-tool-priority.md`.
- Calendar mutations additionally require the verified UI procedure in `references/calendar-mutation-procedure.md`.
- A competent tool-calling model. Release evidence used codex/gpt-5.5; small local models were observed narrating instead of executing and are not recommended for MUTATE operations.

## Skill Output

- Guest replies sent via the Airbnb send path, with live-thread verification before success is claimed.
- Calendar mutations (v0.2): availability/price changes with reported before-state, actions, **fresh-load verified after-state**, screenshot audit paths, and the exact inverse operation.
- Structured refusals/escalations when gates are not satisfied or verification is ambiguous (`unconfirmed`).

## Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Duplicate/wrong guest messages | Send state machine; acknowledgments treated as *attempted*; verify in live thread; never auto-resend from ambiguous state |
| Unauthorized calendar changes | MUTATE-CAL requires explicit operator approval word per operation, one op per approval; MUTATE-RESTRICTED (listing edits, accept/decline, refunds) always refused |
| **False success claims** (observed in testing: an agent claimed a block succeeded when it had clicked a loading skeleton) | Mandatory Step-5 fresh-load verification; "if the stores/UI didn't change, the run didn't happen"; screenshot audit trail per action |
| Anti-bot/account risk from automation | Host-owned logged-in browser identity (headful) instead of anonymous headless automation; platform-native endpoints preferred over UI driving |
| Weak-model improvisation | Tool-priority tiers with explicit drop rules; verified step-by-step mutation procedure; skill directs agents to read references before acting |

## Ethical Considerations

Operates a real marketplace account affecting real guests; the operator remains responsible for pricing honesty, availability accuracy, and message content. The skill's gates are designed to keep a human accountable for every mutation. Do not use to manipulate availability/pricing deceptively or to operate accounts without authorization.

## References

- `SKILL.md` — operating model, tier table, approval gate
- `references/airbnb-tool-priority.md` — role→tool mapping + degradation rules
- `references/calendar-mutation-procedure.md` — verified mutation procedure (validated live 2026-07-04)
- `references/airbnb-safety-rules.md`, `references/airbnb-message-state-machine.md`
- **Release evidence (v0.2.0)**: live round-trip on the reference deployment — agent blocked and unblocked a single night under operator approval, each leg fresh-load verified with screenshot trail; plus a same-day negative result (false-success claim by a weaker model) that motivated the mandatory verification step. Incident record: publisher's repo issue #25.
