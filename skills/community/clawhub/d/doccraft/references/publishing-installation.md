# Publishing And Installation

Use this reference when preparing the skill for distribution or helping another user install it.

## Publishable contents

The publishable unit is the entire `doccraft` folder.

It should include:

- `SKILL.md`
- `agents/openai.yaml`
- `references/`
- `scripts/`
- `ooxml/`
- `docx-js.md`
- `ooxml.md`
- `LICENSE.txt`

It should not include:

- `__pycache__/`
- bundled `.xsd` schema files when the upload target rejects them
- local test outputs
- temporary JSON or DOCX files
- workspace-specific helper files outside the skill folder

## Distribution options

### 1. Direct folder distribution

Give the recipient the whole skill folder and have them place it under:

- `$CODEX_HOME/skills/doccraft`

This is the simplest path for internal sharing.

### 2. Git repository distribution

Put the skill folder contents into a dedicated repository directory so others can install from the repo.

Recommended repository shape:

```text
doccraft/
  SKILL.md
  agents/
  references/
  scripts/
  ooxml/
  docx-js.md
  ooxml.md
  LICENSE.txt
```

## Runtime dependencies

The skill is self-contained in terms of workflow logic and OOXML helper files, but the host environment still needs:

- Python for the helper scripts
- Node.js for `generate_docx_from_markdown.cjs`
- A resolvable Node `docx` module for new DOCX generation

The `docx` module can be provided by:

- the recipient workspace `node_modules`
- a globally resolvable installation
- `SGDB_DOCX_MODULE` pointing to a module path

If the published package excludes OOXML `.xsd` files for upload compatibility, strict schema validation is not available in that package. Core text generation, DOCX generation, unpack, edit, and repack workflows still work.

## Validation before publishing

Run:

```bash
python <path-to-skill-creator>/scripts/quick_validate.py <path-to-skill>
```

If the host `python` lacks `yaml`, use a Python interpreter that has it installed.

## Packaging

Use [scripts/package_skill.py](../scripts/package_skill.py) to create a clean zip archive for sharing.

The packaging script intentionally excludes `.xsd` files so the resulting archive is safe for upload targets that reject those files.
