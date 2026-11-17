# Mobile Navigation Review Template

Use only when mobile is explicitly in scope or the artifact/workflow is mobile-first.

## Scope Inputs

- Device class, web/app/webview context, safe areas, and orientation.
- Primary destinations, task frequency, navigation depth, and deep-link expectations.
- Keyboard, gesture, offline, and authentication constraints.

## Evidence Checklist

- Current location, back behavior, tab persistence, and deep-link restoration are predictable.
- Primary destinations fit the chosen pattern; overflow items remain discoverable.
- Touch targets, thumb reach, safe areas, browser chrome, and virtual keyboard are handled.
- Drawers, sheets, menus, and modals manage focus and do not create nested escape traps.
- Labels survive localization and text scaling; icons have accessible names.
- Navigation remains usable during loading, offline, permission, and session-expiry states.

## High-Risk Findings

- `P0`: user becomes trapped, loses work, or cannot reach a primary destination.
- `P1`: hidden current state, ambiguous back behavior, or keyboard occlusion disrupts common tasks.
- `P2`: icon consistency, transition timing, or secondary destination grouping needs polish.

## Acceptance Examples

- System/browser back returns to the expected prior state without duplicating history.
- At 200% text scaling, destination labels remain understandable without overlapping controls.
- Bottom actions clear device safe areas and the virtual keyboard.
- Reduced-motion users receive equivalent state change without spatial animation dependence.
