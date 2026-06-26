# Beamer Pipeline Public

Convert academic papers or structured paper notes into a Chinese academic Beamer deliverable through the same seven-phase pipeline shape as the original `/beamer` shortcut, while keeping the public package free of private Telegram queue, worker, session, and local-path coupling.

## v0.3.0

- Removed all hardcoded `~/clawd/*` paths in artifact-search roots; replaced with `~/.openclaw/*` equivalents so the skill runs correctly on any OpenClaw installation.
- Added `run_agent_role.js` with shared agent-role dispatch logic (programmer/reviewer/tester).
- Added full repair/scanner script suite: equation coverage repair, instruction leak repair, notation coverage repair, strategy placeholder repair, equation coverage scanner, slide symbol scanner, and coverage status.
- Enhanced `deck_language_render_guards.js` for output language constraints.
- All 15 JS scripts pass `node -c` syntax verification.

## What this skill does

This skill provides a publishable, local-first Beamer pipeline runner. It preserves the original seven-stage contract:

1. `analysis` / 分析: build `analysis.json` with paragraph, figure, table, equation, notation, and formal-statement ledgers.
2. `slides_outline_skeleton` / slides 大纲: build `slides.json` with roadmap, conclusion preview, body/appendix split, and slide skeletons.
3. `equation_coverage` / 公式覆盖: resolve `equation_coverage` to concrete slide/frame mappings.
4. `notation_consistency` / 记号一致性: resolve `notation_coverage`, first visible definitions, and cross-slide consistency.
5. `compile_and_structural_repair` / 编译与结构修复: produce `main.tex`, compile or repair `main.pdf`, and check structural alignment.
6. `review_and_auto_rework` / reviewer 审核与自动返工: convert reviewer failures into repair work and revalidate.
7. `final_acceptance_delivery` / 终验与交付: package final artifacts and require ready-for-review acceptance fields.

The public runner creates phase prompts, phase logs, state files, workspace contracts, and local validation gates. Agent execution is intentionally pluggable via `--agent-cmd` so that ClawHub users can attach their own OpenClaw or LLM runtime without shipping Yilin's private Telegram worker/session implementation.

## Deliverable folder

The pipeline writes one canonical output directory containing, as phases progress:

- `analysis.json`
- `slides.json`
- `main.tex`
- `main.pdf` when LaTeX compilation succeeds
- `README.md`
- `asset_manifest.json`
- `figures/`
- `beamer_task_contract.md`
- `beamer_pipeline_state.json`
- `beamer_phase_log.jsonl`
- `phase_<n>_<name>_prompt.md`

## Inputs

- A source document path, usually Markdown converted from a paper, or a paper-note file.
- An output directory.
- Optional execution flags for dry-run, single-phase execution, validation, asset preparation, LaTeX command, and agent command.

## CLI usage

```bash
node scripts/run_beamer_public.js --input paper.md --out out --dry-run
node scripts/run_beamer_public.js --input paper.md --out out --init-only
node scripts/run_beamer_public.js --input paper.md --out out --phase 1 --agent-cmd 'your-agent --prompt {prompt}'
node scripts/run_beamer_public.js --input paper.md --out out --validate-phase 5
```

Supported options:

- `--init-only`: prepare workspace, localized assets, and contract only.
- `--dry-run`: print the seven-phase plan and required artifacts.
- `--phase <1-7>`: run one phase.
- `--validate-phase <2-6>`: validate existing artifacts for a phase gate.
- `--agent-cmd <command>`: command used to produce/repair artifacts for each phase.
- `--latex-cmd <command>`: LaTeX command for phase 5, default `LATEXMK_BIN` or `latexmk`.
- `--skip-assets`: skip `prepare_task_assets.js`.

`--agent-cmd` placeholders:

- `{prompt}`: generated phase prompt file path, shell-quoted.
- `{phase}`: phase index.
- `{phaseName}`: phase name.
- `{out}`: output directory, shell-quoted.
- `{input}`: source file path, shell-quoted.

## Agent setup (required for default `--agent-cmd`)

The default agent command uses `{role}` which maps to three agent IDs:

| Phase | Agent ID    |
|-------|-------------|
| 1-5   | programmer  |
| 6     | reviewer    |
| 7     | tester      |

These are **not** standard OpenClaw agent IDs — they must be configured in the user's
`~/.openclaw/openclaw.json` under `agents.list`. A minimal configuration example:

```json
{
  "agents": {
    "list": [
      { "id": "main", ... },
      {
        "id": "programmer",
        "name": "Programmer",
        "model": { "primary": "your-model" },
        "workspace": "/path/to/workspace"
      },
      {
        "id": "reviewer",
        "name": "Reviewer",
        "model": { "primary": "your-model" },
        "workspace": "/path/to/workspace"
      },
      {
        "id": "tester",
        "name": "Tester",
        "model": { "primary": "your-model" },
        "workspace": "/path/to/workspace"
      }
    ]
  }
}
```

### Alternatives

- **`--no-agent`**: skip all agent invocations and write prompt files only. Useful for inspection or manual execution.
- **Custom `--agent-cmd`**: provide your own command, e.g. `--agent-cmd 'openclaw agent --agent main --message "$(cat {prompt})"'` to route all phases through a single agent.

## Quality contract

A generated deck should:

- Preserve all source figures, tables, subfigures, and appendix figures/tables when available.
- Expand slide count as needed; any target slide count is a lower bound, not a cap.
- Include a roadmap page and conclusion-preview page.
- Use formal Chinese academic presentation style.
- Separate formal statements from intuition when both are needed.
- Give full faithful Chinese translations for crucial theorem/proposition/lemma/corollary/definition/assumption statements.
- Keep visible slide text free of internal scaffold labels such as `core_message`, `source_paragraph_ids`, `paragraph_ledger`, `核心信息`, `来源段落`, `这页负责`, and `服务于未读论文听众`.
- Track figure/table/equation/notation/formal-statement coverage explicitly.
- Define symbols, abbreviations, operators, and hyperparameters on first visible use using source-grounded definitions.

## Included scripts

### Pipeline runner
- `scripts/run_beamer_public.js`: public seven-phase runner with pluggable agent execution.
- `scripts/run_agent_role.js`: shared agent-role logic for programmer/reviewer/tester phases.
- `scripts/beamer_phase_blueprint.js`: seven-phase names, goals, required artifacts, and planned-coverage gates.
- `scripts/prepare_task_assets.js`: localizes markdown image URLs into `figures/` and writes `asset_manifest.json`.
- `scripts/beamer_acceptance_contract.js`: validates final structured Beamer acceptance fields.

### Repair scripts (auto-fix specific quality issues)
- `scripts/deck_equation_coverage_repair.js`: repairs unresolved equation coverage entries.
- `scripts/deck_instruction_leak_repair.js`: removes scaffold/internal instruction leakage from slide text.
- `scripts/deck_notation_coverage_repair.js`: repairs missing or inconsistent notation coverage.
- `scripts/deck_strategy_placeholder_repair.js`: replaces strategy placeholders with concrete content.

### Scanner scripts (detect quality issues)
- `scripts/deck_equation_coverage_scanner.js`: scans for equation coverage gaps.
- `scripts/slide_symbol_scanner.js`: scans for symbol definition/usage inconsistencies.
- `scripts/coverage_status.js`: computes coverage status across equation/notation/formal-statement dimensions.

### Shared utilities
- `scripts/deck_symbol_canonicalization.js`: shared symbol canonicalization helper.
- `scripts/deck_language_render_guards.js`: render guard constraints for output language.
- `scripts/slide_schema.js`: shared slide/equation block normalization helper.

## Dependencies

Required:

- Node.js 18+ or newer

Optional:

- A LaTeX distribution such as TeX Live or MacTeX
- `latexmk` or `xelatex` for compiling `main.tex` to `main.pdf`
- An OpenClaw or other agent runtime wired through `--agent-cmd`

## Privacy and portability notes

This public package intentionally excludes:

- Telegram bot tokens and session targets
- `.openclaw` runtime state
- SQLite task databases
- launchd worker configuration
- private OpenClaw runtime/session/database orchestration code
- executable upstream reference snapshots
- user-specific logs and caches
- private source PDFs or historical task outputs

Do not publish generated paper decks unless you have the right to redistribute their source content and figures.
