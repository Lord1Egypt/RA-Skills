# Executable Implementation Contract

Read this reference after a Level 2 approval or before substantial implementation with multiple states, routes, breakpoints, or release gates.

## Create and Approve

Initialize a contract inside the target project:

```bash
python3 <skill-dir>/scripts/design-contract.py init \
  --out .codex/design-guide/design-contract.json
```

Replace every placeholder with the approved product decisions. Define concrete flow starts and stable selectors. Prefer role, label, or `data-testid` selectors over layout-dependent CSS selectors.

Set `contractStatus` to `approved` only after the user has approved the direction. Record:

- `approval.direction`: the chosen direction or combined direction.
- `approval.artifacts`: paths or durable review links that the user inspected.
- `approval.tradeoffs`: accepted limitations and rejected alternatives.

Validate before implementation:

```bash
python3 <skill-dir>/scripts/design-contract.py validate \
  .codex/design-guide/design-contract.json \
  --project-root . \
  --require-approved
```

## Contract Rules

- Every `requiredStates` value must appear in at least one flow's `coversStates`.
- Every required data contract path must exist inside the project root.
- Flow IDs and breakpoints must be unique.
- Keyboard-complete contracts must contain an executable keyboard step.
- Visual baseline keys use `<flow-id>@<breakpoint>`, for example `review-image@390`.
- Keep performance budgets realistic for the product, then tighten them over time. Do not inflate a budget solely to make a failing run green.

## Change Control

The contract is not frozen against all iteration. When implementation reveals a necessary change:

1. Identify whether it alters user flow, information priority, responsive behavior, critical state handling, or an accepted tradeoff.
2. For material changes, update the review artifact and obtain confirmation before changing the approved contract.
3. For implementation-detail changes, update the contract and record the reason without reopening design approval.
4. Keep the artifact, contract, code, and verification report consistent.
