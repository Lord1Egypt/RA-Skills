# ClawHub Publishing

This repository is prepared for ClawHub publishing as a text-based OpenClaw skill bundle.

## Included In ClawHub

The ClawHub bundle is intended to include text-based skill material only:

- `SKILL.md`, `README.md`, `QUALITY.md`, and this file
- `agents/openai.yaml`
- `pyproject.toml`
- `.github/workflows/quality.yml`
- `scripts/*.py`
- `references/` text files, schemas, catalogs, and examples
- `examples/` text inputs such as `.ini` files or README placeholders
- `assets/diagrams/*.mmd`
- config examples and templates where they are text-based

## Excluded From ClawHub

`.clawhubignore` excludes binary and generated assets from the publish candidate, including PDFs, PNG previews, DOCX files, fonts, logos, `preview/`, `output/`, caches, virtual environments, local env files, and temporary files.

Those files remain part of the GitHub repository for brand presentation, examples, local demos, and generated artifact previews. They are not part of the ClawHub text bundle.

## License And Brand Boundary

ClawHub publishes skills under MIT-0. The text/code bundle can be used under ClawHub's publishing terms, but CompleteTech LLC names, logos, seals, and other brand assets remain reserved. Publishing this text bundle does not grant a trademark or brand-asset license and does not relicense excluded binary brand assets.

## Runtime Dependencies

Runtime requirements are declared in `SKILL.md` under `metadata.openclaw`.

- All Python-backed skills require `python3`.
- PDF/generator skills declare `reportlab` where PDF rendering is used.
- The contract skill declares `jinja2`.
- `pyyaml` is declared so the included quality/audit validator can parse YAML metadata.
- Optional PNG preview dependencies such as `pypdfium2` and `pillow` are GitHub/local-demo conveniences, not required for the ClawHub core workflow unless a user intentionally runs PNG preview generation.

## Local Readiness Check

Run before publishing:

```bash
python3 scripts/validate_quality.py
```

The validator checks lint, Python compilation, structured-file parsing, Mermaid rendering, smoke tests, Pyright where configured, and ClawHub bundle readiness. It does not publish to ClawHub.

## Publishing

Do not publish automatically. Use the ClawHub CLI only after explicit approval and an authenticated owner context, for example:

```bash
clawhub skill publish . --owner <owner> --version <semver>
```
