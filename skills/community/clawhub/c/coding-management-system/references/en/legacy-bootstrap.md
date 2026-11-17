# Legacy Bootstrap 2.1

Use Legacy Bootstrap when an existing project has CMS records but no trustworthy Active Packet. The bootstrap is read-only by default.

## Read Boundary

1. Resolve the project root to its real path.
2. Find one immediate child directory named `Docs` case-insensitively.
3. Reject ambiguous Docs directories or any Docs path resolving outside the project.
4. Inventory file names, sizes, and modification times.
5. Read only likely current-state files and files explicitly linked by them.
6. Do not recursively load historical Markdown bodies, handoffs, or full logs.

Likely current-state files include Active Packet, TARGET, ACCEPTANCE, current Work Order, current assignment, current status, and the latest effective QA decision. A filename containing `archive`, `history`, `completed`, or `handoff` is not current authority unless a selected file links it.

## Conflict Detection

Write nothing when any material conflict exists, including:

- two or more current assignments without an explicit current override;
- target, status, or Work Order naming different active routes;
- an Accepted heading followed by a superseding Failed or Blocked decision;
- missing target, acceptance, scope, or authorization;
- Contract, Governance, or Artifact evidence being claimed as Runtime completion;
- a linked authority path escaping the project;
- an existing Active Packet with invalid or contradictory authority.

Return one Owner request containing all route choices, the conflicting evidence paths, the recommended default, and the consequence of each choice.

## Explicit Override

A clearly marked `Current Override`, `Current Effective`, or equivalent current-route statement may supersede older records. Preserve the older files as history and cite the override as authority. Do not infer an override merely from the newest timestamp.

## Conflict-Free Draft

Produce one Packet with:

- a user-visible desired outcome;
- minimum current scope and Non-Goals;
- delivery class;
- one bounded stage outcome;
- acceptance criteria tied to evidence class;
- project-local write boundary;
- authority sources and SHA-256 fingerprint;
- exactly one next action.

Keep it around 120 lines or fewer. `--write` writes only `Docs/ACTIVE_PACKET.md`, atomically where possible. It does not rename, delete, or rewrite legacy records.

## Commands

```text
bootstrap-active-packet.mjs --workspace <path> --language zh-CN --json
bootstrap-active-packet.mjs --workspace <path> --language zh-CN --json --write
```

The first command is always read-only. A conflict result uses a nonzero exit and reports `written: false`.
