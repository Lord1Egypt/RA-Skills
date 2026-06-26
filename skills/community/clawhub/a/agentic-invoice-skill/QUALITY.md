# Quality Checks

Run the production-readiness checks from this repository root:

```bash
python3 scripts/validate_quality.py
```

The validator compiles Python files, runs Ruff, parses YAML/JSON/INI files, renders Mermaid sources when Mermaid tooling is available, runs generator `--help` smoke checks where generator scripts exist, runs catalog `--list` smoke checks where renderer catalog scripts exist, and runs Pyright when a `pyrightconfig.json` file is present.

GitHub Actions runs the same validator on push and pull request.
