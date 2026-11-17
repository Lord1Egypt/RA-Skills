# Data Table Review Template

Use for dense tables, list workbenches, inventory, moderation queues, CRM records, and admin grids.

## Scope Inputs

- Primary row-level and batch jobs.
- Expected row count and update frequency.
- Required columns, roles, permissions, and destructive actions.
- Desktop density and any explicitly required narrow viewport.

## Evidence Checklist

- Column priority, stable widths, long values, truncation disclosure, and horizontal navigation.
- Search, filter, sort, saved views, pagination or virtualization, and result counts.
- Selection persistence across filters/pages and visible selected scope.
- Row action discoverability, keyboard path, focus return, and bulk-action safeguards.
- Loading, empty, partial, stale, error, permission, optimistic, and rollback states.
- Source, freshness, timezone, units, calculation definitions, and export consistency.

## High-Risk Findings

- `P0`: destructive batch action can affect unseen rows or lacks recoverability.
- `P1`: users cannot identify selected scope, compare key fields, or reproduce a filtered view.
- `P2`: density, alignment, sticky regions, or secondary metadata need polish.

## Acceptance Examples

- Selected count and scope remain visible before confirmation.
- Keyboard users can enter a row, invoke actions, dismiss dialogs, and return to the originating row.
- Long representative values do not hide the differentiating content without a disclosure path.
- Empty and zero-result states distinguish “no data” from “filters removed every result”.
