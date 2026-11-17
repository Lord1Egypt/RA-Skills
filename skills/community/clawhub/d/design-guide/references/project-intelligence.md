# Project Intelligence

Read this reference before substantial work in an existing repository.

## Inventory

Run:

```bash
python3 <skill-dir>/scripts/inspect-project.py <project-root> --format markdown
```

Use the JSON form when another script or artifact will consume the result. Treat the report as a starting inventory, then inspect the high-value files it identifies.

Resolve these questions before selecting an implementation approach:

- Which framework, router, package manager, styling system, UI kit, icon set, and state library already own the interface?
- Where do routes, reusable components, design tokens, API schemas, tests, and public assets live?
- Which build, lint, typecheck, test, accessibility, and performance commands are already authoritative?
- Does the changed surface have existing behavior, analytics, permissions, data contracts, or responsive rules that must be preserved?

Do not infer that a capability is absent only because the scanner did not detect it. Search the reported configs and package scripts. Prefer repository conventions over bundled examples.

## Change Map

Before editing, write a compact map in working notes:

```text
Entry route/component:
Shared components/tokens:
State and data owners:
Existing tests:
Commands to verify:
Files likely to change:
Compatibility risks:
```

Keep this map internal unless the user asks for a plan or it reveals a decision they need to make.

## Greenfield Projects

When no frontend stack exists, select the smallest stack that satisfies the request. Record the choice and its maintenance cost in the design contract. Avoid adding a framework, UI library, state library, and animation library all at once unless each solves a demonstrated requirement.
