# Production Quality Gates

Read this reference before verification of a substantial frontend implementation.

## Contract-Driven Verification

Run the application through an HTTP preview for release-quality checks:

```bash
python3 <skill-dir>/scripts/verify-ui.py http://127.0.0.1:3000 \
  --contract .codex/design-guide/design-contract.json \
  --project-root . \
  --out .codex/design-guide/verification
```

The verifier runs each declared flow at every contract breakpoint, captures screenshots, records console and page errors, checks horizontal overflow, runs accessibility checks when `axe-core` is available, compares visual baselines, records browser performance metrics, and optionally runs Lighthouse.

Dependencies:

- Playwright is required. Install Python Playwright or use a host-provided `pw-python`.
- Use the system Chromium with `--chromium` when bundled browsers are unavailable.
- Install `axe-core` in the project or pass `--axe-script <axe.min.js>`.
- Install Lighthouse or pass `--lighthouse-command <binary>` for HTTP release verification.

`--allow-missing-tools` is acceptable for an early v0, never as evidence that a production gate passed. `file://` targets are useful for prototypes but skip Lighthouse and may not represent production routing or asset behavior.

## Accessibility

Automated checks are necessary but incomplete. Also verify:

- Complete keyboard order, visible focus, escape behavior, focus return, and no keyboard traps.
- Accessible names, labels, landmarks, headings, status announcements, and error association.
- Contrast in default, hover, focus, disabled, selected, error, and high-contrast-relevant states.
- Zoom and text reflow at 200%, pointer target size, reduced motion, and media alternatives.
- Dialog, menu, combobox, tabs, grid, drag/drop, and custom controls against their expected interaction patterns.

## Visual Regression

Use stable fixtures, fonts, browser versions, viewport dimensions, locale, time, and animation settings. Store intentional baselines in the target repository, not in the skill. Review the generated diff image before accepting a baseline update.

Compare screenshots directly when needed:

```bash
python3 <skill-dir>/scripts/visual-diff.py baseline.png current.png \
  --diff-out diff.png --max-ratio 0.01
```

## Performance

Treat browser timing as a fast regression signal and Lighthouse as the release audit. Also run the project's bundle analyzer or framework profiler when route weight, hydration, long tasks, image loading, fonts, or interaction latency are material. Do not claim Core Web Vitals from synthetic local metrics alone.

## No-Ship Conditions

Do not ship with failed declared flows, unreviewed screenshot changes, related console errors, horizontal overflow, inaccessible primary actions, missing critical states, broken reduced-motion behavior, or unexplained performance budget regressions.
