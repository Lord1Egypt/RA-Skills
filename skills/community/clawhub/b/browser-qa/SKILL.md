---

name: browser-qa
description: "Automate visual testing and UI interaction verification. 4-phase methodology: smoke test (console errors, network status, Web Vitals), interaction test (forms, auth, user journeys), visual regression (breakpoints, dark mode), accessibility audit (WCAG AA, keyboard nav). Trigger phrases: browser test, visual testing, UI verification, QA checklist, pre-ship testing."
metadata: {"clawdbot":{"emoji":"\ud83e\uddea","requires":{"bins":[],"env":[]},"os":["linux","darwin","win32"],"version":"1.0.1"}}
---


# Browser QA — Automated Visual Testing & Interaction

Structured QA methodology for verifying UI behavior, visual consistency, and accessibility.


## Before You Run: Scope and Safety

This skill drives a real browser and can submit forms, log in, and complete
checkouts. Those actions change state on the target site.

**Use it only against sites you own or have written permission to test.**
Before the first interaction, confirm with the user:

- **Target URL** — a staging, sandbox, or test environment. Not production.
- **Test credentials** — a dedicated test account, never a personal or admin account.
- **Test payment data** — a sandbox/test card, never a real card.
- **What may be submitted** — which forms, which flows, and whether checkout
  may complete end-to-end.

**Never submit a form, create an account, log in with real credentials, or
complete a checkout on production unless the user explicitly approves that
exact action.** Do not treat "run the QA suite" as approval for state-changing
steps. If a flow is ambiguous, ask.

Prefer read-only checks first: navigate, assert on visible content, screenshot.
Only submit when the specific submission has been approved.

## Quick Start

1. **Phase 1: Smoke Test** — Navigate page, check for console errors, verify Core Web Vitals
2. **Phase 2: Interaction Test** — Click links, submit forms, verify user flows (login, checkout)
3. **Phase 3: Visual Regression** — Screenshot key pages at 3 breakpoints (375px, 768px, 1440px)
4. **Phase 4: Accessibility** — Run axe-core, verify keyboard nav, check screen reader landmarks

## Key Concepts

- **Smoke Test**: Detects hard-breaking errors before interaction testing wastes time
- **Interaction Test**: Verifies critical user journeys (auth, forms, checkout)
- **Visual Regression**: Detects layout shifts, missing elements, viewport overflow issues
- **Accessibility**: WCAG AA compliance, keyboard navigation, screen reader support

## Common Usage

### Phase 1: Smoke Test

```text
1. Navigate to target URL
2. Check for console errors (filter analytics noise)
3. Verify no 4xx/5xx in network requests
4. Screenshot above-the-fold (desktop + mobile)
5. Check Core Web Vitals: LCP < 2.5s, CLS < 0.1, INP < 200ms
```

### Phase 2: Interaction Test

```text
1. Click every nav link — verify no dead links
2. Submit forms with valid data — verify success state
3. Submit forms with invalid data — verify error state
4. Test auth flow: login → protected page → logout
5. Test critical journeys: checkout, onboarding, search
```

### Phase 3: Visual Regression

```text
1. Screenshot key pages at 3 breakpoints (375px, 768px, 1440px)
2. Compare against baseline screenshots (if stored)
3. Flag layout shifts > 5px, missing elements, overflow
4. Check dark mode if applicable
```

### Phase 4: Accessibility

```text
1. Run axe-core on each page
2. Flag WCAG AA violations (contrast, labels, focus order)
3. Verify keyboard navigation works end-to-end
4. Check screen reader landmarks
```

## Output Format

```text
## QA Report — [URL] — [timestamp]

### Smoke Test
- Console errors: 0 critical, 2 warnings (analytics noise)
- Network: all 200/304, no failures
- Core Web Vitals: LCP 1.2s ✓, CLS 0.02 ✓, INP 89ms ✓

### Interactions
- [✓] Nav links: 12/12 working
- [✗] Contact form: missing error state for invalid email
- [✓] Auth flow: login/logout working

### Visual
- [✗] Hero section overflows on 375px viewport
- [✓] Dark mode: all pages consistent

### Accessibility
- 2 AA violations: missing alt text, low contrast footer links

### Verdict: SHIP WITH FIXES (2 issues, 0 blockers)
```

## References

- `references/tools.md` — browser automation tools (claude-in-chrome, Playwright, Puppeteer)
- `references/wcag.md` — WCAG AA checklist and common violations

---

**Adapted from everything-claude-code by @affaan-m (MIT)**
