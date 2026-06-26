---
name: cuihua-a11y-checker
description: |
  ♿ AI-powered accessibility (a11y) checker. Automatically detect WCAG violations, generate ARIA labels,
  test keyboard navigation, and ensure your app is accessible to everyone.

metadata:
  openclaw:
    requires:
      bins: [node]
      env: []
  
  version: "1.0.0"
  author: "翠花 (Cuihua) - ClawHub Pioneer"
  license: "MIT"
  tags: [accessibility, a11y, wcag, aria, keyboard-navigation, screen-reader, inclusive-design]

capabilities:
  - WCAG 2.1 compliance checking
  - Auto-generate ARIA labels
  - Keyboard navigation testing
  - Color contrast validation
  - Screen reader compatibility
  - Semantic HTML suggestions
---

# cuihua-a11y-checker ♿

> **Build accessible apps for everyone**

AI-powered accessibility assistant that ensures your app works for all users:
- ♿ **WCAG 2.1** compliance
- 🎯 **Auto-fix** common issues
- ⌨️ **Keyboard** navigation testing
- 🎨 **Color contrast** validation
- 📱 **Screen reader** optimization

## Why Accessibility Matters

- 🌍 **15% of population** has disabilities
- ⚖️ **Legal requirement** in many countries
- 📈 **Better UX** for everyone
- 🔍 **Better SEO** (search engines love semantic HTML)

## Quick Start

> "Check accessibility of src/components"

**Output:**
```
♿ Accessibility Report
━━━━━━━━━━━━━━━━━━━━

Files scanned: 12
Issues found: 18

🔴 CRITICAL (3):
  - Missing alt text on images (5 instances)
  - Form inputs without labels (2 instances)
  - Insufficient color contrast (1 instance)

🟡 WARNINGS (8):
  - Missing ARIA labels on buttons
  - Non-semantic HTML elements
  - Missing skip navigation link

🟢 SUGGESTIONS (7):
  - Add landmarks (header, main, footer)
  - Improve heading hierarchy
  - Add focus indicators
```

## Features

### 1. WCAG Compliance ✅

Check against WCAG 2.1 standards:

**Level A (Must have)**:
- Text alternatives for images
- Keyboard accessibility
- Color is not the only visual means
- Labels or instructions for forms

**Level AA (Should have)**:
- Color contrast ratio ≥ 4.5:1
- Resize text up to 200%
- Multiple ways to navigate
- Consistent navigation

**Level AAA (Nice to have)**:
- Color contrast ratio ≥ 7:1
- Sign language for audio
- Extended audio descriptions

### 2. Auto-fix Issues 🔧

**Before:**
```html
<img src="logo.png">
<button onclick="submit()">Click</button>
<div class="nav">...</div>
```

**After:**
```html
<img src="logo.png" alt="Company Logo">
<button onclick="submit()" aria-label="Submit form">Click</button>
<nav aria-label="Main navigation">...</nav>
```

### 3. Keyboard Navigation ⌨️

Test keyboard accessibility:

```
⌨️  Keyboard Navigation Test
━━━━━━━━━━━━━━━━━━━━━━━━

✅ Tab order is logical
❌ Focus indicator not visible
❌ Skip link missing
✅ All interactive elements reachable

Issues:
1. Add CSS for :focus state
2. Add skip navigation link
3. Ensure modal traps focus
```

### 4. Color Contrast 🎨

Validate color combinations:

```
🎨 Color Contrast Report
━━━━━━━━━━━━━━━━━━━━━

❌ FAIL: #777 on #fff
   Ratio: 4.47:1 (needs 4.5:1)
   Location: .text-muted class
   Fix: Use #767676 or darker

✅ PASS: #000 on #fff
   Ratio: 21:1

✅ PASS: #0066cc on #fff
   Ratio: 7.47:1
```

### 5. ARIA Labels 🏷️

Auto-generate semantic labels:

```html
<!-- Before -->
<button><i class="icon-search"></i></button>

<!-- After -->
<button aria-label="Search">
  <i class="icon-search" aria-hidden="true"></i>
</button>

<!-- Before -->
<div role="dialog">
  <h2>Confirm</h2>
  ...
</div>

<!-- After -->
<div role="dialog" aria-labelledby="dialog-title" aria-modal="true">
  <h2 id="dialog-title">Confirm</h2>
  ...
</div>
```

### 6. Screen Reader Testing 📢

Simulate screen reader experience:

```
📢 Screen Reader Output
━━━━━━━━━━━━━━━━━━━━━

Navigation:
  "Navigation, landmark"
  "Home, link"
  "About, link"
  "Contact, link"

Main content:
  "Main, landmark"
  "Welcome to our site, heading level 1"
  "Get started today, heading level 2"
  "Sign up, button"

Issues:
  - Button at line 45 has no accessible name
  - Image at line 67 has no alt text
```

## Usage Examples

### Example 1: Component Audit

**User:** "Check accessibility of LoginForm component"

**Agent:**
```
♿ Accessibility Audit: LoginForm.jsx
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 CRITICAL ISSUES (2):

1. Form inputs missing labels (line 12-15)
   <input type="email" name="email" />
   <input type="password" name="password" />
   
   Fix: Add labels
   <label htmlFor="email">Email</label>
   <input type="email" id="email" name="email" />

2. Submit button has no accessible name (line 18)
   <button type="submit"><Icon name="arrow" /></button>
   
   Fix: Add text or aria-label
   <button type="submit" aria-label="Sign in">
     <Icon name="arrow" />
   </button>

🟡 WARNINGS (1):

1. No error announcements for screen readers
   
   Fix: Add aria-live region
   <div aria-live="polite" aria-atomic="true">
     {error && <p>{error}</p>}
   </div>

WCAG Level: Currently D (not compliant)
After fixes: Level AA ✅
```

### Example 2: Color Contrast Fix

**User:** "Fix color contrast issues"

**Agent:**
```
🎨 Fixing color contrast...

Found 3 issues:

1. .text-muted (#777 on #fff)
   Current: 4.47:1 (FAIL)
   Fixed: #767676 (4.54:1) ✅

2. .btn-secondary (#999 on #fff)
   Current: 2.85:1 (FAIL)
   Fixed: #595959 (7.00:1) ✅

3. .link-subtle (#aaa on #fff)
   Current: 2.32:1 (FAIL)
   Fixed: #6c6c6c (4.50:1) ✅

Updated: styles.css
All contrasts now meet WCAG AA standard!
```

### Example 3: Keyboard Navigation

**User:** "Test keyboard navigation"

**Agent:**
```
⌨️  Testing keyboard navigation...

✅ PASS: Tab order follows visual order
✅ PASS: All interactive elements focusable
❌ FAIL: Focus indicator not visible
❌ FAIL: Modal doesn't trap focus
✅ PASS: Escape key closes modal

Recommendations:

1. Add visible focus styles:
   *:focus {
     outline: 2px solid #0066cc;
     outline-offset: 2px;
   }

2. Implement focus trap in modal:
   useEffect(() => {
     const focusableElements = modal.querySelectorAll(
       'button, [href], input, select, textarea'
     );
     // Trap focus logic...
   }, []);

3. Add skip navigation link:
   <a href="#main" class="skip-link">
     Skip to main content
   </a>
```

## Configuration

`.a11yrc.json`:

```json
{
  "wcagLevel": "AA",
  "rules": {
    "colorContrast": "error",
    "altText": "error",
    "ariaLabels": "warn",
    "headingOrder": "warn",
    "landmarks": "warn"
  },
  "ignore": [
    "node_modules/**",
    "build/**"
  ],
  "autoFix": {
    "altText": true,
    "ariaLabels": true,
    "colorContrast": false
  }
}
```

## Pricing

### Free
- ✅ Basic WCAG checks
- ✅ Up to 10 components

### Pro ($12/month)
- ✅ Full WCAG 2.1 suite
- ✅ Auto-fix suggestions
- ✅ CI/CD integration

### Enterprise ($99/month)
- ✅ Custom rules
- ✅ Compliance reports
- ✅ Team training

## Resources

- 📖 [WCAG Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- 🎓 [Accessibility Tutorial](./docs/tutorial.md)
- 💬 [Discord](https://discord.gg/clawd)

## License

MIT

---

**Made with 🌸 by 翠花 (Cuihua)**

_Build apps that work for everyone._
