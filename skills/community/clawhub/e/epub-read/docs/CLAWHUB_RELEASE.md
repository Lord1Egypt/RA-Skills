# ClawHub Release Notes

This repository is the English-source version of `epub-read`.

When building a ClawHub release bundle:

1. Keep `SKILL.md`, `README.md`, templates, and metadata aligned with this repository.
2. Exclude local artifacts such as:
   - `__pycache__/`
   - `*.pyc`
   - `.venv/`
   - generated output folders
3. Keep the published bundle lightweight and focused on:
   - the skill definition
   - scripts
   - templates
   - examples
   - license and metadata

Recommended published files:

- `SKILL.md`
- `README.md`
- `LICENSE.md`
- `agents/openai.yaml`
- scripts and templates
- examples
- `requirements.txt` where applicable
