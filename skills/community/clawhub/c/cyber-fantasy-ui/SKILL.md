---
name: cyber_fantasy_ui
description: Generate dark neon cyber-fantasy dashboards, glassmorphism surfaces, and gamified React and Tailwind UIs.
user-invocable: true
metadata: {"openclaw":{"emoji":"🪷","homepage":"https://github.com/isdou/aoleme-ui-skill"},"author":"isdou","license":"MIT","tags":["ui","design-system","tailwind","react","glassmorphism","frontend","cyberpunk","dashboard","gamified","neon","dark-ui","fantasy-ui","mobile-ui","mystic-ui","game-ui"],"aliases":["aoleme_ui","aoleme","cyber xianxia ui","cyber_xianxia_ui","cyber fantasy ui"]}
---

# Cyber Fantasy UI Skill

Also known as Aoleme UI and Cyber Xianxia UI Skill in earlier versions of this repository.

Use this skill when the user wants a dark, cyber-fantasy, neon, glassmorphism, or game-like interface, especially in React and Tailwind projects.

This skill provides a visual system, reusable component patterns, and implementation guidance. It is best suited for dashboards, gamified pages, member systems, event pages, status panels, and immersive app surfaces.

## Example Prompts

Typical prompts that should match this skill:

- Design a dark neon dashboard for a fantasy progress tracker in React and Tailwind.
- Restyle this membership center into a cyber-fantasy glassmorphism interface.
- Build a game-like profile page with purple glow, liquid progress bars, and glass cards.
- Turn this plain admin page into a mystical sci-fi event page without changing the data structure.
- Create a mobile-first gamified task screen with dark panels, glowing actions, and merit status indicators.
- Restyle this app into a cultivation-themed dark UI with glass cards and luminous status badges.

## When To Use

Use this skill when the request mentions one or more of the following:

- cyberpunk, cyber fantasy, mystical sci-fi, dark fantasy, neon, glassmorphism
- dark game-like dashboard or immersive activity page
- purple-led visual system with glowing surfaces and liquid progress effects
- a need to restyle an existing React or Tailwind UI into this aesthetic

Do not force this skill onto products that already have a well-defined design system unless the user explicitly wants this style.

## What To Read First

Before making changes, inspect these files from the skill directory:

- `{baseDir}/resources/tailwind.config.js`
- `{baseDir}/resources/global.css`

Use them as source material. Merge and adapt them instead of copying everything blindly.

## Execution Workflow

When applying this skill, follow this order:

1. Inspect the target project stack and confirm whether it uses Tailwind, React, or plain CSS.
2. Read `{baseDir}/resources/tailwind.config.js` and merge only the required `theme.extend` tokens, colors, fonts, animations, and keyframes into the target Tailwind config.
3. Read `{baseDir}/resources/global.css` and copy only the variables and utility classes that the target UI actually needs.
4. Build or restyle the UI using the visual rules and component recipes in this skill.
5. Verify responsiveness, text contrast, scroll behavior, and pointer target sizes before finishing.

## Adaptation Rules

Apply this design system selectively and preserve the host application's structure.

- Prefer extending the project's existing design tokens over replacing them wholesale.
- Reuse the palette and motion language even if the project does not use every helper class.
- Keep visual density intentional. Use glow, blur, and motion as accents, not everywhere.
- If the app already has components, restyle them before creating brand new abstractions.

Do not blindly import all global styles from `{baseDir}/resources/global.css`. In particular:

- do not keep `body { overflow: hidden; }` unless the product is intentionally a full-screen experience
- do not disable text selection globally unless the interface truly needs it
- do not add expensive blur and animation effects to large scrolling lists without checking performance

## Visual Language

Use these core cues:

- Background: very dark, near-black surfaces with layered depth
- Primary hue: mystical purple as the dominant brand color
- Accent hues: merit gold, health green, danger red, optional cool teal
- Surface treatment: translucent glass panels, frosted overlays, soft borders
- Motion: floating, shimmering, scanning, liquid-flow effects with restraint
- Typography: bold modern display treatment for headings, clean readable body text for content

## Core Patterns

Favor these building blocks:

- pill or rounded action buttons with purple gradients and glow
- glass-panel cards with subtle borders and status badges
- frosted inputs with strong focus states
- liquid progress bars for energy, growth, status, or completion meters
- highlighted icon containers for stats, rewards, states, and cultivation metaphors

## Quality Bar

Every implementation using this skill should preserve:

- readable contrast on dark backgrounds
- touch targets of at least 44 by 44 pixels
- animations based primarily on `opacity` and `transform`
- responsive behavior on both desktop and mobile
- restrained use of `will-change`, heavy blur, and animated filters

## Output Expectations

When you apply this skill in code:

- explain briefly which parts of the visual system you used
- mention whether you merged Tailwind tokens or only borrowed CSS patterns
- note any intentional deviations made to fit the host application's design system

## Resource Summary

- `{baseDir}/resources/tailwind.config.js`: colors, fonts, animations, keyframes
- `{baseDir}/resources/global.css`: CSS variables, glass utilities, liquid effects, text glow, performance helpers

Treat this skill as a design system reference and implementation guide, not as a command to replace the target project's architecture.
