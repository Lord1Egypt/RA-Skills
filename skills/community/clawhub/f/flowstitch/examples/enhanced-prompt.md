# Example: Prompt Enhancement

This shows the before/after of running FlowStitch §1 (Prompt Enhancement) on a vague user input.

---

## Example 1: Landing Page

### User Input (Vague)
> "Make a landing page for my fitness app called 'Pulse'. Use red and black. It should have a place for features and a hero section."

### Enhanced Prompt (Stitch-Optimized)

**Overall Purpose:** A high-energy, modern landing page for 'Pulse', a fitness tracking application. The vibe is powerful, motivating, and high-performance.

**DESIGN SYSTEM (REQUIRED):**
- Platform: Web, Desktop-first
- Theme: Dark, high-contrast, energetic
- Background: Deep Obsidian (#0f172a) for the primary canvas
- Primary Accent: Racing Red (#e11d48) for CTA buttons and active states
- Text Primary: Crisp White (#ffffff) for headlines
- Text Secondary: Soft Gray (#94a3b8) for body copy
- Font: Bold, condensed sans-serif (Inter Tight or similar) for speed and strength
- Buttons: Sharp-edged or slightly rounded (4px), full-width on mobile
- Layout: Full-width hero, centered content, max-width 1280px container

**PAGE STRUCTURE:**
1. **Header:** Minimalist navigation — Pulse logo (left), nav links (center), "Start Training" primary red CTA (right)
2. **Hero Section:** Large, emotive athletics photography background. Headline: "Elevate Every Beat." Subheadline: "Track, analyze, and crush your fitness goals with Pulse." Primary red CTA: "Get Started Free"
3. **Feature Grid:** Three-column layout:
   - **Real-time Tracking:** Live stats from your wearable
   - **AI Coaching:** Personalized workouts based on performance
   - **Community Challenges:** Compete with friends and stay motivated
4. **Social Proof:** Horizontal strip — "Trusted by 500,000+ athletes" with user avatars
5. **Pricing Section:** Three-tier cards (Free / Pro / Team) with feature comparison
6. **Footer:** Quick links (Training, Pricing, Support), social icons, legal

---

## Example 2: Simple Login Page

### User Input (Vague)
> "make me a login page"

### Enhanced Prompt (Stitch-Optimized)

A clean, trustworthy login page with a centered form and minimal branding.

**DESIGN SYSTEM (REQUIRED):**
- Platform: Web, Desktop-first
- Theme: Light, minimal, professional
- Background: Clean White (#ffffff) for page canvas
- Surface: Soft Gray (#f9fafb) for form card
- Primary Accent: Deep Blue (#2563eb) for submit button and links
- Text Primary: Near Black (#111827) for labels and headings
- Text Secondary: Medium Gray (#6b7280) for placeholder text
- Font: Clean sans-serif (Inter or system default)
- Buttons: Subtly rounded (8px), full-width within form
- Cards: Gently rounded (12px), soft shadow for elevation

**Page Structure:**
1. **Header:** Minimal logo, centered at top
2. **Login Card:** Centered form — email input, password input, "Forgot password?" link
3. **Submit Button:** Primary blue "Sign In" button, full-width
4. **Divider + Social:** "Or continue with" — Google + GitHub sign-in buttons
5. **Footer Link:** "Don't have an account? Sign up"

---

## Example 3: Targeted Edit

### User Input
> "add a search bar to my header"

### Enhanced Prompt (Stitch Edit)

Add a search bar to the existing header navigation.

**Specific changes:**
- **Location:** Header, right side, before user avatar
- **Style:** Pill-shaped input with soft gray background (#f3f4f6), subtle border (#e5e7eb)
- **Icon:** Magnifying glass icon inside the input on the left, in medium gray (#9ca3af)
- **Placeholder:** "Search..." in light gray
- **Focus behavior:** Expands from 200px to 320px width with subtle shadow and border color shift to brand primary
- **Width:** 200px default, 320px on focus (smooth CSS transition)

**Context:** This is a targeted edit. Preserve all existing header elements and make only this change.

---

💡 **Key patterns:**
- Notice how vague colors ("red and black") become precise hex codes with semantic roles
- Vague sections ("place for features") become numbered, specific components
- The DESIGN SYSTEM block is always present and copy-paste ready
- Edit prompts are precise and scope-limited to avoid unwanted changes
