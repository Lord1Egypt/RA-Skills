# Technical Specification Architecture

## Authority and Scope

Define an explicit source-of-truth order: current user direction, invariant safety and data rules, verified implementation behavior, then historical plans. State which document is authoritative and when it must be updated.

## Front-Loaded Reading Model

Place a compact, mandatory rule block immediately after the title. Cover only constraints that apply to every task: data boundaries, security, protected code, scope control, repository hygiene, and verification responsibility.

Follow it with a clickable section index, a task-to-section routing table, and a note that historical or experimental material is read only when current facts cannot explain a decision. This enables narrow context loading without weakening safety.

Use one lightweight contributor entrypoint as the default read. The authoritative specification remains queryable reference material; ordinary tasks should not load it in full. Route by heading, symbol, identifier, or bounded line range.

## Context Budget Policy

Define repository-specific limits for initial file count, default line range, command output, visual checks, and handoff length. Keep the limits in the lightweight entrypoint and validate them mechanically when the repository chooses fixed values.

Budgets reduce observation noise; they do not override safety review or prevent reading additional evidence when a task genuinely requires it.

## Stable Hierarchy

- Use exactly one H1 for the document title.
- Use H2 for mandatory rules, the index, and primary chapters.
- Use H3 only beneath its owning H2.
- Avoid heading-level jumps and unnecessary depth.
- Preserve established numbering and anchors when refactoring an existing document.

## Separation of Concerns

Keep normative rules, verified current state, historical plans, and private experiments distinct. Experimental material remains non-authoritative and excluded from publication by default.

## Maintenance Rules

Use frontmatter for document type, language, schema or semantic version, update time, and status. Raise the version when governance changes. Ensure the update time is not older than the newest completed record it covers.
