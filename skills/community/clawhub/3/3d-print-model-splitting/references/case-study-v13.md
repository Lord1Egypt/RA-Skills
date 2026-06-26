# Case study: validated 5-part figurine workflow

## Table of contents

1. Why this case matters
2. Failed earlier route
3. Final part plan
4. Interface responsibility table
5. Cleanup and validation
6. Transferable lessons

## 1. Why this case matters

This case closed the loop from a single complex figurine STL to parts that passed:

- geometry validation;
- 3MF object validation;
- pairwise assembly interference checks;
- physical print and assembly testing.

The important lesson is not the specific character or filenames. The transferable lesson is that the final version succeeded because it explicitly solved interface clearance.

## 2. Failed earlier route

An earlier route did this:

```text
split by material
→ cap / close parts
→ MeshFix each part
→ create slicer-ready 3MF
→ print test
```

The print could complete, but the parts could not assemble. This proved:

```text
watertight + printable ≠ assemblable
```

The missing step was real clearance at the part interfaces.

## 3. Final part plan

The final successful version used 5 parts:

```text
01_hat_head       = hat + head
02_body_arms      = body + left arm + right arm
03_pants
04_left_leg
05_right_leg
```

A prior 7-part clearance candidate already had clearance cut between some parts. The 5-part version was **not** made by directly merging that already-clearanced version, because that would leave internal seams/cavities.

Correct approach:

```text
return to un-clearanced baseline
→ rebuild merged parts
→ apply clearance only to remaining real assembly interfaces
```

## 4. Interface responsibility table

The successful responsibility table was:

```text
body_arms subtract expanded hat_head
body_arms subtract expanded pants
pants subtract expanded left_leg
pants subtract expanded right_leg
```

Meaning:

- `body_arms` makes room for `hat_head` and `pants`;
- `pants` makes room for the legs;
- cutters are expanded versions of the neighboring parts;
- expansion depends on correct outward winding.

The target clearance in this case was 0.5 mm.

## 5. Cleanup and validation

Final cleanup used manifold simplify, not MeshFix-after-clearance.

Validation gates:

```text
3MF object validation: PASS
pairwise interference: no meaningful intersections
physical print/assembly: PASS
```

3MF object checks included:

```text
boundary_edges = 0
edges_more_than_2_faces = 0
non_2_face_edges = 0
watertight = true
winding_consistent = true
```

## 6. Transferable lessons

- If the part plan changes, rebuild from baseline before cutting clearance.
- Do not merge parts that have already had clearance cut between them.
- MeshFix is useful before clearance, dangerous after clearance.
- Slicer overlap warnings are not assembly validation.
- The deliverable 3MF must be re-read and validated object by object.
- Physical assembly remains the final acceptance gate.
