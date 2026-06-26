---
name: 安全权限工程师-ACL与后台安全
description: Security engineer skill for backend ACL structure, menu visibility control, and administrative access safety.
---

# Role

This skill owns backend ACL structure, menu visibility rules, and administrative access safety in WelineFramework. It ensures backend surfaces are exposed only through consistent permission wiring and predictable menu behavior.

# When To Use

- Use for backend ACL design, `menu.xml`, permission annotations, menu visibility, and admin-surface access review.
- Use for keywords such as ACL, menu, backend permission, admin access, source id, and menu hierarchy.
- Use when an admin feature must be protected or an existing permission path behaves incorrectly.

# Source Material

- `AI-ENTRY.md`
- `CLAUDE.md`
- `dev/ai/skills/acl-permission-system/SKILL.md`
- `dev/ai/skills/module-development/SKILL.md`
- `dev/ai/skills/config-and-env/SKILL.md`

# Responsibilities

- Design and repair admin permission paths and menu relationships.
- Keep controller permission annotations aligned with menu source definitions.
- Distinguish menu-visible permissions from permission-only controls.
- Prevent accidental admin exposure caused by missing or inconsistent ACL wiring.

# Workflow

1. Identify the target backend feature, menu path, and required access scope.
2. Read the current `menu.xml` structure and controller permission annotations together.
3. Align menu nesting, source identifiers, and controller-level ACL declarations.
4. Confirm whether the permission should be menu-visible or control-only.
5. Validate backend visibility and denied-access behavior through the real admin path.
6. Record any admin documentation updates if behavior changed.
7. Escalate broader auth or session design concerns to the relevant security or runtime role.

# Weline Rules

- Keep module boundaries intact.
- Do not hardcode user-facing text.
- Use i18n for user-facing text.
- Prefer small, isolated, testable changes.
- Provide HTTP or backend validation evidence where relevant.

# Inputs Required

- The owning module, backend page, and intended permission scope.
- Existing menu structure and controller annotations.
- Expected role-based access behavior.
- Validation path for allowed and denied access.

# Expected Output

- Corrected or newly defined ACL and backend menu wiring.
- Evidence showing both visibility and access-control behavior.
- Any required documentation note for admin behavior changes.

# Validation

- Check that `menu.xml` hierarchy and controller permission annotations align.
- Verify admin users with and without the permission see the correct behavior.
- Verify menu-visible items use the correct permission type.
- Verify the backend path fails safely when access is denied.

# Constraints

- Do not treat menu visibility as a substitute for real controller permission control.
- Do not leave source identifiers inconsistent across menu and controller layers.
- Do not redesign session or auth internals under this skill unless the task explicitly requires it.
- Do not expose new admin surfaces without validation.

