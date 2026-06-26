# Versioning convention for STL splitting projects

## Table of contents

1. Directory shape
2. Version naming
3. Status values
4. Required version notes
5. Baseline and rollback rules

## 1. Directory shape

Use a project-local `versions/` folder:

```text
<project-root>/versions/
├── v01-annotation-test/
├── v02-split-baseline/
├── v03-meshfix-print-test/
├── v04-clearance-0p5/
└── v05-final-candidate/
```

Do not write generated models into the skill package. Keep all model outputs in the current project folder.

## 2. Version naming

Use:

```text
vNN-short-name
```

Rules:

- `vNN` is two digits and strictly increasing.
- `short-name` is 2–4 lowercase words.
- Put details in `VERSION.md`, not in the directory name.
- Do not rename failed versions; mark their status and reason.

Examples:

```text
v02-split-baseline
v03-meshfix-print-test
v04-clearance-0p5
v05-5part-clearance
```

## 3. Status values

Recommended statuses:

```text
planned          planned but not generated
running          currently being generated
review           waiting for human/slicer/print review
baseline         clean rollback point; do not overwrite
passed-geometry  watertight/non-manifold/interference checks pass
print-candidate  ready for slicer/print test
final-pass       physical print/assembly passed
failed           failed before printing
failed-print     printed but physical result failed
archived         kept for history only
```

## 4. Required version notes

Each version should include `VERSION.md`:

```markdown
# vNN-short-name

## Status
status-value

## Goal
What this version is testing.

## Input
Which baseline/version/files it came from.

## Operations
- split/cap?
- MeshFix before clearance?
- union/merge?
- clearance responsibility table?
- cleanup method?
- 3MF export?

## Outputs
Main STL/3MF/preview/report paths.

## Validation
- STL checks
- 3MF object checks
- pairwise interference checks
- slicer review
- physical print result

## Result
Decision and why.

## Rollback
Where to return if this fails.
```

## 5. Baseline and rollback rules

- A baseline is a clean rollback point, not an active experiment folder.
- Never overwrite a human-approved baseline.
- If a print is physically unassemblable, mark it `failed-print` and return to the last clean pre-clearance version.
- If changing the part plan, rebuild from an un-clearanced baseline instead of merging already-clearanced parts.
