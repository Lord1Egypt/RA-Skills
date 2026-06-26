# Design rules

## Product goal

Turn a vague CP2K request into a runnable draft with transparent assumptions.

## Priorities

1. Prefer scientific honesty over pretending certainty.
2. Prefer runnable defaults over overfitted sophistication.
3. Prefer explicit warnings over hidden heuristics.
4. Prefer deterministic script output for repetitive steps.

## Follow-up policy

Ask only if the missing information changes the physical meaning of the job or blocks drafting entirely.

Do not ask for:
- speed vs accuracy if a balanced preset is fine
- hardware details unless the user specifically wants machine-aware tuning
- vacuum padding for an ordinary isolated molecule

Ask or flag review when:
- charge is plausibly nonzero
- spin state is unclear for open-shell or transition-metal systems
- an xyz file is being treated as a periodic crystal/slab
- a specialized workflow is requested beyond the supported draft space

## Output rules

Always emit or explain:
- what task was inferred
- why periodicity was chosen
- what basis/potential family was used
- whether SCF is OT or diagonalization
- whether k-points are heuristic
- whether dispersion was added
- what the user should review before production use
