# api-design-review

Review a proposed REST/HTTP API — an OpenAPI spec, design doc, or endpoint sketch — and produce severity-tagged findings, a go/no-go verdict, and a required-before-ship checklist.

---

## What It Does

Walks the API through nine review dimensions — resource modeling, HTTP verbs and status codes, request/response shape, errors, pagination/filtering/sorting, idempotency, versioning, auth, and rate limiting — applies industry checklists (Microsoft REST guidelines, Zalando RESTful API guidelines, Nordic APIs review patterns), and produces a structured review report with severity-tagged findings, a Top-5 must-fix list, a go/no-go ship verdict, and a required-before-ship checklist. The report is written for a design review meeting: the API author can read it cold and know what to change.

---

## When To Use

- A platform, product, or backend engineer needs a structured second opinion on a draft API before client teams build against it.
- A staff engineer is reviewing an API RFC and wants a consistent rubric across teams.
- An API gateway / platform team is auditing services for guideline compliance.
- A team is migrating to OpenAPI and wants to lint the spec for design (not just syntax) issues.

---

## Compatibility

| Platform | Supported |
|----------|:---------:|
| Claude Code | ✅ |
| Openclaw | ✅ |
| Codex | ✅ |

---

## Source

Part of the [open-skill-hub-api-design](../../README.md) plugin.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
