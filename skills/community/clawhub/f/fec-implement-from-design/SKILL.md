---
name: fec-implement-from-design
description: Use when implementing UI from Figma, Sketch, MasterGo, Pixso, Modao, MockingBot, screenshots, design selections, design tokens, or design-to-code tasks for production frontend components/pages; Chinese triggers include design draft, implementation by design.
---

# Implement according to design draft

## Purpose

Based on the design context of design tools (Figma, Sketch, MasterGo, Pixso, Mokou, Mock), high-fidelity implementation of pages or components emphasizes component reuse, design token mapping, accessibility, and production-oriented front-end implementation.

## Supported design tools

| Tools | MCP Integration | How to obtain design data |
| -------- | ------------------------- | ----------------------------------------- |
| Figma | `figma` / `figma-desktop` | API to obtain design structure and variable definitions |
| Sketch | `sketch` | MCP Get screenshot of design selection |
| MasterGo | `mastergo` | API to get DSL structure data |
| Pixso | `pixso` | Local MCP gets frame data and code |
| Mo Dao | `modao` | MCP obtains prototype data and generates design descriptions |
| Mocke | No MCP | Acquired via user-provided screenshots, annotations, or exported CSS |

## Target

- Realize the design draft as accurately as possible
- Prioritize reusing existing project components before creating new ones
- Map design variables to existing Tokens as much as possible
- Keep implementations maintainable, well-typed, testable, and accessible
- Avoid introducing duplication of basic components or parallel design systems

## Procedure

### 1. Identify design sources

Select the design data acquisition method according to priority:

- `figma` — Figma API integration
- `figma-desktop` — Figma desktop integration
- `mastergo` — MasterGo DSL data
- `pixso` — Pixso local MCP
- `modao` — Ink knife prototype data
- `sketch` — Sketch selection screenshot
- If none of the above MCPs are available, ask the user to provide design screenshots or annotations (applicable to tools without MCP such as Mocke)
- If there is no authoritative design draft, but the task clearly requires a visual website, brand page, portfolio or high-aesthetic redesign, user-provided or locally generated section-level reference images can be used as a temporary source of visual truth; this source must be analyzed first and then implemented, and marked in the plan as not an authoritative design system.

### 2. Read the design context

Read the design context from the MCP or user-supplied design data:

- Check layout structure
- Check spacing, fonts, colors, variables, states, icons and component hierarchy
- If MCP provides resource files or SVG/image sources, use them directly
- If MCP has provided real resources, do not create placeholder resources by yourself
- If the user provides screenshots instead of MCP data, infer visual information such as layout, color, font, etc. from the screenshots
- If using images/screenshots for reference, first extract block structure, visual hierarchy, main and functional colors, font temperament, spacing rhythm, media position, interaction status hints and responsive risks before writing code.
- Prioritize the use of clear section-level reference images or local detail images for multi-section pages; do not guess buttons, font sizes, spacing and component status from compressed long images.
- Unreadable text, fake screenshots, uninspectable materials or conflict status in visual references cannot be copied directly; they need to be translated into the real content, real status or clear placeholder description of the project.

### 3. Search for reusable components

Before creating a new component, search the code base for reusable components, focusing on:

- Button
- Input / Select / Checkbox / Radio / Switch
- Modal / Drawer / Dialog
- Table / List / Card
- Tabs / Breadcrumb / Pagination
- Page Container/Block Container/Empty State/Loading State

### 4. Output realization plan

Before revising the document, produce a short implementation plan. The plan must include:

- List of files that need to be changed
- Component splitting plan
- Status/data flow
- Responsive behavior
- The decision to reuse or create a new one
- Design gaps or points of ambiguity
- The authenticity of the source of the image/screenshot, and what visual details are covered by project tokens, component conventions, or accessibility requirements

### 5. Implementation by framework

Implement according to the front-end framework currently used by the warehouse:

- Strictly follow the existing agreements in the warehouse
- Prefer explicitly typed props and interfaces/types
- Keep components small and composable
- Extract duplicate logic into hooks/composables/utilities

### 6. Design Token Mapping

- Prefer using existing design tokens, CSS variables, theme variables or tool classes
- Do not hardcode colors, rounded corners and spacing unless there is no corresponding token
- If the design uses a new Token, make it clear and don’t quietly hardcode it everywhere

### 7. Accessibility guarantee

- Prioritize the use of semantic HTML
- Make sure interactive controls have accessible names
- Preserve visible focus styles
- Check the keyboard operability of dialog boxes, menus, tabs, and form controls

### 8. Verify after encoding

- If there is lint, execute lint
- If there are tests, execute them
- If testing is missing, indicate the recommended minimum testing range

## Detailed reference

When writing the implementation plan report, load [references/design-plan-template.md](references/design-plan-template.md).

## Constraints

- If you already have a design context (MCP or screenshots), don’t rely on guesswork to implement the UI
- If the project already has a UI system, do not introduce a new UI Kit
- Do not replace tokenized styles with hard-coding unless there is a valid reason
- Don't ignore statuses such as hover, active, disabled, loading, empty, error, etc.
- In scenarios where MCP tools are not available, such as Mocke, proactively ask users for key screenshots and annotation information, and do not make up visual data out of thin air.
- Do not treat the generated image as a directly reproducible code specification; it only provides visual evidence, and the final implementation must obey the current project components, tokens, accessibility and performance boundaries
- Do not replace section analysis with an unreadable full-page image; key sections, CTAs, forms, navigation and status must be inspectable

## Expected Output

- The design implementation plan report is saved as `reports/design-plan-YYYY-MM-DD-HHmmss.md`, including implementation summary, component splitting plan, status/data flow, and change file list
- The code realizes high-fidelity restoration of the design draft, maximizing component reuse rate
- Design variables map to existing Tokens, no hard-coded colors/spacing/rounded corners
- Interactive elements have accessible names and keyboard support, and focus styles are visible
