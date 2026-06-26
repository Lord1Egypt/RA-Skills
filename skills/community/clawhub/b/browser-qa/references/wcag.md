# WCAG AA Accessibility Checklist

## Critical Violations (Must Fix)

### Contrast

- Text contrast ratio ≥ 4.5:1 for normal text
- Text contrast ratio ≥ 3:1 for large text (18pt+)
- Use tools: axe-core, WAVE, WebAIM contrast checker

### Images & Icons

- All `<img>` must have descriptive `alt` text
- Decorative images: `alt=""`
- Icon buttons: must have aria-label or text
- Logos: describe the brand/page

### Form Labels

- Every input must have associated `<label>`
- Use `htmlFor` attribute linking to input `id`
- Error messages linked to input via `aria-describedby`

### Keyboard Navigation

- All interactive elements keyboard accessible (Tab key)
- Tab order logical (top-to-bottom, left-to-right)
- No keyboard trap (user can tab out)
- No reliance on mouse-only interactions

### Semantic HTML

- Use proper heading hierarchy (`<h1>` → `<h2>` → `<h3>`)
- Use `<button>` for buttons, not `<div onclick>`
- Use `<nav>`, `<main>`, `<article>`, `<footer>` landmarks
- Links must have text content (visible or aria-label)

## Common Violations

| Issue | Fix |
|-------|-----|
| Missing alt text on images | Add descriptive alt: `<img alt="Product photo">` |
| Color-only communication | Add text label or icon: "✓ Required" not just green |
| Insufficient contrast | Use contrast checker, aim for 4.5:1 ratio |
| Missing focus indicator | Add `:focus { outline: 2px solid #0066cc }` |
| Click-only interactions | Add keyboard handler: `onKeyDown={(e) => e.key === 'Enter' && action()}` |
| Form errors without labels | Link error via aria-describedby |
| Decorative elements announced | Use `aria-hidden="true"` on decorative icons |
| No landmarks | Add `<nav>`, `<main>`, `<footer>` |

## Testing Procedure

### Automated (axe-core)

```bash
npm install --save-dev @axe-core/react
# Reports WCAG violations in browser console
```

### Manual Checklist

1. Disable CSS — content still readable, semantic
2. Keyboard-only navigation — can use entire site with Tab + Enter
3. Screen reader (NVDA, JAWS, VoiceOver) — all content announced, landmarks clear
4. Dark mode test — contrast still sufficient
5. 200% zoom — no overlap, layout reflows properly

## WCAG AA (Web Content Accessibility Guidelines Level AA)

Target level for most public websites. Covers:

- Perceivable: content readable by all (color, text size, contrast)
- Operable: keyboard, touch, no seizure hazards
- Understandable: clear language, predictable, error prevention
- Robust: compatible with assistive technology

**Common target:** WCAG AA 2.1 is industry standard. Most violations are contrast, labels, and keyboard navigation.
