# Exit-Intent Trigger Rules — Reference Guide

## Trigger Signal Types

### Desktop Signals

**Cursor Exit (Primary)**
The most reliable desktop exit signal. The browser fires a `mouseout` event when the cursor leaves the document viewport. Best practice is to detect upward exit only (toward browser chrome / tabs / address bar), since sideways or downward exits usually indicate interaction with OS-level UI, not intent to leave.

Implementation notes:
- Listen for `mouseout` on the `<html>` element
- Check `event.relatedTarget === null` and `event.clientY < 0`
- Debounce by 100-200ms to avoid false triggers from fast mouse movement near the top

**Time-Gated Cursor Exit**
Combine cursor exit with a minimum time-on-page threshold. This prevents popups from firing on quick bounces where the visitor clearly isn't your target audience. Recommended minimums:
- Content/blog pages: 15 seconds
- Product pages: 15-20 seconds
- Cart page: 10 seconds (they already showed purchase intent)
- Collection/category pages: 20 seconds

**Scroll Depth Reversal**
Track the maximum scroll depth reached. If a user scrolls to 60%+ of the page and then rapidly scrolls back to the top, they may be looking for navigation to leave. This works well as a secondary signal combined with cursor exit.

**Idle Timeout**
If the user has been inactive (no mouse movement, scroll, or click) for 60+ seconds on a product or cart page, they may have switched tabs or lost interest. This can trigger a softer re-engagement element like a tab-title change ("Come back! Your cart misses you") rather than an overlay popup.

### Mobile Signals

Mobile lacks cursor tracking, so alternative signals are needed:

**Back Button / Navigation Gesture**
Intercept the `beforeunload` event or use the History API to detect back-button presses. When detected, show a bottom sheet before navigation completes. Note: browser support varies — test on iOS Safari, Chrome Android, and Samsung Internet.

**Tab/App Switch**
Use the `visibilitychange` event to detect when the user switches away from the browser tab. Show a re-engagement element when they return, not when they leave (you can't show a popup when the tab is hidden).

**Scroll Reversal Pattern**
After the user scrolls past 70% of a product page and then rapidly scrolls back up (velocity > threshold), display a non-intrusive bottom bar. This catches "I've seen enough, leaving now" behavior.

**Inactivity + Page Focus Loss**
Combine `visibilitychange` with a 30s+ inactivity timer. If the user was engaged (scrolled, tapped) and then goes silent before switching tabs, they're a good candidate for a return-visit popup.

## Exclusion Rules

### Behavioral Exclusions
| Rule | Rationale |
|---|---|
| User is on checkout page (past cart) | Never interrupt a completing purchase |
| User already saw popup this session | Prevents fatigue and annoyance |
| User dismissed popup within 72 hours | Cross-session frequency cap |
| User completed purchase within 30 days | Recent buyers don't need discounts |
| User has active promo code in cart | Already incentivized, popup adds no value |

### Traffic Source Exclusions
| Rule | Rationale |
|---|---|
| Referrer is email campaign with discount | Already has an offer, don't stack |
| UTM contains "affiliate" or "partner" | Affiliate terms may prohibit popup discounts |
| Referrer is price-comparison site | These visitors are highly price-sensitive; a popup discount may be expected and not incremental |

### Technical Exclusions
| Rule | Rationale |
|---|---|
| User agent matches known bots | Bots don't convert; showing popups to crawlers wastes impressions and may confuse analytics |
| JavaScript disabled or popup blocked | Graceful degradation — don't attempt to show if the environment can't support it |
| Page load time > 5 seconds | If the page is slow, adding a popup makes the experience worse |

## Trigger Logic Patterns

### AND Logic (Desktop — Recommended)
All conditions must be true simultaneously:
```
IF time_on_page >= 15s
AND cursor_exited_top == true
AND page_type IN [product, cart]
AND session_popup_count == 0
AND days_since_purchase > 30
AND has_active_promo == false
THEN show_popup(tier_based_on_cart)
```

### OR Logic (Mobile — One Signal Sufficient)
Any single strong signal is enough (since signals are rarer on mobile):
```
IF (back_button_detected AND time_on_page >= 20s)
OR (tab_switch AND time_on_page >= 30s AND page_type IN [product, cart])
OR (scroll_reversal_from_70pct AND time_on_page >= 25s)
THEN show_bottom_sheet(tier_based_on_cart)
```

### Priority Queue (Advanced)
When multiple popups compete (exit intent, email capture, announcement bar), use a priority system:
1. Exit intent on cart page (highest revenue potential)
2. Exit intent on product page
3. Email capture on blog/content pages
4. Announcement bar (lowest priority, always yields)

Never show more than one popup per session unless the user explicitly engages with the first.

## Performance Requirements

- Popup JavaScript bundle: < 20 KB gzipped
- Load method: Lazy-load after page `load` event (never render-blocking)
- Layout impact: Zero CLS contribution (use `position: fixed` or `position: sticky`, never inject into document flow)
- Event listeners: Use passive listeners for scroll tracking (`{ passive: true }`)
- Cleanup: Remove all event listeners when popup is shown or dismissed
