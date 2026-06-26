# ClawHub Release Notes

This repository is the English-source version of `content-alchemy`.

When building a ClawHub release bundle:

1. Keep `SKILL.md`, `README.md`, `skill.json`, templates, and examples aligned with this repository.
2. Exclude local artifacts such as:
   - `__pycache__/`
   - `*.pyc`
   - `.venv/`
   - local session data
   - temporary markdown files
3. Keep the published bundle focused on:
   - the skill definition
   - scripts
   - templates
   - examples
   - metadata and license

Important note:

The public bundle should expose the skill's English-facing behavior and documentation, while long-document session state should remain local and should never be shipped inside the release package.
