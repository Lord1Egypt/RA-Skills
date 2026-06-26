# Clearance and Boolean lessons

## Table of contents

1. Slicer Boolean is not assembly validation
2. MeshFix timing
3. Winding and volume sign
4. Manifold Boolean workflow
5. Changing part plans
6. Version hygiene

## 1. Slicer Boolean is not assembly validation

Complex sculpted STL geometry often contains:

- coplanar triangles;
- tiny slivers;
- self-touching regions;
- near-zero-area faces;
- dense triangle soup with no CAD intent.

Blender or slicer Boolean tools may fail, silently alter geometry, or report no overlap while physical parts still collide. Use slicers for slicing decisions, not as the sole source of truth for assembly clearance.

## 2. MeshFix timing

MeshFix is excellent for printability repair:

- closing boundaries;
- resolving non-manifold edges;
- producing watertight meshes.

But MeshFix does not know which cavities are intentional assembly clearance.

Dangerous sequence:

```text
cut clearance cavity
→ run strong MeshFix
→ MeshFix fills cavity
→ part prints but no longer fits
```

Safe default:

```text
MeshFix before clearance: allowed when needed
MeshFix after clearance: avoid; use tiny simplify/sliver cleanup instead
```

## 3. Winding and volume sign

A watertight STL can still have negative volume because its normals are inverted.

If cutter expansion uses vertex normals and the mesh is inverted, expansion can go inward, reversing the intended clearance.

Before Boolean:

1. load STL;
2. remove unreferenced vertices;
3. if `mesh.volume < 0`, invert;
4. only then expand cutter normals.

## 4. Manifold Boolean workflow

Reliable clearance workflow:

```text
clean un-clearanced baseline
→ optional pre-clearance MeshFix
→ normalize outward winding
→ expand neighbor cutter by clearance distance
→ manifold Boolean difference
→ manifold simplify with tiny tolerance
→ 3MF object validation
→ pairwise interference validation
```

The simplify tolerance must be much smaller than the intended clearance. For example, if clearance is 0.5 mm, a 0.001 mm cleanup is numerical cleanup, not geometry redesign.

## 5. Changing part plans

If the part plan changes, do not merge parts that already had clearance cut between them.

Bad:

```text
7-part clearance version
→ directly merge two already-clearanced neighboring parts
→ internal seam/cavity remains
```

Good:

```text
un-clearanced baseline
→ rebuild merged parts
→ cut clearance only at remaining external assembly interfaces
```

## 6. Version hygiene

Keep failed and successful branches understandable:

- mark “printed but did not assemble” as `failed-print`;
- do not keep patching a failed branch blindly;
- return to the last clean baseline when interface logic is wrong;
- retain reports for traceability, but make final deliverables obvious;
- final acceptance requires physical assembly, not just watertight STL.
