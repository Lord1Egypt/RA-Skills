# architecture-decision-record-drafter

Turn an in-flight architectural decision into a complete, append-only Architecture Decision Record (ADR) that a future maintainer can re-read months later and understand why the system is the way it is.

---

## What It Does

Guides the user through scoping the decision, surfacing the forces and constraints, enumerating at least two real alternatives with honest trade-offs, naming the chosen option, and recording the consequences. Produces a MADR-style ADR in Markdown with sequential filename, status, decision drivers, considered options with pros and cons, decision outcome, positive and negative consequences, related decisions, and a supersession field — ready to drop into `docs/adr/` and commit alongside the change.

---

## When To Use

- A team is choosing between two or more technical approaches (data store, framework, integration pattern, deployment topology, build tool) and needs the rationale captured before the decision is implemented.
- An existing decision is being replaced and a new ADR is needed to supersede the prior record.
- A new engineer needs to document an existing-but-undocumented decision so it survives team rotation.
- A platform team wants a consistent ADR template across services.

---

## Compatibility

| Platform | Supported |
|----------|:---------:|
| Claude Code | ✅ |
| Openclaw | ✅ |
| Codex | ✅ |

---

## Source

Part of the [open-skill-hub-software-architecture](../../README.md) plugin.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
