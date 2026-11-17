# Phase 4: Verify

Run every applicable check and report pass/fail individually.

## Structure

- Parse all YAML/frontmatter and require expected files, types, IDs, links, and indexes.
- Ensure catalog entry points resolve to existing facts/dimensions/measures and every source
  operation has evidence.
- Check required fields, unique names/IDs, stable paths, and no unresolved placeholders outside
  explicitly open evidence.

## Semantic Lint

- One business key cannot define two differently named dimensions; repeated same-name dimensions are
  identical.
- Reuse an existing shared dimension when the business key matches.
- Every fact has a falsifiable grain, time semantics, dimensions compatible with grain, and measures
  with declared additivity and unit/basis.
- Routes stay inside their evidence boundary and request all context needed by the selected source
  operations.
- No invented field, enum, value, relationship, or aggregation appears without a citation.

For OKF, additionally validate v0.1 root metadata, allowed concept types, concept paths, required
body sections, relative links, and citations. A mechanically repairable formatting error may be
fixed and rechecked. Any semantic failure returns to Phase 2 with one blocking question; never
silently pass or downgrade it.
