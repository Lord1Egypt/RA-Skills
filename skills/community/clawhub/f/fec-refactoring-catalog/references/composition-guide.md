# Refactoring Composition Guide

Relationships here are conditional. Apply an edge only when its enabling condition exists and verify every intermediate state.

## Inverse / Trade-off Pairs
- `RF-EXTRACT-FUNCTION` ↔ `RF-INLINE-FUNCTION`: introduce a meaningful boundary or remove an indirection that no longer pays for itself.
- `RF-EXTRACT-VARIABLE` ↔ `RF-INLINE-VARIABLE`: name an important expression or remove a name that obscures rather than clarifies.
- `RF-PULL-UP-METHOD` ↔ `RF-PUSH-DOWN-METHOD`: move behavior toward the level where it is truly shared or specialized.
- `RF-PULL-UP-FIELD` ↔ `RF-PUSH-DOWN-FIELD`: place data at the narrowest hierarchy level that accurately owns it.
- `RF-HIDE-DELEGATE` ↔ `RF-REMOVE-MIDDLE-MAN`: trade client coupling against excessive pass-through indirection.

## Common Conditional Sequences
### Extraction enables ownership movement
`RF-EXTRACT-FUNCTION` → `RF-MOVE-FUNCTION`

Use when only part of a larger function is dominated by another module’s data. Extract a coherent unit first, then move that unit to the better owner.

### Query extraction enables function extraction
`RF-REPLACE-TEMP-WITH-QUERY` → `RF-EXTRACT-FUNCTION`

Use when local temporaries make the desired function boundary carry awkward state. Confirm the query is safe to recompute or cache appropriately.

### Type separation enables variant dispatch
`RF-REPLACE-TYPE-CODE-WITH-SUBCLASSES` → `RF-REPLACE-CONDITIONAL-WITH-POLYMORPHISM`

Use in genuine OO/domain hierarchies. In frontend code, a discriminated union plus strategy/component map may express the same intent without subclasses.

### Regroup then re-extract
`RF-INLINE-FUNCTION` / `RF-INLINE-CLASS` → regroup scattered logic → `RF-EXTRACT-FUNCTION` / `RF-EXTRACT-CLASS`

Use for Shotgun Surgery caused by poorly placed tiny abstractions. The larger intermediate unit must remain verified.

### Split a process, then place responsibilities
`RF-SPLIT-PHASE` → `RF-EXTRACT-FUNCTION` → `RF-MOVE-FUNCTION`

Use when a process has separable stages and a stage has a clearer owner after extraction.

### Control a global before changing its representation
`RF-ENCAPSULATE-VARIABLE` → `RF-RENAME-VARIABLE` / `RF-MOVE-FUNCTION`

Use when a shared variable needs an access seam before changing naming or ownership.

### Encapsulate structured data before its collections
`RF-ENCAPSULATE-RECORD` → `RF-ENCAPSULATE-COLLECTION`

Use when callers currently manipulate raw record fields and raw collection mutation at the same boundary.

## Stop Conditions
Do not continue a sequence when the current step fails verification, exceeds its diff budget, changes a public contract unexpectedly, or removes the precondition for the next edge.
