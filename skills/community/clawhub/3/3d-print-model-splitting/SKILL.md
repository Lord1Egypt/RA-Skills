---
name: 3d-print-model-splitting
description: Use when splitting a single complex STL / figurine / statue model into multiple 3D-printable and physically assemblable parts, especially with Blender face/material annotation, Bambu Studio, MeshFix, manifold Boolean, interface clearance/allowance, 3MF object validation, or assembly interference checks. Trigger for requests about STL hand-model splitting, Bambu-ready 3MF delivery, print-fit failures, or fixing part interfaces that print but do not assemble.
---

# 3D Print Model Splitting

This skill turns a single complex sculpted STL into multiple Bambu-ready, physically assemblable parts.

## Core rule

Do not confuse printable with assemblable.

Also do not confuse a material-selection preview with a split part.

- MeshFix/slicers can make parts watertight and printable.
- They do not guarantee that interfaces have clearance.
- The validated workflow succeeds because it treats part interfaces as the core problem.
- A face-selection preview is only a semantic preview. It is not a valid part preview until every split part has its open contact boundary capped/filled.

## Mandatory preview gates

For interactive demos or human-guided annotation, proactively generate previews; do not wait for the user to ask.

- After preparing the annotation `.blend`: render a quick source/annotation preview so the user can confirm scale, orientation, and material slots.
- After the user saves material-face annotation: render an annotation preview/contact sheet with clear part colors and face counts.
- Before claiming “拆件完成” / “split complete”: generate a **capped split preview**, not just a face-selection preview.
- In previews, label colors explicitly. If possible, show cap/interface faces in a distinct color.
- If any part is still open at the cut/contact surface, say so clearly and call it “annotation preview only”, not “split preview”.

## Split-surface capping hard rules

Every part created by material splitting must have its cut/contact surfaces filled before baseline export.

- Deleting the other material groups leaves shell openings at the interface. This is expected but not acceptable as a split baseline.
- Cap/fill all boundary loops introduced by the split before exporting baseline STLs.
- Validate capping with boundary-edge counts per part. Target: `boundary_edges = 0` for each baseline part, unless a known intentional opening is documented.
- If automatic hole filling leaves residual boundaries, retry with a more robust method or explicitly report the residual count; do not present it as final.
- Lock the first accepted baseline only after it is “split + capped”; never lock a raw material-isolated shell as baseline.

## Scope boundaries

Good fit:

- figurines, statues, toys, decorative sculpts, and similar triangle-mesh STL files;
- human-guided semantic part boundaries;
- glue-fit or lightly finished assemblies;
- Bambu-ready 3MF/STL handoffs.

Poor fit unless explicitly requested:

- fully automatic semantic recognition;
- precision mechanical snap-fits;
- automatic locator pins/magnets without human-confirmed anchors;
- CAD-grade tolerance guarantees.

## Dependencies

Common tools/libraries:

- Blender for STL import, face/material annotation, rendering, and optional interference checks;
- Python packages as needed by scripts: `trimesh`, `numpy`, `manifold3d`, `pymeshfix`, `Pillow`;
- Bambu Studio or another slicer for final slicing/print review;
- project-local folders for generated STL/3MF/Blend/PNG outputs.

Do not write generated model outputs into the skill directory.

## Progressive references

Read only what the task needs:

- `references/sop.md` — generic workflow from STL to assemblable 3MF.
- `references/clearance-lessons.md` — Boolean/MeshFix/clearance failure modes.
- `references/blender-material-annotation.md` — human Blender annotation instructions.
- `references/versioning.md` — project versioning and status conventions.
- `references/case-study-v13.md` — optional validated example for a 5-part figurine.

## Standard workflow

1. **Prepare annotation file**
   - Create a Blender `.blend` from the input STL.
   - Add material slots for intended parts.
   - Use a project-local output folder.

2. **Human material-face annotation**
   - Human selects triangle faces in Blender Edit Mode.
   - Assign each face to a material slot.
   - Material assignment is geometry metadata (`polygon.material_index`), not texture paint.

3. **Split by material and lock a baseline**
   - Use material indices to export parts.
   - Clean tiny islands, cap open boundaries, export STL, render preview.
   - Lock a baseline that is only “split + capped”, with no clearance/pins/experimental Boolean.
   - Never overwrite the baseline.

4. **Repair only before clearance**
   - Use MeshFix when needed to make baseline parts watertight before clearance.
   - Treat MeshFix as a printability repair, not an assembly solution.

5. **Normalize winding before Boolean**
   - Ensure each STL has outward / positive-volume winding.
   - If volume is negative, invert before expanding cutters.
   - Wrong winding can reverse the clearance direction.

6. **Apply interface clearance**
   - Decide the real remaining assembly interfaces.
   - Define a responsibility table: which part subtracts which expanded neighbor.
   - Use robust manifold Boolean difference for interface allowance.
   - Choose clearance based on printer, scale, material, and finishing expectations.

7. **Do not MeshFix after clearance**
   - After clearance, use only tiny manifold simplify/sliver cleanup.
   - Strong MeshFix can fill intentional clearance cavities and recreate interference.

8. **Validate the deliverable, not only source STL**
   - Export the final 3MF/STL set.
   - Re-read 3MF objects and validate watertight/non-manifold properties.
   - Run pairwise interference checks on adjacent parts.

9. **Slicer and physical test**
   - Use Bambu Studio or another slicer for import/slicing/support/print preview.
   - Do not treat “no overlap warning” as assembly proof.
   - Physical assembly test is the final gate.

## Interface-clearance hard rules

- Start from an un-clearanced baseline when changing the part plan.
- Do not directly merge parts that already had clearance cut between them; this leaves internal cavities/seams.
- Keep clearance work localized to real assembly interfaces.
- If assembly is tight, create a new version and increase clearance locally; do not repair a failed branch blindly.

## Deliverables checklist

For a final handoff, include:

- final Bambu 3MF or slicer-ready project;
- final STL parts;
- preview/contact sheet;
- version note;
- validation summary;
- 3MF object validation report;
- pairwise interference report;
- notes on failed/disallowed routes.

## Script organization

Scripts in `scripts/` are reusable helpers with parameterized paths and part definitions. Keep new scripts project-agnostic: no user-specific absolute paths, no private names, and no hardcoded part schema unless the script clearly accepts a config/CLI override.
