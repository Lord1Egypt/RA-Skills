---
name: accessibility-scanner
description: Scan web applications for accessibility issues — WCAG 2.2 compliance, screen reader compatibility, keyboard navigation, color contrast, and ARIA usage.
metadata:
  tags: ["accessibility", "a11y", "wcag", "web", "compliance"]
---

# Accessibility Scanner

Scan web applications for WCAG 2.2 compliance issues including screen reader compatibility, keyboard navigation, color contrast, ARIA usage, semantic HTML, and focus management. Use for accessibility audits, compliance reviews, or improving inclusive design.

## Usage

```
"Scan my app for accessibility issues"
"Check WCAG compliance on these pages"
"Audit ARIA usage in my components"
"Review keyboard navigation"
```

## How It Works

### 1. Static Analysis

Scan source code for common a11y issues:

```bash
# Find images without alt text
grep -rn '<img' src/ | grep -v 'alt='
# Find buttons without accessible names
grep -rn '<button' src/ | grep -v 'aria-label\|aria-labelledby'
# Find interactive elements without keyboard handlers
grep -rn 'onClick' src/ | grep -v 'onKeyDown\|onKeyPress\|role="button"'
# Find form inputs without labels
grep -rn '<input' src/ | grep -v 'aria-label\|id.*label\|aria-labelledby'
```

### 2. WCAG 2.2 Checklist

**Level A (must have):**
- All images have alt text (1.1.1)
- All form inputs have labels (1.3.1)
- Color not sole means of conveying info (1.4.1)
- All functionality available via keyboard (2.1.1)
- No keyboard traps (2.1.2)
- Page has title (2.4.2)
- Link purpose clear from text (2.4.4)

**Level AA (should have):**
- Color contrast ≥4.5:1 for text (1.4.3)
- Text resizable to 200% without loss (1.4.4)
- Skip navigation links (2.4.1)
- Focus visible on all interactive elements (2.4.7)
- Consistent navigation (3.2.3)
- Error identification (3.3.1)

**Level AAA (nice to have):**
- Color contrast ≥7:1 (1.4.6)
- Sign language for media (1.2.6)

### 3. Component-Level Audit

For each interactive component:
- Proper ARIA roles and states
- Focus management (modals, dropdowns, tabs)
- Keyboard interaction patterns match WAI-ARIA practices
- Screen reader announcements for dynamic content
- Touch target size (44x44px minimum)

### 4. Automated Testing Integration

Recommend tools:
- `@axe-core/playwright` or `@axe-core/react` for CI
- `eslint-plugin-jsx-a11y` for lint-time checks
- Lighthouse accessibility audit
- NVDA/VoiceOver manual testing checklist

## Output

```
## Accessibility Audit Report

**WCAG Target:** 2.2 Level AA
**Pages scanned:** 12 | **Components:** 45

### Compliance Score: 72/100

### 🔴 Critical (5)
1. **13 images missing alt text** across 8 pages
2. **Custom dropdown** has no keyboard navigation
3. **Modal** doesn't trap focus (Tab escapes to background)
4. **3 form inputs** missing label association
5. **Color contrast** fails on 2 button styles (3.2:1, need 4.5:1)

### 🟡 Warnings (8)
6. No skip navigation link
7. Focus indicator invisible on 4 interactive elements
8. Tab order illogical in settings form
[...]

### ✅ Passing
- Semantic HTML used for page structure
- ARIA landmarks present (main, nav, footer)
- Proper heading hierarchy (single h1, ordered nesting)
- Form error messages associated with inputs
```
