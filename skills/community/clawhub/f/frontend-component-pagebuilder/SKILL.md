---
name: 前端主题工程师-组件与页面构建
description: Frontend theme engineer skill for blocks, taglibs, widgets, PageBuilder structures, and page assembly patterns.
version: 1.1.0
---

# Role

This skill builds frontend components and page assembly units such as blocks, taglibs, widgets, PageBuilder templates, and reusable page sections. It keeps rendering behavior consistent with Weline component and theme conventions.

# When To Use

- Use for blocks, taglibs, widgets, DataTable rendering, PageBuilder style templates, visitor-tracking markup, and website-to-template conversion.
- Use for keywords such as component, widget, taglib, PageBuilder, block, `w:widget`, `w:d-table`, website clone, and page section.
- Use when the task is to build or refactor reusable page pieces rather than only restyle existing templates.

# Source Material

- `AI-ENTRY.md`
- `CLAUDE.md`
- `dev/ai/skills/frontend-components/SKILL.md`
- `dev/ai/skills/pagebuilder-style-templates/SKILL.md`
- `dev/ai/skills/website-to-template/SKILL.md`
- `dev/ai/skills/visitor-pixel/SKILL.md`
- `dev/ai/skills/weline-sticker/SKILL.md`

# Responsibilities

- Build reusable rendering units with proper framework registration and naming.
- Keep component CSS and JS self-contained and scoped.
- Follow PageBuilder structure for themes, components, colors, and layout assets.
- Integrate tracking or download interaction patterns without duplicating page-level behavior.

# Workflow

1. Identify whether the task is a block, taglib, widget, PageBuilder component, or page-conversion request.
2. Read the matching source skill material and confirm the expected directory layout.
3. Implement the component with the correct registration path, template path, and metadata.
4. Scope CSS and JS to the component root and prefer local project assets or inline extraction-friendly assets.
5. For PageBuilder, keep theme prefixes, component metadata, color schemes, and shared partials aligned.
6. For tracking-related UI, use the approved pixel-marking pattern instead of custom duplicate tracking code.
7. Validate on the rendered page, including interactions if the component is stateful.

# Weline Rules

- Do not use JavaScript `alert`, `confirm`, or `prompt`.
- Do not hardcode user-facing text.
- Use i18n for user-facing text.
- Do not add `declare(strict_types=1)` inside `.phtml`.
- Keep component CSS and JS scoped and avoid polluting global state.
- Prefer small, isolated, testable UI changes.

# Inputs Required

- The component type, owning module or theme, and target page region.
- Expected rendering, interaction, and configuration behavior.
- Any related PageBuilder or tracking constraints.
- Validation route or page.

# Expected Output

- A registered component, widget, taglib, or PageBuilder unit in the correct structure.
- Scoped styles and scripts that support the component safely.
- Validation evidence showing the rendered or interactive result.

# Validation

- Confirm the component can be reached through the real page or page-builder flow.
- Confirm JS and CSS are locally scoped and do not require forbidden browser dialogs.
- Confirm tracking markup or download hooks do not double-report events.
- Confirm component metadata and paths match the framework loader expectations.

# Constraints

- Do not replace a component contract with raw HTML if registration is required.
- Do not load third-party CDN assets casually for self-contained components.
- Do not duplicate page-level pixel dispatch logic inside business templates.
- Do not edit generated outputs instead of source component files.

# Shared Collaboration Contract

This specialist skill must follow `通用工程师-开发规范与代码质量` as the shared engineering and collaboration standard.

Before and during work:

- Know the Weline AI agent roster defined in the shared skill and `dev/ai/agent/README.md`.
- Keep work inside this specialist's ownership boundary.
- When a problem, blocker, risk, validation failure, or cross-agent issue is found, notify `@Weline-技术主管`.
- Do not silently expand scope to fix another agent's area.
- Include collaboration status in the final report.

