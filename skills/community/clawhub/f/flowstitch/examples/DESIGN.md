# Design System: Furniture Collections List
**Project ID:** 13534454087919359824

*This is a gold-standard DESIGN.md example. It shows the level of detail and language quality expected for Stitch generation prompts.*

---

## 1. Visual Theme & Atmosphere

The Furniture Collections List embodies a **sophisticated, minimalist sanctuary** that marries the pristine simplicity of Scandinavian design with the refined visual language of luxury editorial presentation. The interface feels **spacious and tranquil**, prioritizing breathing room and visual clarity above all else. The design philosophy is gallery-like and photography-first, allowing each furniture piece to command attention as an individual art object.

The overall mood is **airy yet grounded**, creating an aspirational aesthetic that remains approachable and welcoming. Every element serves a clear purpose while maintaining visual sophistication. The atmosphere evokes the serene ambiance of a high-end furniture showroom where customers browse thoughtfully without visual overwhelm.

**Key Characteristics:**
- Expansive whitespace creating generous breathing room between elements
- Clean, architectural grid system with structured content blocks
- Photography-first presentation with minimal UI interference
- Whisper-soft visual hierarchy that guides without shouting
- Refined, understated interactive elements

## 2. Color Palette & Roles

### Primary Foundation
- **Warm Barely-There Cream** (#FCFAFA) – Primary page background. Creates an almost imperceptible warmth that feels more inviting than pure white.
- **Crisp Very Light Gray** (#F5F5F5) – Secondary surface for card backgrounds and content areas.

### Accent & Interactive
- **Deep Muted Teal-Navy** (#294056) – The sole vibrant accent. Used exclusively for primary CTAs ("Shop Now", "View all products"), active navigation links, and selected filter states.

### Typography & Text Hierarchy
- **Charcoal Near-Black** (#2C2C2C) – Primary text for headlines and product names.
- **Soft Warm Gray** (#6B6B6B) – Secondary text for body copy, descriptions, and supporting metadata.
- **Ultra-Soft Silver Gray** (#E0E0E0) – Borders, dividers, and subtle structural elements.

### Functional States
- **Success Moss** (#10B981) – Stock availability, confirmation states
- **Alert Terracotta** (#EF4444) – Low stock warnings, error states
- **Informational Slate** (#64748B) – Neutral system messages

## 3. Typography Rules

**Primary Font Family:** Manrope  
**Character:** Modern, geometric sans-serif with gentle humanist warmth. Slightly rounded letterforms that feel contemporary yet approachable.

- **Display Headlines (H1):** Semi-bold (600), letter-spacing 0.02em, 2.75–3.5rem
- **Section Headers (H2):** Semi-bold (600), letter-spacing 0.01em, 2–2.5rem
- **Product Names (H3):** Medium (500), normal letter-spacing, 1.5–1.75rem
- **Body Text:** Regular (400), line-height 1.7, 1rem
- **Small/Meta Text:** Regular (400), line-height 1.5, 0.875rem
- **CTA Buttons:** Medium (500), letter-spacing 0.01em, 1rem

## 4. Component Stylings

### Buttons
- **Shape:** Subtly rounded corners (8px) — approachable but not playful
- **Primary CTA:** Deep Muted Teal-Navy (#294056) background, pure white text
- **Hover:** Subtle darkening to deeper navy, 250ms ease-in-out transition
- **Focus:** Soft outer glow in primary color for keyboard accessibility
- **Padding:** 0.875rem vertical × 2rem horizontal

### Cards & Product Containers
- **Corner Style:** Gently rounded (12px/0.75rem)
- **Background:** Alternates between Warm Barely-There Cream and Crisp Very Light Gray
- **Shadow:** Flat by default. On hover: whisper-soft diffused (`0 2px 8px rgba(0,0,0,0.06)`)
- **Border:** Optional 1px hairline in Ultra-Soft Silver Gray (#E0E0E0)
- **Padding:** Generous 2–2.5rem internal
- **Images:** Full-bleed top, square or 4:3 ratio

### Navigation
- **Style:** Horizontal, generous item spacing (2–3rem)
- **Typography:** Medium weight (500), subtle uppercase, letter-spacing 0.06em
- **Active/Hover:** 200ms transition to Deep Muted Teal-Navy
- **Active Indicator:** 2px underline in Deep Muted Teal-Navy

### Inputs & Forms
- **Border:** 1px in Soft Warm Gray
- **Background:** Warm Barely-There Cream → Crisp Very Light Gray on focus
- **Corners:** 8px matching buttons
- **Focus:** Border shifts to Deep Muted Teal-Navy with subtle glow

## 5. Layout Principles

- **Max Width:** 1440px for visual balance on large displays
- **Grid:** Responsive 12-column, 24px mobile / 32px desktop gutters
- **Product Grid:** 4 columns large desktop → 3 desktop → 2 tablet → 1 mobile
- **Whitespace Base Unit:** 8px micro / 16px component / 32px section base
- **Section Margins:** 80–128px between major sections
- **Edge Padding:** 24px mobile / 48px tablet+desktop

## 6. Design System Notes for Stitch Generation

**Copy this block into every baton prompt:**

**DESIGN SYSTEM (REQUIRED):**
- Platform: Web, Desktop-first
- Theme: Light, minimal, photography-first, gallery-like
- Background: Warm barely-there cream (#FCFAFA)
- Surface: Crisp very light gray (#F5F5F5) for card backgrounds
- Primary Accent: Deep muted teal-navy (#294056) for CTAs and active states
- Text Primary: Charcoal near-black (#2C2C2C) for headlines
- Text Secondary: Soft warm gray (#6B6B6B) for body copy
- Font: Modern geometric sans-serif (Manrope or similar), clean and approachable
- Buttons: Subtly rounded corners (8px), comfortable padding, teal-navy fill
- Cards: Gently rounded (12px), whisper-soft shadow on hover only
- Layout: Centered content, 1440px max-width, generous whitespace, 80px+ section margins
