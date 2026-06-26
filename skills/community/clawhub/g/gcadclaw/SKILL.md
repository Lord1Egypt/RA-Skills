---
name: gcadclaw
version: 1.0.0
description: 通过 pygcadwin 实现 GstarCAD 二维图纸的自然语言生成、修改、校验与修复。支持机械零件、装配体、工程图纸的 DWG 自动化输出，包含截图反馈和实体验证。
author: haochen-gcad
license: MIT
tags: [cad, gstarcad, dwg, mechanical, engineering, drawing, automation, pygcadwin, 2d]
tools: [python, exec, filesystem]
platforms: [windows]
metadata: {
  "openclaw": {
    "os": ["win32"],
    "requires": {
      "bins": ["python"],
      "anyBins": []
    }
  }
}
---

# GcadClaw

> **Note on naming.** `gcadclaw` is the *external*, marketplace-style skill
> bundle (Windows setup-wizard payload, `agents/openai.yaml` persona) and is
> configured to install `pygcadwin` directly from PyPI. It is distinct from the in-app
> `cadclaw` agent in `data/graphs/agents_config.json`, which is an `llm_tool`
> agent driven by the `gcad-coder-general` and `gcad-design2d-general` skills. Both can coexist.

## Purpose

Create or modify 2D GstarCAD drawings from natural-language requirements using the `pygcadwin` PyPI package, then prove the result with structured feedback artifacts.

## Defaults

Use these defaults unless the user specifies otherwise. Do not ask for clarification just because the user omitted units, "2D", output format, base plane, origin, or common drafting conventions.

- Task type: a 2D GstarCAD DWG drawing generated through `pygcadwin`.
- Units: millimeters.
- CAD target: live GstarCAD through `pygcadwin.Gcad`.
- Output: `.dwg` plus feedback artifacts.
- Base drawing plane: XY model space unless the user requests paper-space layout.
- Up/elevation axis: positive Z for side, front, section, and elevation references.
- Origin: center of the main part or assembly unless a mating interface, pivot, fixed root component, or datum feature suggests a better origin.
- View selection: for ordinary part designs, default to a standard three-view orthographic drawing: top/plan, front/elevation, and right-side view. Replace one side view with a section/detail view only when it communicates the design better. For assemblies, include the top/plan arrangement plus front/side/section views needed to show stack-up, pivots, travel, or mating relationships.
- Geometry representation: closed 2D outlines for visible profiles; centerlines for axes, bolt circles, symmetry, and rotation; hidden/dashed lines only when useful; hatches for cut material in sections.
- Layers: create named layers for outline/body, cut/hole, centerline, hidden, dimensions, text/notes, construction, and optional part-specific layers.
- Dimensions and notes: include critical overall sizes, hole diameters, spacing, bolt circles, thickness/height notes, fillet/chamfer notes, view labels, section/detail labels, part labels, and assumptions.
- Assembly structure: fixed root part or datum, named part outlines/layers, explicit generated placements, pivot axes, mating holes, travel arcs, and labels for separate moving parts.
- Small plastic enclosure wall: 2.0-3.0 mm when unspecified.
- Cosmetic fillet: 1.0-3.0 mm when safe for local geometry.
- M3/M4/M5 normal clearance holes: 3.4/4.5/5.5 mm unless another standard is requested.
- Feedback: mandatory before/after entity evidence plus at least one PNG screenshot.

Ask one focused clarification only when the drawing is impossible, fit-critical, safety-critical, compliance-bound, or lacks any usable dimensions. Otherwise proceed with explicit assumptions and record them in the brief.

## Required Workflow

1. **Write a brief.** Record intent, dimensions, units, assumptions, layers, expected entities, annotations/dimensions, output paths, and validation targets in `brief.md`.
2. **Capture before state.** Use `scripts/capture_feedback.py` or equivalent `pygcadwin` enumeration to write `before_entities.json`.
3. **Plan actions.** Prefer a Python script or `pygcadwin.run_actions()` sequence that uses typed APIs: `ensure_layer`, `create_segment`, `create_circle`, `create_arc`, `create_polyline`, `create_rect`, `create_text`, `create_dimension`, `create_hatch`, `create_table`, `zoom_extents`, `save_as`, and `snapshot`.
4. **Execute drawing edits.** Use `pygcadwin.Gcad(create_if_missing=True, visible=True)` and `cad.context`; keep calculations explicit and named before creating geometry.
5. **Capture after state.** Write `after_entities.json` and compare entity counts, layers, object names, handles, colors, linetypes, and lineweights against the brief.
6. **Capture screenshot.** Call `ctx.zoom_extents()` or a scoped view operation, then `ctx.view.snapshot().save(<png>)` or the `snapshot` tool. Verify that the PNG is nonblank. Do not mark a drawing-modifying task complete without a nonblank PNG screenshot.
7. **Repair if needed.** If validation or screenshot capture fails, classify the issue, make the smallest responsible change, rerun the failed check, and update feedback.
8. **Report final feedback.** Write `feedback.md` or `feedback.json` with files, checks run, screenshot path, repair attempts, assumptions, and remaining caveats.

## Non-Negotiables

- Do not claim success from code generation alone.
- Do not skip screenshots for drawing-modifying tasks.
- Do not accept all-black/all-white screenshots as successful evidence.
- Do not use raw CAD commands when a typed `pygcadwin` API exists.
- Do not invent unavailable `pygcadwin` API names; inspect the installed package or PyPI project docs when uncertain.
- Do not report validation that was not actually run.

## Feedback Artifacts

Every completed drawing workflow must persist:

- `brief.md`
- `actions.jsonl`
- `before_entities.json`
- `after_entities.json`
- `review.png` or a more specific PNG screenshot name
- `feedback.md` or `feedback.json`
- final `.dwg` path when save succeeds

Read `references/feedback-loop.md` before implementing or repairing a feedback-producing workflow. Read `references/2d-pygcadwin-workflow.md` when translating prose into `pygcadwin` drawing code.

## External Prerequisites

Live drawing, DWG save, and screenshot workflows require Windows with GstarCAD installed and registered as a COM server. Install `pygcadwin` from PyPI with `python scripts/setup_python_env.py`; the PyPI package declares its Windows automation dependencies.

## Repair Loop

When a check fails:

1. Read the failing output or screenshot capture error.
2. Classify it as source error, COM connection error, missing geometry, wrong layer/style, wrong scale, missing dimension/annotation, screenshot failure, or save failure.
3. Change the smallest responsible source/action.
4. Rerun the failed command and dependent validation.
5. Update `feedback.md` with the failed attempt and final state.

If screenshot capture fails after one repair attempt, report partial completion and keep entity evidence, action logs, and DWG output available. Do not call the workflow fully successful.

<!-- BEGIN AUTO-GENERATED PYTHON PACKAGE SETUP -->

## Python package setup

This Skill installs `pygcadwin` directly from PyPI:

```text
https://pypi.org/project/pygcadwin/
```

When this Skill is used in a fresh Python environment:

1. Validate the import:

   ```bash
   python scripts/validate_env.py
   ```

2. If validation fails, install the PyPI package:

   ```bash
   python scripts/setup_python_env.py
   ```

3. Validate again:

   ```bash
   python scripts/validate_env.py
   ```

The expected import is `pygcadwin`. The skill does not bundle a local wheel for this package.

<!-- END AUTO-GENERATED PYTHON PACKAGE SETUP -->
