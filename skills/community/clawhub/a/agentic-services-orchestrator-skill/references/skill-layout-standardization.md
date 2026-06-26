# Skill Layout Standardization

This audit covers the sibling `agentic_*_skill` repositories that make up the CompleteTech LLC agentic services skill library.

## Shared Shell

Every related skill should expose this outer shell so humans, automation, and the orchestrator can find the same kinds of assets in the same places:

- `.gitattributes`
- `.gitignore`
- `LICENSE`
- `README.md`
- `SKILL.md`
- `BRAND_ASSETS.md`
- `requirements.txt`
- `agents/`
- `assets/`
- `assets/diagrams/`
- `references/`
- `scripts/`
- `examples/`

## Intentional Differences

The shared shell does not require identical internals.

| Skill family | Repositories | Intentional differences |
|---|---|---|
| Renderer/reference skills | case study, customer success, delivery, discovery, email, invoice, proposal, security review | Use `references/` catalogs and `scripts/render_*.py` helpers to render branded draft artifacts. |
| Generator/config skills | certificate, contract, envelope | Keep root-level `generate_*.py`, `config.ini`, `pyrightconfig.json`, and input override examples for backwards-compatible CLI use. Shared `references/` and `scripts/` folders exist for supporting docs and future helper automation. |
| Orchestrator | services orchestrator | Keeps workflow schemas/adapters in `references/` and coordinates routing/state instead of generating a specialist artifact directly. |

## Mermaid Sources

Each skill keeps its Mermaid workflow source under `assets/diagrams/`. README files should include the inline Mermaid for GitHub rendering and link to the `.mmd` source. PNG diagram files are not part of the standard shell.

## Placeholder Directories

When a standard directory has no active implementation files yet, keep a short `README.md` explaining the directory's intended use. This makes the layout commit-friendly without inventing unused code.

## Validation Expectations

- Mermaid sources should parse/render with Mermaid CLI when available.
- YAML, JSON, and INI files should parse with standard parsers.
- Generator-style workflows should retain their existing root CLI entry points.
- Existing business logic, templates, examples, generated previews, and outputs should not be deleted as part of shell standardization.
