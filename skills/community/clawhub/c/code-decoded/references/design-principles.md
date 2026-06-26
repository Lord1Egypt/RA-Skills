# Design Principles

## The Rules

**Visual first.** Every screen should be at least 50% visual. If something can be a diagram, animation, or interactive element — it should not be a paragraph.

**Short text.** Max 2-3 sentences per text block. No walls of text. If you need more words, split into more sections.

**Real code only.** Code snippets are exact copies from the actual codebase. Never modify, simplify, or invent. The learner should be able to open the real file and see the exact same code.

**Application quizzes.** Test whether the learner can use what they learned to solve a new problem — not whether they can recall a definition. "Which file would you edit to change the login timeout?" not "What is JWT?"

**Specific metaphors.** Each concept gets a metaphor that fits that specific idea. A database is a library with a card catalog. Auth is a bouncer checking IDs. API rate limiting is a nightclub with a capacity limit. Never reuse the same metaphor for different concepts.

**No AI aesthetic.** Follow `no-slop-ui` rules. No gradient backgrounds, no glassmorphism, no oversized rounded corners, no decorative copy. Clean, functional, honest. Think product documentation from a company that cares.

## Visual Language

- **Architecture diagrams** — box and arrow, clean, labelled. Show the relationship between components, not the code.
- **Data flow** — step-by-step trace with numbered steps and highlighted code at each step
- **Animations** — subtle, purposeful. Show data moving between components. Not decorative.
- **Code/English split** — left column: code. Right column: plain English explanation of exactly that code. Line-by-line if needed.

## Colour

Use a calm, neutral palette. Dark mode preferred for code sections. Light mode for explanatory sections.

Suggested (adjust to match the repo's existing branding if any):
- Background: `#0f172a` (dark sections) / `#f8fafc` (light sections)
- Surface: `#1e293b` / `#ffffff`
- Primary accent: `#38bdf8`
- Text: `#f1f5f9` / `#0f172a`
- Code highlight: `#1e293b` with `#38bdf8` for keywords

## Typography

- Body: system-ui or a single clean sans-serif (Inter, if available via local font)
- Code: monospace (Fira Code, Cascadia Code, or system monospace fallback)
- Size: 15-16px body, 14px code
- Line height: 1.6 body, 1.5 code

## Module Structure

Each module follows this pattern:
1. **Hook** — one sentence: what problem does this piece of code solve?
2. **Visual** — diagram or animation showing how it fits in the bigger picture
3. **Code** — real snippet from the repo with plain-English translation
4. **Application** — one practical question: "if you wanted to change X, where would you look?"
5. **Quiz** (optional) — one application-focused question with 3-4 options
