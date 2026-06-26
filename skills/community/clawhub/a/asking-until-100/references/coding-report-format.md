# Coding Report Format

For highest-rigor coding and project-build tasks, begin with a provisional ASCII project structure
under `Provisional Project Structure` and then emit sections in this order:

1. `Working Hypothesis`
2. `Architecture Questions`
3. `Product Questions`
4. `Constraint Questions`
5. `Decision-Critical Unknowns`

## Project structure rules

- Use an ASCII tree.
- Keep the tree plausible and minimal.
- Treat the structure as a proposal to validate, not a final decision.
- Prefer `repo_plus_prompt` when an existing repo clearly looks relevant.
- Fall back to prompt-only archetypes for greenfield or weak-signal cases.

## Working hypothesis rules

The `Working Hypothesis` block must include:

- the working hypothesis itself
- execution gate summary
- blocking dimensions
- repo signal summary when repo inspection materially shaped the report

## Question rules

- Ask architecture questions first because they change the implementation shape.
- Ask product questions next so the user can correct scope or behavior early.
- Ask constraint questions after that to surface delivery, security, rollback, and timeline risks.
