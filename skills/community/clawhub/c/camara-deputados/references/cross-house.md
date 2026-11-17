# Tracking a proposition across both houses

The Chamber and Senate assign different identifiers to related legislative records. Never send a Chamber proposition ID directly to a Senate matter-detail endpoint or treat a Senate process ID as a Chamber proposition ID.

## Chamber to Senate

1. Resolve the Chamber proposition by `siglaTipo`, `numero`, and `ano`.
2. Inspect its detail and movements for transfer to the Senate.
3. Search the Senate `/processo` collection by the corresponding identification or terms.
4. Preserve the Chamber proposition ID, Senate matter code, and `IdentificacaoProcesso` as separate fields.

## Senate to Chamber

1. Retrieve the Senate process detail and inspect autuações and house identifiers.
2. When the process records a Chamber designation, query `/proposicoes` with the Chamber `siglaTipo`, `numero`, and `ano`.
3. Enrich with Chamber detail and movements; do not infer equivalence from title similarity alone.

For an auditable answer, show both official identifiers and link each house's record separately.
