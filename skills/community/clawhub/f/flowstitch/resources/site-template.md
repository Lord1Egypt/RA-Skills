# Site Template

Use these templates when setting up a new project for the FlowStitch build loop.
Copy and customize for your project — then save to `.stitch/`.

---

## SITE.md Template

Save as: `.stitch/SITE.md`

```markdown
# Project Vision & Constitution

> **AGENT INSTRUCTION:** Read this file before every build loop iteration. It is the project's long-term memory.

## 1. Core Identity
* **Project Name:** [Your project name]
* **Stitch Project ID:** [Your Stitch project ID]
* **Mission:** [What the site achieves in one sentence]
* **Target Audience:** [Who uses this site]
* **Voice:** [Tone and personality — e.g., "Warm, refined, trustworthy"]

## 2. Visual Language
*Reference these descriptors when prompting Stitch — use natural language only, not CSS.*

* **The "Vibe" (Adjectives):**
    * *Primary:* [Main aesthetic keyword — e.g., "Minimal"]
    * *Secondary:* [Supporting aesthetic — e.g., "Sophisticated"]
    * *Tertiary:* [Additional flavor — e.g., "Photography-first"]

* **Color Philosophy (Semantic):**
    * **Background:** [Description] (#hexcode) — [role]
    * **Primary Accent:** [Description] (#hexcode) — [role]
    * **Text Primary:** [Description] (#hexcode) — [role]
    * **Text Secondary:** [Description] (#hexcode) — [role]

## 3. Architecture & File Structure
* **Root:** `site/public/`
* **Asset Flow:** Stitch generates to `.stitch/designs/` → Validate → Move to `site/public/`
* **Navigation Strategy:** [Describe nav structure — e.g., "Global header with 5 links"]

## 4. Live Sitemap (Current State)
*Agent MUST update this section when a page is successfully merged.*

* [x] `index.html` — [Description]
* [ ] `about.html` — [Description]
* [ ] `contact.html` — [Description]

## 5. The Roadmap (Backlog)
*Pick the next task from here when the baton is empty or completed.*

### High Priority
- [ ] [Page/feature description]
- [ ] [Page/feature description]

### Medium Priority
- [ ] [Page/feature description]

## 6. Creative Freedom Guidelines
*When the backlog is empty, follow these guidelines.*

1. **Stay On-Brand:** New pages must fit the established vibe
2. **Enhance the Core:** Support the site mission
3. **Naming Convention:** Lowercase, descriptive filenames

### Ideas to Explore
*Pick one, build it, then REMOVE it from this list.*

- [ ] `[page].html` — [Description]
- [ ] `[page].html` — [Description]

## 7. Rules of Engagement
1. Do NOT recreate pages already marked `[x]` in Section 4
2. ALWAYS update `next-prompt.md` before completing an iteration
3. Consume ideas from Section 6 when you use them
4. Keep the loop moving — leave a valid baton every time
```

---

## DESIGN.md Template

Save as: `.stitch/DESIGN.md`  
Generate automatically using FlowStitch §2 (Design System Synthesis), or fill manually.

```markdown
# Design System: [Project Name]
**Project ID:** [Stitch Project ID]

## 1. Visual Theme & Atmosphere
[Describe mood, density, and aesthetic philosophy in evocative terms.
Example: "A sophisticated minimalist sanctuary with gallery-like spaciousness."]

## 2. Color Palette & Roles
- **[Descriptive Name]** (#hexcode) – [Functional role, e.g., "Primary page background"]
- **[Descriptive Name]** (#hexcode) – [Functional role, e.g., "CTA buttons and links"]
- **[Descriptive Name]** (#hexcode) – [Functional role, e.g., "Headlines and body text"]

## 3. Typography Rules
- **Font Family:** [Name and character, e.g., "Manrope — modern geometric with humanist warmth"]
- **Headlines:** [Weight, size, spacing]
- **Body:** [Weight, line-height, size]
- **Labels/Meta:** [Weight, size]

## 4. Component Stylings
* **Buttons:** [Shape, color, hover behavior]
* **Cards:** [Corner roundness, background, shadow]
* **Inputs:** [Border style, background, focus state]
* **Navigation:** [Style, active state, spacing]

## 5. Layout Principles
[Whitespace strategy, grid columns, max-width, responsive behavior, section margins]

## 6. Design System Notes for Stitch Generation
**Copy this entire block into every baton prompt:**

**DESIGN SYSTEM (REQUIRED):**
- Platform: [Web/Mobile], [Desktop/Mobile]-first
- Theme: [Dark/Light], [descriptors]
- Background: [Descriptive Name] (#hex)
- Primary Accent: [Descriptive Name] (#hex) for [role]
- Text Primary: [Descriptive Name] (#hex)
- Font: [Description]
- Buttons: [Shape description]
- Cards: [Corner and shadow description]
- Layout: [Container and spacing description]
```
