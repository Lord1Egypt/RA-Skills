# Aspect-Ratio Adaptation and Square Icon Conversion

Read this reference only when the user explicitly requests an output aspect ratio different from the supplied reference.

When active, these rules override crop and placement preservation only where necessary to fit the target ratio; identity anchors and primary-subject proportions remain invariant.

## Non-negotiable invariants

- Treat the primary semantic system and its connected structural parts as one proportional group.
- Apply uniform scaling to that group; never stretch, squash, shear, or independently resize it.
- Preserve identity anchors, relative scale, overlap, orientation, depth order, and distinctive negative space.
- Do not crop away a critical identity anchor. Cropping is allowed only when the primary system and its identity remain intact.
- Do not enlarge a subordinate object merely to fill newly available space.

## Recomposition strategy

After fitting the primary system inside the target safe area, adapt the rest of the composition in this order:

1. Extend or contract surrounding background planes and negative space.
2. Reposition subordinate systems without changing their scale where possible.
3. Delete, group, or demote low-value secondary details.
4. Simplify internal marks when the target format must remain readable at small size.
5. Fill the full canvas with existing HSB palette roles or newly extended palette flat planes.

Prefer recomposition over non-uniform deformation. Do not invent photographic detail or unsupported objects to fill empty space. Do not add letterbox or pillarbox bars unless explicitly requested.

## Landscape-to-square conversion

For a landscape reference converted to a 1:1 square icon:

- keep the wide primary silhouette proportionally intact;
- fit the primary system inside a square safe area with clear edge margins;
- use expanded sky, ground, water, wall, or other environmental planes to occupy additional vertical space;
- preserve foreground, midground, and background ordering;
- reposition small supporting elements only when needed to avoid edge loss or focal competition;
- keep the primary system dominant and do not let repositioned supports become equal focal centers;
- use solid flat fields for all extensions; do not stretch texture, lighting, blur, or photographic detail.

## Validation

Treat any failure below as a Visual Validation Checklist failure and follow the Generation Call Protocol in `../SKILL.md`. Fail if:

- the primary subject is visibly stretched, squeezed, or sheared;
- connected parts no longer share the original proportions;
- a critical identity anchor is cropped or displaced;
- new background space introduces unsupported objects or texture;
- secondary elements become larger or more salient than the primary system;
- the square composition is not legible at small size;
- the full canvas is not filled by crisp flat shapes.
