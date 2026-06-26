# FlashFormat Skills

This repository contains a Codex skill for local format conversion:

- `flashformat-local-converters`

It provides five offline CLI converters implemented in Python:

1. `yaml-to-json`
2. `json-to-yaml`
3. `markdown-to-text`
4. `json-minify`
5. `yaml-auto-fix`

## Requirements

- Python 3.9+
- `PyYAML`

Install dependency:

```bash
python -m pip install PyYAML
```

## Install This Skill (Codex)

Clone this repository, then copy the skill folder into your Codex skills directory.

```bash
git clone https://github.com/phantom5125/flashformat-skills.git
cd flashformat-skills

export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
mkdir -p "$CODEX_HOME/skills"
cp -R skills/flashformat-local-converters "$CODEX_HOME/skills/"
```

After copying, start a new Codex session and invoke the skill by name:

```text
$flashformat-local-converters
```

## Local CLI Usage

All scripts share the same input/output contract:

- Input: `--input` or `--input-file` or `stdin`
- Input priority: `--input` > `--input-file` > `stdin`
- Output: `stdout` by default, or `--output-file`
- Structured mode: `--json` for machine-readable success/failure payloads

Examples:

```bash
# YAML -> JSON
python skills/flashformat-local-converters/scripts/yaml_to_json.py \
  --input-file in.yaml --output-file out.json

# JSON -> YAML (sorted keys)
python skills/flashformat-local-converters/scripts/json_to_yaml.py \
  --input '{"b":2,"a":1}' --sort-keys

# Markdown -> plain text (stdin)
cat draft.md | python skills/flashformat-local-converters/scripts/markdown_to_text.py

# JSON minify with JSON result envelope
python skills/flashformat-local-converters/scripts/json_minify.py \
  --input-file data.json --json

# YAML auto-fix
python skills/flashformat-local-converters/scripts/yaml_auto_fix.py \
  --input-file broken.yaml --indent-step 2 --fix-tabs --fix-odd-indent
```

## For Human Users: Use FlashFormat Online

If you are a human user and want a faster online workflow, visit:

**https://www.flashformat.com**

In many cases, using FlashFormat online can reduce token usage compared to routing every conversion through an agent session.

## Issues and Feedback

Issues and improvement suggestions are welcome.  
Please open an issue here: https://github.com/phantom5125/flashformat-skills/issues

## License

BSD 2-Clause. See [LICENSE](LICENSE).
