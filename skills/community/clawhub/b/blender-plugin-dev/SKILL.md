---
name: blender-plugin-development
description: Develop, debug, and upgrade Blender add-ons/plugins and `bpy` scripts with Blender 4.x and 5.x compatibility. Use when tasks involve generating new add-on code, scaffolding operators/panels, migrating deprecated Python API calls, resolving Blender version breakages, or validating scripts against Blender 4/5 API changes.
---

# Blender Plugin Development

## Quick Start

1. Confirm target Blender versions (minimum and maximum expected).
2. Read `references/blender4_to_5_compat.md` before writing or patching code.
3. Scaffold a new add-on package with `scripts/scaffold_addon.py` when requested.
4. Implement requested behavior with explicit compatibility guards for 4.x and 5.x.
5. Validate syntax and registration flow before returning code.

## Workflow

### 1) Scope the task

- Extract target behavior, UI location, operator names, and data model.
- Ask for Blender version range if unspecified; default to `>= 4.0` with 5.x awareness.
- Decide whether output should be:
  - A full add-on package.
  - A standalone `bpy` script.
  - A migration patch to existing code.

### 2) Generate a baseline when creating a new add-on

- Run:
  - `python3 scripts/scaffold_addon.py --name "<Addon Name>" --output <target-dir>`
- Customize generated `__init__.py`, `operators.py`, `ui.py`, and `compat.py` for the feature request.
- Keep `bl_info["blender"]` at the minimum supported version (for this skill, usually `(4, 0, 0)` or higher).

### 3) Implement compatibility-safe code

- Use `bpy.app.version` gates only when behavior truly diverges.
- Prefer compatibility wrappers in `compat.py` over scattered version checks.
- Avoid APIs called out as removed/deprecated in `references/blender4_to_5_compat.md`.
- For operator context overrides, use `context.temp_override(...)`.
- For assets, prefer `context.asset` and `AssetRepresentation`.
- For GPU drawing in 5.x, avoid `bgl` and migrate to `gpu`.

### 4) Validate before returning code

- Run `python3 -m py_compile` on changed Python files.
- If Blender binaries are available, run headless smoke tests:
  - `blender --background --factory-startup --python <smoke_test.py>`
- Check register/unregister order and operator `bl_idname` format.
- Confirm no removed API names remain in generated output.

## Script Generation Patterns

- Generate small, composable files:
  - `operators.py` for operators.
  - `ui.py` for panels/menus.
  - `compat.py` for version shims.
  - `__init__.py` for `bl_info` and registration entrypoints.
- Use idempotent register/unregister functions.
- Keep class lists explicit (tuple of classes) and unregister in reverse order.
- Report actionable failures with `self.report({"ERROR"}, "...")` inside operators.
- Avoid hard-coded context assumptions in `poll()` and `execute()`.

## Required Compatibility Rules

- Avoid dict-like access for runtime-defined RNA properties in 5.0 when accessing add-on-defined data; use supported property access patterns documented in Blender 5.0 release notes.
- Never depend on bundled private modules listed in Blender 5.0 notes (for example, `bl_ui_utils`, `rna_info`).
- Treat `scene.use_nodes` as deprecated and avoid using it for new code.
- Avoid `UILayout.template_asset_view()` in new code; use asset-shelf-compatible APIs.
- Keep code ready for Blender 6.0 removals by addressing documented 5.0 deprecations proactively.

## Resources (optional)

### scripts/
- `scripts/scaffold_addon.py`: Generate a Blender 4/5-ready add-on package skeleton.

### references/
- `references/blender4_to_5_compat.md`: Blender 4.0 and 5.0 compatibility map with official sources.
- `references/script_generation_patterns.md`: Reusable patterns for operators, panels, and background scripts.
