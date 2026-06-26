# Beamer generation contract

Use this contract when converting a paper or paper notes into a Beamer package.

## Required deliverables

Write all deliverables into one canonical output directory:

- `analysis.json`
- `slides.json`
- `main.tex`
- `main.pdf` if compilation succeeds
- `README.md`
- `asset_manifest.json`
- `figures/`

## Content requirements

- Preserve every source figure, table, subfigure, and appendix figure/table that is available from the source.
- If content does not fit, split across more frames/pages; do not replace source material with “see paper”.
- Treat any requested page count as a lower bound, not an upper bound.
- Use Chinese academic presentation prose suitable for an audience that has not read the paper.
- Include background, method, formal results, numerical study, insights, and conclusion significance.
- Separate formal mathematical statements from economic/technical intuition when dense.
- Translate crucial theorem/proposition/lemma/corollary/definition/assumption statements faithfully and fully into Chinese.
- Give numerical experiments dedicated coverage rather than burying them in an appendix index.
- Give each insight its own page when needed.

## Visible text constraints

Do not render internal planning metadata into visible Beamer text. Keep these only in JSON metadata or notes:

- `core_message`
- `source_paragraph_ids`
- `paragraph_ledger`
- coverage tracking labels
- speaker-note scaffolding
- `核心信息`
- `来源段落`
- `这页负责`
- `服务于未读论文听众`

Use natural academic wording instead of internal labels.

## Equation and notation requirements

- `equation_coverage` may mark an equation as covered only if the corresponding frame visibly contains an equation/align/math display.
- Do not count a prose-only mention or notes-only mention as equation coverage.
- If the source has a continuous numbered equation range with 3 or more equations, do not show only one representative formula and claim the whole range is covered.
- Preserve exact equation numbers or ranges when available, for example `Eq. (1)`, `Eqs. (2)-(3)`, `Eq. (13)-(16)`.
- Define abbreviations, symbols, operators, and hyperparameters on first visible use using source-supported definitions.
- `notation_coverage` should include `source_paragraph_ids`, `source_quote`, `source_definition_summary`, and `defined_on_first_visible_use=true` when applicable.

## Final acceptance fields

The final report should expose structured acceptance fields:

- `compile_status`
- `readability_status`
- `tex_warnings`
- `layout_policy`
- `visible_prose_recovery_hint`
- `visible_prose_fidelity_final`
- `render_fidelity_safeguards`
