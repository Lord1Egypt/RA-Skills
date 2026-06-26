# Blender Plugin Development Skill

A Codex skill for Blender add-on development and `bpy` script generation with Blender 4.x and 5.x compatibility.

## What This Skill Includes

- `SKILL.md`: Workflow and operating rules for add-on/script tasks.
- `scripts/scaffold_addon.py`: Generator for a Blender add-on package skeleton.
- `references/blender4_to_5_compat.md`: Key API migration notes from Blender 4.0 to 5.0.
- `references/script_generation_patterns.md`: Reusable operator/panel/registration templates.

## Compatibility Focus

This skill is designed for:

- Blender 4.x add-ons and scripts
- Blender 5.x API changes and migration safety

It explicitly covers breaking changes and deprecations documented in official Blender API and release notes.

## Quick Start

1. Generate a new add-on scaffold:

```bash
python3 scripts/scaffold_addon.py --name "My Addon" --output .
```

2. Optional scaffold arguments:

```bash
python3 scripts/scaffold_addon.py \
  --name "My Addon" \
  --module my_addon \
  --author "Your Name" \
  --version 0.1.0 \
  --blender-min 4.0.0 \
  --output .
```

3. Use the generated files (`__init__.py`, `compat.py`, `operators.py`, `ui.py`) as the baseline for feature implementation.

## Validation

- Validate Python syntax:

```bash
python3 -m py_compile scripts/scaffold_addon.py
```

- Validate skill structure:

```bash
python3 /home/zwhy/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
```

## Sources

- Blender 4.0 Python API release notes: https://developer.blender.org/docs/release_notes/4.0/python_api/
- Blender 5.0 Python API release notes: https://developer.blender.org/docs/release_notes/5.0/python_api/
- Blender 4.0 API changelog: https://docs.blender.org/api/4.0/change_log.html
- Blender 5.0 API changelog: https://docs.blender.org/api/5.0/change_log.html
