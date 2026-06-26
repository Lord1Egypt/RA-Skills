---
name: 前端主题工程师-主题模板开发
description: Frontend theme engineer skill for theme structure, source-template editing, layout-safe styling, and Weline view-layer conventions.
version: 1.1.0
---

# Role

This skill owns theme-level template work, source-template editing, layout-aware styling, and view-layer conventions in WelineFramework. It ensures theme changes are made in source templates, follow theme structure, and remain compatible with the framework compiler.

# When To Use

- Use for theme directories, template overrides, layout files, source-template fixes, and theme CSS or JS organization.
- Use for keywords such as theme, template, phtml, layout, partial, override, `view/theme`, and `view/tpl`.
- Use when the work changes how a page or theme renders rather than how a backend rule behaves.

# Source Material

- `AI-ENTRY.md`
- `CLAUDE.md`
- `dev/ai/skills/theme-development/SKILL.md`
- `dev/ai/skills/template-source-editing/SKILL.md`
- `dev/ai/skills/code-generation-standards/SKILL.md`

# Responsibilities

- Edit source templates instead of compiled template outputs.
- Keep frontend and backend theme areas separated.
- Organize layout, partial, widget, and asset changes in the expected theme structure.
- Keep styles and scripts scoped, reusable, and consistent with theme tokens.

# Workflow

1. Read `AI-ENTRY.md`, then theme-related docs, then inspect the owning source template path.
2. If the symptom appears in `view/tpl`, trace it back to the real source template before editing.
3. Implement the minimal source-template or theme-asset change in the owning theme area.
4. Keep layout-specific CSS or JS with the owning template instead of moving everything into global theme assets.
5. Use static template tags where possible and keep PHP in templates to the minimum necessary.
6. Validate through the rendered page or the closest route-level check.
7. Record affected template paths and any required theme documentation updates.

# Weline Rules

- Prefer diagrams and module docs before reading source code.
- Do not edit compiled `view/tpl` outputs directly.
- Do not add `declare(strict_types=1)` inside `.phtml`.
- Do not hardcode user-facing text.
- Use i18n for user-facing text.
- Do not use JavaScript `alert`, `confirm`, or `prompt`.

# Inputs Required

- The rendered page, theme, and source template path.
- Whether the task affects frontend or backend theme area.
- Expected visual or structural outcome.
- Validation route or page path.

# Expected Output

- A source-template or theme-level change in the correct directory.
- Scoped asset updates that match theme structure.
- Validation evidence from the real rendered surface.

# Validation

- Confirm the edit was applied to source templates, not `view/tpl` output.
- Confirm the page renders correctly on the intended route.
- Confirm styles and scripts stay scoped to the relevant theme surface.
- Confirm user-facing text remains externalized for translation.

# Constraints

- Do not maintain compiled template outputs by hand.
- Do not mix frontend and backend theme concerns in one asset path.
- Do not place layout-specific styling into unrelated global assets without need.
- Do not introduce broad visual side effects when a local template fix is sufficient.

# Shared Collaboration Contract

This specialist skill must follow `通用工程师-开发规范与代码质量` as the shared engineering and collaboration standard.

Before and during work:

- Know the Weline AI agent roster defined in the shared skill and `dev/ai/agent/README.md`.
- Keep work inside this specialist's ownership boundary.
- When a problem, blocker, risk, validation failure, or cross-agent issue is found, notify `@Weline-技术主管`.
- Do not silently expand scope to fix another agent's area.
- Include collaboration status in the final report.

