# 3D / AR asset spec (high-visual products)

Goal: “Visually credible + loadable + scalable to variants/configurator.”

## 1) Recommended formats and compatibility

- Web: **GLB** (single file, mesh + materials + texture refs)
- iOS AR: **USDZ** (Quick Look)
- One source → export both GLB and USDZ per SKU to avoid drift.

## 2) Performance budget (starting point; tune by device and page)

- Triangle count: Keep per-product within acceptable range (tier by complexity)
- Textures: Total texture size per product within budget; mobile-first
- Material count: Minimize (faster render and load)
- LOD (optional): At least 2 levels for complex products

> When writing for users, frame as “budget + acceptance criteria” (load time, interaction frame rate, above-the-fold strategy), not raw numbers only.

## 3) PBR materials (recommended)

Per material, aim for:

- Albedo/Base Color
- Normal
- Roughness
- Metallic (0 for non-metals)
- AO (optional)

Furniture notes:

- Wood: Avoid stretched or tiling UVs
- Fabric/leather: Roughness and normal drive perceived quality
- Metal: Keep highlights and reflections restrained to avoid plastic look

## 4) Size accuracy and AR calibration

- Models must be real-world scale (consistent units, e.g. mm)
- AR placement needs a defined floor/contact plane
- For modular sofas/units, define combination rules and collision if using a configurator

## 5) Variants and naming (operable)

Use a consistent naming scheme:

- SKU: `product_id` / `variant_id` / `material` / `color` / `size`
- Files: `<product>_<variant>_<format>.glb` or `.usdz`
- Textures: `<product>_<material>_<map>_<res>.png`

## 6) Default camera and interaction

Define:

- Default view (strong first impression)
- Detail views (texture, edges, craft details)
- AR copy (one line: “what hesitation this solves”)

## 7) Sign-off checklist

- Size within tolerance (define the tolerance)
- Materials look correct (no color shift or plastic look under lighting)
- Loads on mobile (define target threshold)
- Interaction stable (rotate, zoom, reset, AR place)
