# Quality Check Reference

Verify your generated frontend code meets premium standards:

## Design System Adherence

- [ ] All colors match design.md tokens exactly
- [ ] Typography scale follows specifications
- [ ] Spacing uses base unit multiples only (4px, 8px, 16px, etc.)
- [ ] Border radius matches design tokens
- [ ] Shadows/elevation match specifications

## Accessibility (WCAG 2.1 AA)

### Visual
- [ ] Text contrast ≥ 4.5:1 ratio
- [ ] UI component contrast ≥ 3:1 ratio
- [ ] No color-only information conveyance
- [ ] Text resizable to 200%

### Interaction
- [ ] Tab order is logical (DOM order)
- [ ] All buttons/links keyboard accessible
- [ ] Focus indicator visible (2px minimum)
- [ ] Skip to main content link present
- [ ] Error messages associated with inputs

### Screen Reader
- [ ] Semantic HTML (header, main, footer, nav, article)
- [ ] ARIA labels on icons/buttons without text
- [ ] Form inputs have associated labels
- [ ] Dynamic content announced (aria-live)

## Performance

- [ ] Images have width/height attributes
- [ ] Lazy loading on below-fold images
- [ ] Fonts loaded with font-display: swap
- [ ] No layout shifts (CLS < 0.1)
- [ ] Critical CSS inlined
- [ ] JavaScript defer/async on non-critical

## 2026 Trends Check

- [ ] Glassmorphism effect on cards/modals (backdrop-filter)
- [ ] Smooth transitions (200-300ms duration)
- [ ] Hover states on all interactive elements
- [ ] Dark mode variants defined
- [ ] Responsive at all breakpoints
- [ ] No loading spinners (use skeletons)

## Code Quality

- [ ] Semantic HTML elements used
- [ ] CSS classes follow naming convention
- [ ] No inline styles (except CSS variables)
- [ ] Alt text on all images
- [ ] No console.log/debug code