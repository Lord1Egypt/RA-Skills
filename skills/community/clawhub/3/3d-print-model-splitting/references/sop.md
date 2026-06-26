# Generic SOP: complex STL to printable, assemblable parts

## Table of contents

1. Inputs and assumptions
2. Workspace layout
3. Human face/material annotation
4. Split and lock baseline
5. Pre-clearance repair
6. Interface clearance
7. Validation
8. Bambu / slicer handoff
9. Failure handling

## 1. Inputs and assumptions

Use this SOP when the source is a sculpted STL with no useful CAD feature tree, part hierarchy, or semantic labels.

Required human input:

- target part plan;
- approximate visual boundaries between parts;
- acceptance of glue, sanding, or light manual finishing if the object is a figurine rather than a precision mechanism.

Do not promise fully automatic semantic splitting. Complex STL geometry does not know what is a hat, head, sleeve, belt, or hair strand.

## 2. Workspace layout

Use a project-local layout rather than hardcoded machine paths:

```text
<project-root>/
├── source/
│   └── input.stl
├── annotation/
│   └── annotation.blend
├── versions/
│   ├── v01-annotation-test/
│   ├── v02-split-baseline/
│   └── vNN-clearance-.../
└── reports/
```

Keep generated STL/3MF/PNG/Blend files out of the skill directory. The skill directory should contain only reusable instructions and scripts.

## 3. Human face/material annotation

Preferred workflow:

1. Prepare a Blender `.blend` from the source STL.
2. Add one material slot per intended part, plus an unassigned/check material.
3. Human opens Blender, selects triangle faces in Edit Mode, and assigns them to part materials.
4. Save the `.blend`.

Why material assignment:

- it writes per-polygon material indices;
- scripts can read it deterministically;
- boundaries stay on triangle edges;
- it avoids unreliable automatic semantic guessing.

See `blender-material-annotation.md` for detailed human instructions.

Preview gate:

- After creating the annotation file, render a quick preview so the human can check scale/orientation before spending time selecting faces.
- After the human saves annotation, render a material-color preview/contact sheet and report face counts per material.
- Call this an **annotation preview** only. It may still be an open shell after isolation.

## 4. Split and lock baseline

After annotation:

1. Read the marked mesh.
2. Group faces by material.
3. Remove tiny accidental islands conservatively.
4. Cap open boundaries.
5. Export one STL per part.
6. Render a preview/contact sheet.
7. Ask for human review.

Hard requirements for step 4:

- Material-isolated parts are usually open at the contact/cut surface.
- Fill those contact boundaries before baseline export; otherwise the preview will show hollow parts and the STLs are not a valid split baseline.
- Use a distinct cap/interface material in the preview when possible, so the human can verify where the generated contact surfaces are.
- Report per-part `boundary_edges` after capping. Target `0`; if non-zero, document the count and treat the result as needing more repair.

Once accepted, lock this as the **split baseline**:

```text
split + capped + no clearance + no pins + no experimental Boolean
```

Never overwrite the baseline. All later experiments must copy forward into versioned directories.

## 5. Pre-clearance repair

Use repair tools only for the correct purpose.

MeshFix is useful before clearance for:

- watertightness;
- open boundaries;
- non-manifold edges;
- slicer import stability.

MeshFix does not solve assembly clearance.

Hard rule:

```text
MeshFix before clearance: allowed when needed
MeshFix after clearance: avoid / treat as dangerous
```

## 6. Interface clearance

This is the critical step that turns printable parts into assemblable parts.

Procedure:

1. Start from an un-clearanced baseline.
2. If the part plan changes, rebuild merged parts from baseline; do not merge already-clearanced parts.
3. Normalize each STL to outward / positive-volume winding.
4. Define the real assembly interfaces.
5. Write a responsibility table: which part subtracts which neighbor.
6. Expand the neighbor cutter outward by the requested clearance.
7. Use robust manifold Boolean difference.
8. After Boolean, only use tiny simplify/sliver cleanup.

Example responsibility table shape:

```text
receiver_part subtract expanded neighbor_part
part_a subtract expanded part_b
part_c subtract expanded part_d
```

The receiver is the part that should make room for the neighbor.

Typical figurine clearance starts around 0.5 mm, but choose tolerance based on printer, material, scale, and finishing expectations.

## 7. Validation

Validate the actual deliverable, not just intermediate STL files.

For every final 3MF object, check:

```text
watertight = true
boundary_edges = 0
edges_more_than_2_faces = 0
non_2_face_edges = 0
winding_consistent = true
```

Then check pairwise intersections on real neighboring interfaces. Tiny coplanar/numerical residue can be acceptable; meaningful volume intersection is not.

Recommended reports:

```text
validate_3mf_objects.json
pairwise_interference.json
assembly_interference_report.txt
```

## 8. Bambu / slicer handoff

Use Bambu Studio or another slicer for:

- object import review;
- orientation;
- support;
- slicing preview;
- printer/profile-specific decisions.

Do not use the slicer as the only assembly verifier. “No overlap warning” is not proof that physical parts will fit.

## 9. Failure handling

If the print succeeds but parts cannot assemble:

1. Mark the version as failed-print.
2. Do not keep repairing that branch blindly.
3. Return to the last clean baseline or the last validated pre-clearance stage.
4. Increase clearance locally or revise the responsibility table.
5. Re-run 3MF object and pairwise interference validation.

If a merged part contains internal seams/cavities, it was probably merged after clearance had already been cut. Rebuild from the un-clearanced baseline.
