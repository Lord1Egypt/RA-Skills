# Blender 4.x to 5.x Compatibility Notes

## Sources

- Blender 4.0 Python API release notes: https://developer.blender.org/docs/release_notes/4.0/python_api/
- Blender 5.0 Python API release notes: https://developer.blender.org/docs/release_notes/5.0/python_api/
- Blender 4.0 API change log: https://docs.blender.org/api/4.0/change_log.html
- Blender 5.0 API change log: https://docs.blender.org/api/5.0/change_log.html

## High-Impact Blender 4.0 Changes

- Replace operator context override arguments with `context.temp_override(...)`.
- Migrate asset APIs:
  - `context.asset_file_handle` -> `context.asset`
  - `context.selected_asset_files` -> `context.selected_assets`
  - `AssetHandle` usage -> `AssetRepresentation`
- Update node-group construction from `NodeTree.inputs/outputs` to `NodeTree.interface`.
- Remove calls to deprecated APIs such as:
  - `Mesh.calc_normals`
  - `bpy.app.version_char`
  - `blf.size(..., dpi=...)`
- Expect mesh custom-data migration to generic attributes (for example, bevel/crease attributes).

## High-Impact Blender 5.0 Changes

- Stop using dict-like access for runtime-defined `bpy.props` data storage.
- Use `options={"READ_ONLY"}` for read-only properties and new `get_transform` / `set_transform` callbacks when transforming values with default storage.
- Do not import bundled modules that became private (for example, `bl_ui_utils`, `rna_info`, `bl_console_utils`).
- Remove legacy GPU paths:
  - Deprecated `bgl` API is removed.
  - `Image.bindcode` is removed; use `gpu.texture.from_image(image)`.
  - Legacy shader-from-GLSL-file flow is removed.
- Update render assumptions:
  - EEVEE identifier is `BLENDER_EEVEE` (not `BLENDER_EEVEE_NEXT`).
- Update asset UI logic:
  - `context.active_file` is unavailable in asset shelf context.
  - `UILayout.template_asset_view()` is removed in favor of asset shelf patterns.
- Update compositor assumptions:
  - `scene.use_nodes` is deprecated (scheduled for removal in 6.0).
  - `scene.node_tree` is removed; use `scene.compositing_node_group`.

## Cross-Version Coding Patterns

1. Centralize compatibility shims.
2. Prefer feature detection with `hasattr(...)` where practical.
3. Add explicit `bpy.app.version` guards for hard API breaks.
4. Keep UI and operator logic separate from compatibility logic.
5. Avoid private or undocumented modules.
6. Review version-specific `change_log.html` before finalizing generated scripts.

## Pre-Delivery Checklist

1. Verify no removed symbols are used.
2. Verify add-on registration/unregistration works.
3. Verify operator `bl_idname` values are valid.
4. Verify all context-sensitive operations use safe context handling.
5. Verify compatibility wrappers are used instead of ad-hoc checks.
