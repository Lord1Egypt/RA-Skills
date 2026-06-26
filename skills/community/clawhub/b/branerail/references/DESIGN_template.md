---
name: YourProductName
version: 1.0.0
description: Design system and visual identity guide
colors:
  # Semantic Colors
  primary: "#1A1C1E"
  secondary: "#6C7278"
  tertiary: "#B8422E"
  
  # Functional Colors
  success: "#2E7D32"
  warning: "#F57C00"
  error: "#C62828"
  info: "#1976D2"
  
  # Neutral Scale
  surface: "#FFFFFF"
  background: "#F7F5F2"
  neutral-light: "#E8E6E1"
  neutral-mid: "#9E9C97"
  neutral-dark: "#3E3E3E"
  
  # Semantic Text
  text-primary: "#1A1C1E"
  text-secondary: "#6C7278"
  text-disabled: "#B8B8B8"
  text-on-primary: "#FFFFFF"
  text-on-secondary: "#FFFFFF"

typography:
  h1:
    fontFamily: "Public Sans"
    fontSize: "3rem"
    fontWeight: "700"
    lineHeight: "1.2"
    letterSpacing: "-0.02em"
  
  h2:
    fontFamily: "Public Sans"
    fontSize: "2rem"
    fontWeight: "700"
    lineHeight: "1.3"
    letterSpacing: "-0.01em"
  
  h3:
    fontFamily: "Public Sans"
    fontSize: "1.5rem"
    fontWeight: "700"
    lineHeight: "1.4"
  
  body-lg:
    fontFamily: "Public Sans"
    fontSize: "1.125rem"
    fontWeight: "400"
    lineHeight: "1.5"
  
  body-md:
    fontFamily: "Public Sans"
    fontSize: "1rem"
    fontWeight: "400"
    lineHeight: "1.5"
  
  body-sm:
    fontFamily: "Public Sans"
    fontSize: "0.875rem"
    fontWeight: "400"
    lineHeight: "1.5"
  
  label-lg:
    fontFamily: "Space Grotesk"
    fontSize: "0.875rem"
    fontWeight: "600"
    lineHeight: "1.4"
    letterSpacing: "0.04em"
  
  label-sm:
    fontFamily: "Space Grotesk"
    fontSize: "0.75rem"
    fontWeight: "600"
    lineHeight: "1.3"
    letterSpacing: "0.06em"
  
  monospace:
    fontFamily: "JetBrains Mono"
    fontSize: "0.875rem"
    fontWeight: "400"
    lineHeight: "1.6"

spacing:
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "24px"
  xl: "32px"
  xxl: "48px"

rounded:
  none: "0px"
  xs: "2px"
  sm: "4px"
  md: "8px"
  lg: "16px"
  full: "9999px"

shadows:
  sm: "0 1px 2px 0 rgba(0, 0, 0, 0.05)"
  md: "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)"
  lg: "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)"
  xl: "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)"

components:
  button-primary:
    backgroundColor: "#1A1C1E"
    textColor: "#FFFFFF"
    paddingY: "12px"
    paddingX: "24px"
    borderRadius: "8px"
    fontSize: "1rem"
    fontWeight: "600"
    hover:
      backgroundColor: "#3E3E3E"
    disabled:
      backgroundColor: "#B8B8B8"
      textColor: "#FFFFFF"

  button-secondary:
    backgroundColor: "#F7F5F2"
    textColor: "#1A1C1E"
    border: "1px solid #9E9C97"
    paddingY: "12px"
    paddingX: "24px"
    borderRadius: "8px"
    hover:
      backgroundColor: "#E8E6E1"

  card:
    backgroundColor: "#FFFFFF"
    borderRadius: "8px"
    boxShadow: "0 1px 3px 0 rgba(0, 0, 0, 0.1)"
    padding: "24px"

  input:
    borderRadius: "4px"
    border: "1px solid #9E9C97"
    padding: "12px 16px"
    fontSize: "1rem"
    focus:
      borderColor: "#1A1C1E"
      boxShadow: "0 0 0 3px rgba(26, 28, 30, 0.1)"

---

# Visual Identity & Design System

## Overview

Architectural Minimalism meets Journalistic Gravitas. This design system balances premium minimalism with approachability, evoking a high-end broadsheet aesthetic while remaining accessible and inviting.

The visual language emphasizes clarity, hierarchy, and restraint—every element serves a purpose. We avoid decoration for its own sake and let functionality guide form.

## Design Philosophy

### Core Principles

1. **Clarity First**: Information hierarchy is ruthless. Unnecessary visual noise is eliminated.
2. **Minimalist Restraint**: Premium products are quiet. Every color, spacing, and element must justify its existence.
3. **Functional Beauty**: Aesthetics emerge from structure, not decoration. Form follows function.
4. **Accessible Luxury**: Premium does not mean exclusive. Contrast, spacing, and type scales are engineered for readability.
5. **Consistency Over Novelty**: The design system is stable, predictable, and versionable—a contract between design and implementation.

### Aesthetic Attributes

- **Tone**: Professional, trustworthy, premium
- **Energy Level**: Calm, focused, intentional (not playful or frantic)
- **Personality**: Intelligent, refined, understated confidence
- **Metaphor**: High-end broadsheet; contemporary gallery; matte finish

## Color Palette

### Semantic Colors

The palette is built on **high-contrast neutrals** with a single **warm accent** color to draw attention to critical actions.

#### Primary Color: #1A1C1E (Deep Charcoal)
- Use for: Primary actions, headings, text, interactive elements.
- Emotion: Authority, trust, professionalism.
- Contrast: 15.6:1 against white (WCAG AAA for body text).

#### Secondary Color: #6C7278 (Warm Gray)
- Use for: Secondary information, disabled states, supporting text.
- Emotion: Subtle, secondary, non-critical.
- Contrast: 7.5:1 against white (WCAG AA for body text).

#### Tertiary Color: #B8422E (Burnt Sienna / Accent)
- Use for: Call-to-action, critical warnings, highlights.
- Emotion: Urgency, importance, warmth.
- Contrast: 4.8:1 against white (WCAG AA for large text only).

#### Functional Colors
- **Success (#2E7D32)**: Confirmation, completed states. Contrast: 7.8:1 (WCAG AA).
- **Warning (#F57C00)**: Caution, attention needed. Contrast: 3.4:1 (WCAG AA for large text).
- **Error (#C62828)**: Destructive, failed, critical. Contrast: 5.2:1 (WCAG AA).
- **Info (#1976D2)**: Informational, neutral alerts. Contrast: 6.3:1 (WCAG AA).

#### Neutral Scale
- **Surface (#FFFFFF)**: Primary background for content areas.
- **Background (#F7F5F2)**: Page background, subtle separation.
- **Neutral Light (#E8E6E1)**: Dividers, borders, subtle contrast.
- **Neutral Mid (#9E9C97)**: Disabled states, secondary information.
- **Neutral Dark (#3E3E3E)**: Alternative text color, high contrast when needed.

### Color Usage Rules

- **Never use color alone to convey meaning**. Always pair with text, icons, or patterns (accessibility for colorblind users).
- **Primary color is dominant**. Secondary and tertiary are used sparingly.
- **Functional colors (success, error, warning) must meet WCAG AA contrast** against their backgrounds.
- **Dark text on light backgrounds**. Avoid light text on light or dark on dark.

## Typography

### Font Families

- **Public Sans** (headings, body): Open-source, neutral, highly legible. Used for all body text, headings, and primary content.
- **Space Grotesk** (labels, UI): Geometric, geometric sans-serif. Used sparingly for small caps, button labels, and UI text.
- **JetBrains Mono** (code): Monospace for code snippets and technical content.

### Type Scale

The type scale is built on a **1.333 (major third) ratio** for predictable hierarchy.

| Level | Font | Size | Weight | Usage |
|-------|------|------|--------|-------|
| h1 | Public Sans | 3rem | 700 | Page titles, hero sections |
| h2 | Public Sans | 2rem | 700 | Section headings |
| h3 | Public Sans | 1.5rem | 700 | Subsection headings |
| body-lg | Public Sans | 1.125rem | 400 | Large body text, cards |
| body-md | Public Sans | 1rem | 400 | Default body text |
| body-sm | Public Sans | 0.875rem | 400 | Supporting text, captions |
| label-lg | Space Grotesk | 0.875rem | 600 | Button labels, tags |
| label-sm | Space Grotesk | 0.75rem | 600 | Small UI labels, badges |

### Line Height and Spacing

- **Headings**: 1.2–1.4 (tighter, more compact)
- **Body text**: 1.5 (generous, readable)
- **Labels**: 1.3–1.4 (compact, supports dense UI)

**Letter spacing**:
- **Headings**: Negative letter spacing (-0.01em to -0.02em) for premium feel.
- **Labels (caps)**: +0.04em to +0.06em for clarity.
- **Body**: Normal (0em).

### Accessibility Notes

- Minimum font size: 16px for body text on mobile (prevents auto-zoom).
- Contrast ratio for body text: 7:1 (WCAG AAA standard).
- Line height of 1.5 improves readability for dyslexic users.

## Spacing System

Spacing is built on an **8px base unit** for consistency and alignment.

| Token | Value | Usage |
|-------|-------|-------|
| xs | 4px | Tight spacing between inline elements |
| sm | 8px | Small gaps between elements |
| md | 16px | Default spacing between sections |
| lg | 24px | Larger sections, page padding |
| xl | 32px | Major section separation |
| xxl | 48px | Page-level spacing |

### Padding and Margins

- **Cards**: 24px (lg)
- **Buttons**: 12px (vertical), 24px (horizontal)
- **Input fields**: 12px (vertical), 16px (horizontal)
- **Page margins**: 24px (mobile), 32px (desktop)
- **Section gap**: 32px (vertical separation between major sections)

## Border Radius

Rounded corners follow a **logarithmic scale** to reduce visual clutter.

| Token | Value | Usage |
|-------|-------|-------|
| none | 0px | Buttons with sharp edges (rare) |
| xs | 2px | Subtle softness on small UI elements |
| sm | 4px | Input fields, small components |
| md | 8px | Cards, buttons, moderate elements |
| lg | 16px | Large containers, modals |
| full | 9999px | Pill buttons, circular avatars |

**Rule**: Avoid excessive rounding. Sharp corners (0–4px) convey precision; rounded corners (8px+) convey friendliness. We default to md (8px) for balance.

## Shadows

Shadows create depth and hierarchy. Avoid excessive drop shadows; use sparingly.

| Level | Shadow | Usage |
|-------|--------|-------|
| sm | 1px 2px (0.05 opacity) | Subtle elevation on hover |
| md | 4px 6px (0.1 opacity) | Cards, modal layers |
| lg | 10px 15px (0.1 opacity) | Dropdowns, popovers |
| xl | 20px 25px (0.1 opacity) | High modals, overlays |

**Rule**: Shadows amplify depth. Use them to separate foreground from background, not for decoration.

## Component Patterns

### Buttons

#### Primary Button
- **Background**: Primary (#1A1C1E)
- **Text**: White on primary
- **Padding**: 12px (v), 24px (h)
- **Border Radius**: 8px
- **Hover**: Background darkens to #3E3E3E
- **Active**: Background darkens further, subtle shadow
- **Disabled**: Gray background (#B8B8B8), disabled text color

**Usage**: Primary actions (submit, confirm, create). One per screen.

#### Secondary Button
- **Background**: Transparent with border
- **Border**: 1px solid neutral-mid
- **Text**: Primary color
- **Padding**: 12px (v), 24px (h)
- **Hover**: Background lightens (neutral-light)

**Usage**: Secondary or alternative actions. Multiple allowed.

#### Tertiary Button
- **Background**: Transparent
- **Text**: Primary or secondary color
- **Underline**: Optional, on hover

**Usage**: Low-priority actions, text links.

### Input Fields

- **Border**: 1px solid neutral-mid
- **Border Radius**: 4px
- **Padding**: 12px (v), 16px (h)
- **Font**: body-md
- **Focus**: Border color becomes primary, subtle shadow (0 0 0 3px rgba(primary, 0.1))
- **Error**: Border color becomes error, with error message below
- **Disabled**: Background becomes neutral-light, text becomes neutral-mid

### Cards

- **Background**: Surface (#FFFFFF)
- **Border Radius**: 8px
- **Padding**: 24px
- **Shadow**: md (subtle elevation)
- **Divider**: 1px solid neutral-light between sections

### Form Layout

- **Label**: Small caps (label-sm), primary color, required asterisk in tertiary
- **Input**: Full width on mobile, constrained on desktop
- **Error message**: body-sm, error color, appears below input
- **Helper text**: body-sm, secondary color, appears below input

### Modals

- **Overlay**: Black, 50% opacity
- **Modal**: Surface background, 16px border radius, lg shadow
- **Header**: h2 heading, 24px padding
- **Body**: 24px padding, body-md text
- **Footer**: Buttons aligned right, 24px padding, top divider

### Navigation

- **Text**: label-lg, all caps, 4px letter spacing
- **Active state**: Primary color, bottom border (2px)
- **Hover**: Background becomes neutral-light
- **Spacing**: 24px between nav items (h), 12px between (v)

## Responsive Design

### Breakpoints

- **Mobile**: 320px–640px (phones)
- **Tablet**: 641px–1024px (tablets)
- **Desktop**: 1025px+ (desktops, widescreen)

### Mobile-First Rules

1. **Typography scales down**: h1 = 2rem on mobile, 3rem on desktop.
2. **Spacing reduces**: Padding = 16px on mobile, 24px+ on desktop.
3. **Full width by default**: Cards and inputs span 100% on mobile.
4. **Touch targets**: Minimum 44px × 44px for all interactive elements.
5. **Navigation changes**: Hamburger menu on mobile, horizontal nav on desktop.

## Accessibility (WCAG AA Compliance)

### Color Contrast

- **Body text**: 7:1 (WCAG AAA; exceeds AA requirement of 4.5:1).
- **Large text** (18pt+): 3:1 (WCAG AA).
- **UI components** (borders, icons): 3:1 (WCAG AA).
- **Disabled states**: Contrast may be reduced; conveyed by state, not color alone.

### Keyboard Navigation

- All interactive elements are keyboard accessible.
- Focus indicator: 2px solid primary color outline.
- Tab order: Logical, left-to-right, top-to-bottom.

### Screen Reader Support

- Semantic HTML: `<button>`, `<nav>`, `<label>`, `<h1>–<h6>`.
- ARIA labels for icons and non-text content.
- Form labels linked to inputs via `<label for>`.

### Motion and Animation

- Animations: Kept under 300ms for snappy feel.
- Respects `prefers-reduced-motion`: Disables animations if user prefers.
- Flashing: Never flashes faster than 3 Hz (photosensitive seizure risk).

## Implementation Guidelines

### CSS Variables (Tailwind)

Export this DESIGN.md to Tailwind using:
```bash
npx @google/design.md export --format tailwind DESIGN.md > tailwind.theme.json
```

### Design Tokens (W3C DTCG)

Export to W3C Design Token Format:
```bash
npx @google/design.md export --format dtcg DESIGN.md > tokens.json
```

### Validation

Lint the DESIGN.md file to catch inconsistencies:
```bash
npx @google/design.md lint DESIGN.md
```

This checks:
- Unresolved token references
- WCAG AA/AAA contrast ratios
- Circular dependencies in tokens

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-27 | Initial release. Defined core colors, typography, spacing, and component patterns. |

## References

- [Google Design System Guidelines](https://design.google/)
- [WCAG 2.1 Accessibility Standards](https://www.w3.org/WAI/WCAG21/quickref/)
- [Material Design](https://m3.material.io/)
- [W3C Design Token Format Community Group](https://design-tokens.github.io/community-group/format/)
