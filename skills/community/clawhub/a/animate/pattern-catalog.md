# Pattern Catalog - Animate

Use these patterns as defaults, then tune them to the product tone and stack.

## Navigation and Shared Transitions

Use when:
- the user needs continuity between list and detail
- route changes feel abrupt

Preferred motion:
- container or shared-element transition on a meaningful axis
- supporting content fades slightly after the primary object moves

Reduced motion:
- crossfade with minimal travel

## Modals, Sheets, and Drawers

Use when:
- overlays interrupt the current task

Preferred motion:
- backdrop fade plus one directional surface movement
- content inside should animate after the container settles

Reduced motion:
- quick fade or low-distance rise

## Lists, Reorder, and Expand/Collapse

Use when:
- items insert, remove, reorder, or reveal detail

Preferred motion:
- layout-aware movement with preserved item identity
- chevron rotation or opacity change only if it reinforces state

Reduced motion:
- shorter duration, lower travel, no bounce

## Loading, Success, Error, Retry

Use when:
- async work changes perceived responsiveness

Preferred motion:
- skeleton or progress feedback for waiting
- concise success confirmation
- error states that appear firmly without violent shake

Reduced motion:
- no pulsing loops unless truly necessary

## Buttons, Forms, and Toggles

Use when:
- the interface needs acknowledgment under touch, mouse, or keyboard

Preferred motion:
- pressed state within 100ms
- focus and validation transitions that do not move layout unpredictably

Reduced motion:
- color, opacity, or border emphasis without travel

## Optimistic Updates and Undo

Use when:
- the app updates state before the backend confirms

Preferred motion:
- immediate optimistic response
- clear pending or syncing state
- graceful rollback if the action fails

Reduced motion:
- concise content swap instead of animated travel
