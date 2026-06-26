# Structure source routing

Use this only when the user needs help obtaining a structure before CP2K drafting.

## Molecules
- Prefer user-uploaded coordinates when available.
- Otherwise prefer PubChem 3D for ordinary small molecules.
- If no curated 3D structure is available, build a simple starting geometry with ASE or RDKit and label it as approximate.

## Bulk crystals
- Prefer Materials Project for well-known inorganic crystals.
- Otherwise use COD or user-provided CIF/POSCAR.
- If polymorph matters, ask or state which phase was assumed.

## 2D materials and slabs
- Prefer an existing relaxed periodic structure from Materials Project or a user-provided cell.
- If slab orientation or termination matters, ask rather than inventing one.

## Rule
Do not fabricate a “real” crystal structure from only a compound name if multiple chemically distinct choices exist.
