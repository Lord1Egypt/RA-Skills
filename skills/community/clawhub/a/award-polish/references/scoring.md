# How the 10 items are scored

**This ruler was calibrated against 5 real SOTDs and 1 template site that never won anything** (2026-10-13, see lessons.md): real award winners should mostly land at 9-10, template sites at 5-6.

**Do not mix the two scales**: these 10 items are our own ruler, with anchors in `reviewer.md` "Anchors". The Awwwards jury's own four items (design 40%, usability 30%, creativity 20%, content 10%) are stricter and are only used to compare with the references' real jury scores, see `reviewer.md`.

Independent reviewers score (reviewer.md: anchor calibration, 2 reviewers averaged, blind comparison with the best version so far). Self-scoring rules are in reviewer.md "Using review results". Scores go in the log; reports to the user do not read them out item by item.

| Item | What to look at | What 9 looks like |
|---|---|---|
| typography | type scale, line height, weight, alignment, line length | you know what matters without reading; comfortable line length; headings at most 2 lines |
| whitespace | section spacing, block spacing, card padding | one fixed spacing scale site-wide, steady breathing room, neither cramped nor empty |
| hierarchy | each screen's focus, primary and secondary buttons | one main focus per screen, the main button visible at a glance |
| color | use of primary and accent colors, contrast | one accent color across the site, WCAG AA contrast, no stray colors |
| motion | entrances, transitions, state changes | every animation has a purpose, short, smooth, never in the way; signature moments have a designed rhythm |
| micro-interactions | press, hover, input, success and failure feedback | instant feedback on every click, clear and pleasant success and failure responses. On marketing or concept sites without forms or results, judge whether hover, press, toggle and scroll-linked feedback is instant, consistent and on-brand |
| responsive | layout at the five widths (375, 768, 1024, 1280, 1440) | every width looks designed for that size, not just "not broken". Desktop-only back offices: the main widths look designed, phone widths readable and unbroken |
| originality | anything no template would have | 1-2 design points that belong only to this product and serve it |
| usability | steps, clarity, error guidance | new users finish the core flow without instructions; common actions take one or two steps. Marketing or concept sites: understanding what the product is and finding the main button within two scrolls is only the 6-point baseline; 9 also needs the first screen to say how it differs from similar products, in a way only this product could say it |
| retention | does anyone want to come back | sincere reasons to return: progress, growth, achievements, recaps, shortcuts. Tools are judged on rechecks, progress and reminders, shareable results, with no deductions for missing levels or points. Marketing sites, portfolios and studio sites are judged on memorability and conversion: whether people want to get in touch or share it, not on return visits |

## What is not scored

Only the 10 items above are scored. The following are pass/fail, because a 7 or an 8 on them means nothing and suggests "almost is fine":

| Check | Record |
|---|---|
| Layout check (spacing, alignment, overflow at five widths) | pass / fail, listing the spots that fail |
| Key elements in the first screen (main button, first result fully visible, not covered by banners or overlays) | pass / fail, y values per width |
| Core flow clicks through | pass / fail |
| Project rules (dashes, theme, console errors, etc.) | pass / fail |
| Performance and accessibility (Lighthouse, LCP, CLS, image size, keyboard) | pass / fail, with numbers |
| Signature moments | each marked "not started / needs polish / done" |

Any failure here outranks raising scores. How good the signature moments are shows in the motion, micro-interactions, usability and retention scores; their status only tracks progress, so a moment cannot be left undone while scores look fine.

## Scoring discipline

- **Score against the references**: first ask "next to the award sites in the reference notes, how far off is this item", then score.
- **No leniency**: evidence rules are in reviewer.md rule 1.
- Scores that only ever go up are suspicious. If something got worse, lower the score honestly.
- Versions are compared by the item-by-item blind comparison (reviewer.md "Comparing with the best version"); absolute scores only count when both rounds used the same reviewer model.
- The finish conditions are in SKILL.md "When to stop". Anchors are in `reviewer.md`.
