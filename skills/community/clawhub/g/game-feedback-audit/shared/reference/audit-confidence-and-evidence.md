# Audit Confidence and Evidence

Every important finding should include:
- `confidence`: `high`, `medium`, or `low`
- `evidence`: one or more of `code`, `config`, `asset`, `screenshot`, `docs`, `inferred`

Use `high` when the issue is directly supported by implementation evidence.
Use `medium` when several signals point the same way but runtime proof is missing.
Use `low` when the issue is plausible but weakly evidenced.

Prefer explicit uncertainty over false confidence.
