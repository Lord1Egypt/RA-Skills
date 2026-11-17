# Cross-Plugin File Contracts (CDH)

Authoritative file-contract schema for Capability Discovery and Handshake between
Personal Supervisor (`master-agent-assistance`) and Governance
(`governance-multi-agent-harness`). Plugins **implement** this contract; they
do **not** fork or restate it.

Machine-readable keys stay English. Respond to humans in their language.

## Single-writer ownership

"Knowing the other plugin exists" does **not** mean co-writing one folder. It
means layered ownership + reference-not-copy + identity handshake.

| Fact | Sole writer | Other side |
| --- | --- | --- |
| Work order / `Docs/ACTIVE_PACKET.md` / acceptance criteria | supervisor (CMS plane, once at intake) | governance cites the path; delegate prompts reference, never restate |
| Adapter / permission ceiling / route decision | governance | supervisor reads the run link only |
| HANDOFF + evidence reports under `.agent-state/<task-id>/` | governance (child writes) | supervisor review stores `{path, summary, sha256}` only |
| Cross-project alignment / rebaseline / decisions | supervisor | governance need not know |
| Lifecycle state (`routed` / `running` / …) | each side's **session log** | bridge maps; **no shared `status.json`** |
| Human approval gate | **supervisor only** | bridge programmatically `approve()`s governance |
| Owner accept / needs-fix | **supervisor review** | bridge then calls `governance.accept('accepted' \| 'needs-follow-up')` |

One dispatch ⇒ one work-order id ⇒ one `.agent-state/<task-id>/` evidence
namespace. Lifecycle never lives in a shared mutable status file.

## Handshake front-matter (schema 1)

Every execution-layer Markdown file under `.agent-state/<task-id>/` opens with
this YAML front-matter fence:

```yaml
---
schema: 1
supervisor-task-id: <SupervisorTaskId>
owner: governance
upstream: Docs/ACTIVE_PACKET.md
---
```

| Field | Required | Rules |
| --- | --- | --- |
| `schema` | yes | Integer `1` (this revision). Mismatch fails loud. |
| `supervisor-task-id` | yes | Non-empty string; the supervisor-owned task id. |
| `owner` | yes | Exactly `governance` for execution-layer files written by the governance child. |
| `upstream` | no | Project-relative path to the supervisor-owned authority file (normally `Docs/ACTIVE_PACKET.md` or the Work Order). Never embed that file's body. |

Session stamp `governance/supervisor-binding` carries the same identity
(`schema: 1`, `taskId`, `supervisorTaskId`, `owner: governance`, optional
`upstream`) so restart replay can join without reading the files first.

## Cross-layer file reference

When one layer cites a file owned by the other, the citation is only:

```json
{ "path": "Docs/ACTIVE_PACKET.md", "summary": "…", "sha256": "<hex>" }
```

| Field | Required | Rules |
| --- | --- | --- |
| `path` | yes | Project-relative or workspace-absolute path inside the project cwd. |
| `summary` | yes | Short human-readable summary; never the file body. |
| `sha256` | preferred | Hex digest of the file bytes. Computed by the writing tool / host, never declared by the model. |

Do not copy Work Order or Active Packet text into the delegate prompt. Cite
`upstream` (or the reference object) so the child opens the authoritative file.

## Evidence namespace

- Root: `.agent-state/<task-id>/` where `<task-id>` is the **governance** task id
  returned by `routeFor`.
- Allowed contents: HANDOFF, evidence summaries, test logs, bounded next-step
  packets — each carrying handshake front-matter when Markdown.
- Paths must stay inside the session workspace (no `..`, symlink, or junction
  escape).
- Supervisor review keeps only reference objects; it does not ingest bodies into
  durable supervisor-memory summaries.

## Plugin obligations

| Repo | Implements | Does not own |
| --- | --- | --- |
| ClawSkills `cms-project-governance` (this skill) | Schema text, ownership table, reference shape | Runtime code |
| `governance-multi-agent-harness` | Front-matter helpers, binding stamp, handoff hash, path confinement | Schema text |
| `master-agent-assistance` | Intake write of Active Packet / Work Order; review stores references only | Schema text; governance session events |

When implementation choices conflict with this file, **this file wins**.
