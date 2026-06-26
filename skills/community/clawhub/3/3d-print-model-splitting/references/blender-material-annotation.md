# Blender material-face annotation

## Table of contents

1. Why this workflow exists
2. Agent setup
3. Human annotation steps
4. Quality checks
5. What not to do

## 1. Why this workflow exists

Complex sculpted STL files rarely contain semantic part information. A model may visually contain a hat, head, torso, pants, arms, or legs, but the STL is usually just triangles.

The reliable compromise is:

```text
human sees semantic boundaries
agent reads polygon material indices
```

This avoids unreliable automatic cutter guesses while keeping downstream splitting deterministic.

## 2. Agent setup

Prepare a Blender file with:

- the imported source STL;
- one material slot per intended part;
- one unassigned/base material;
- optionally one check/uncertain material;
- a text note inside the `.blend` explaining how to annotate.

Material naming pattern:

```text
BASE_UNASSIGNED
PART_01_<name>
PART_02_<name>
CHECK_UNCERTAIN
```

Use stable prefixes such as `PART_01_` so scripts can preserve part order.

## 3. Human annotation steps

In Blender:

1. Select the source mesh.
2. Press `Tab` for Edit Mode.
3. Press `3` for Face Select.
4. Select triangle faces belonging to a part.
5. In Material Properties, choose the target part material.
6. Click `Assign`.
7. Repeat for all parts.
8. Save the `.blend`.

Useful selection tools:

- `C` Circle Select for painting broad regions;
- `B` Box Select for rectangular areas;
- Shift-click for incremental edits;
- assign uncertain boundary faces to a check material if needed.

## 4. Quality checks

Before running automated splitting:

- every intended part has nonzero face count;
- obvious semantic regions are not left unassigned;
- boundary rings are visually continuous enough to cap;
- uncertain faces have been resolved or intentionally documented;
- tiny accidental islands are expected but should be cleaned conservatively.

## 5. What not to do

- Do not use Texture Paint; it creates image/color data, not reliable per-face part metadata.
- Do not actually cut the model manually unless the workflow explicitly asks for it.
- Do not expect the agent to infer all semantic boundaries from geometry alone.
- Do not mix left/right naming conventions; define whether left/right means character-left or screen-left.
