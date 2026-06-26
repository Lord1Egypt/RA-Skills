---
name: frontend-premium
description: Create premium frontend interfaces with modern design systems. Forces generation of design.md for consistency, follows 2026 trends, ensures accessibility, and provides quality checks.
---

# Frontend Premium Skill

This skill helps agents generate premium-quality frontend interfaces by:
1. Forcing creation of a design.md file (Google Stitch style) for consistency
2. Following 2026 UI/UX trends (glassmorphism, bento grids, micro-animations)
3. Ensuring WCAG 2.1 AA accessibility compliance
4. Providing quality verification and recommendations
5. Suggesting modern tech stack (Motion, Lucide/Phosphor icons, Tailwind, RSC)

## 🎯 Core Workflow

When working on frontend tasks, the skill enforces this process:

1. **Generate design.md first** - Document your design system (colors, typography, spacing, components)
2. **Follow the design.md** - All UI generation must reference and follow this file
3. **Apply 2026 trends** - Incorporate glassmorphism, bento layouts, subtle animations
4. **Ensure accessibility** - WCAG 2.1 AA, keyboard nav, focus management
5. **Verify quality** - Check adherence to design system and best practices

## 📋 Files Generated

### design.md (Required)

A Google Stitch-style design system document that serves as the single source of truth for visual decisions.

**Structure:**
```markdown
## Colors
- Primary: #HEXVALUE
- Secondary: #HEXVALUE
- Background: #HEXVALUE
- Surface: #HEXVALUE
- Error: #HEXVALUE
- Text Primary: #HEXVALUE
- Text Secondary: #HEXVALUE

## Typography
- Font Family: Inter, sans-serif (or similar)
- Heading 1: SIZEpx, WEIGHT weight
- Heading 2: SIZEpx, WEIGHT weight
- Body: SIZEpx, WEIGHT weight
- Caption: SIZEpx, WEIGHT weight

## Spacing
- Base unit: 4px or 8px
- Values: 4, 8, 16, 24, 32, 48px

## Components
- Button border radius: VALUEpx
- Card border radius: VALUEpx
- Card shadow: OFFSET BLUR SPREAD COLOR
- Input border: WIDTHpx solid #HEXVALUE
```

### quality-check.md (Generated)

A verification checklist that validates the generated code against the design system.

## 🔥 2026 Trends to Apply

### Layout & Visuals
- **Glassmorphism & Frosted Glass** - Background-filter: blur, semi-transparent surfaces
- **Bento Grid Layouts** - Asymmetrical, card-based layouts inspired by Apple
- **Micro-interactions** - Subtle hover, focus, and animation states
- **Dark Mode First** - Design for dark mode as default, light as variant
- **Gradients Subtils** - Soft, natural gradients instead of harsh transitions
- **Bold Typography** - Expressive, large-scale typography for hierarchy
- **Neumorphism Soft** - Soft shadows and highlights for depth
- **Skeleton Loaders** - Content placeholders instead of spinners

### Interactions
- **Interactive Hover States** - All interactive elements respond to hover/focus
- **Motion Principles** - Easing, timing, spring physics for natural feel
- **Scroll-triggered Animations** - Elements animate as they enter viewport
- **Touch-friendly Targets** - Minimum 48x48px tap targets

## ♿ Accessibility Requirements

### Visual
- WCAG 2.1 AA minimum contrast ratios
- Text resize support (up to 200%)
- Color blindness friendly palettes
- Visible focus indicators (minimum 2px outline)

### Interaction
- Full keyboard navigation
- Logical tab order
- Skip navigation links
- ARIA labels for non-text content
- Error identification and suggestions

### Performance
- First Contentful Paint < 1.8s
- Time to Interactive < 3.5s
- Cumulative Layout Shift < 0.1
- Optimized images and assets

## 🛠 Recommended Tech Stack

### Framework & Rendering
- **Next.js 15** (App Router, Server Components)
- **React 19** with Concurrent Features
- **RSC优先** (React Server Components for performance)

### Styling
- **Tailwind CSS** - Utility-first, design token friendly
- **Motion** (framer-motion) - Production-grade animations
- **CSS Variables** - For design token consumption

### Icons
- **Lucide** - Clean, consistent SVG icons (default)
- **Phosphor** - Multiple weights/styles including duotone
- **Iconiq** - Motion-powered animated icons (for premium interactions)

### Development
- **TypeScript** - Strict mode for safety
- **ESLint + Prettier** - Code quality and formatting
- **Vitest** - Component testing
- **Playwright** - E2E testing

## 🔍 Quality Verification Checklist

When generating code, verify:

### Design System Adherence
- [ ] All colors from design.md used consistently
- [ ] Typography scale followed exactly
- [ ] Spacing values match base unit multiples
- [ ] Component styles match specifications

### Accessibility
- [ ] Color contrast ratios ≥ 4.5:1 (text), ≥ 3:1 (UI)
- [ ] All interactive elements keyboard accessible
- [ ] Focus visible and styled
- [ ] ARIA labels where needed
- [ ] Semantic HTML elements used

### Performance
- [ ] No layout shifts during loading
- [ ] Images optimized and lazy-loaded
- [ ] CSS/JS minified
- [ ] Critical CSS inlined

### Trends Applied
- [ ] Glassmorphism or frosted elements present
- [ ] Micro-interactions on hover/focus
- [ ] Responsive design (mobile-first)
- [ ] Dark mode variant considered

## 📚 References

See `references/` for:
- [Design token examples](references/design-tokens.md)
- [Accessibility checklist](references/a11y-checklist.md)
- [2026 trends deep dive](references/trends-2026.md)
- [Tech stack comparisons](references/tech-stack.md)

## 💡 Usage Tips

1. **Always start with design.md** - Generate it before any UI components
2. **Reference it constantly** - Ask "Does this match my design.md?" for every decision
3. **Iterate on the design** - Update design.md as you learn, then regenerate
4. **Test accessibility early** - Don't bolt it on at the end
5. **Keep it subtle** - 2026 trends favor refinement over flashiness

## 🚫 Common Pitfalls to Avoid

- ❌ Generating UI without a design system first
- ❌ Ignoring accessibility until QA
- ❌ Overusing trends (glassmorphism everywhere)
- ❌ Forgetting dark mode considerations
- ❌ Using animations that cause motion sickness
- ❌ Ignoring performance budgets
- ❌ Inconsistent spacing and typography
- ❌ Using raster icons instead of SVG

---

## Skill Files

| File | Description |
|------|-------------|
| **SKILL.md** (this file) | Core skill instructions |
| **references/design-tokens.md** | Design token examples and best practices |
| **references/a11y-checklist.md** | Detailed accessibility checklist |
| **references/trends-2026.md** | Deep dive on 2026 UI/UX trends |
| **references/tech-stack.md** | Tech stack recommendations and comparisons |

## 📦 Installation

This skill is already installed in your OpenClaw skills directory at:
`~/.openclaw/skills/frontend-premium/`

To use it, simply work on frontend tasks and the skill will automatically provide guidance.

## 🔄 Updates

To get the latest version of this skill, the skill-creator system will handle updates automatically when you run skill management commands.

---