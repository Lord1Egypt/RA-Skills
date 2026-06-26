# dreamlover-skill

> Distill anime and game character materials into reusable character skills. The top-level skill generates the character package, then installs a Codex version first and optionally exports an OpenClaw version.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Agent Skill](https://img.shields.io/badge/Agent-Skill-green)](https://github.com/tobemorelucky/dreamlover-skill)

Repo: [tobemorelucky/dreamlover-skill](https://github.com/tobemorelucky/dreamlover-skill)  
[中文](README.md)

## What It Is

`dreamlover-skill` is the generator skill.

It first creates one shared static character source:

- `canon.md`
- `persona.md`
- `style_examples.md`
- `meta.json`

Then it builds platform wrappers from that source:

- Codex primary install: `./.agents/skills/{slug}/`
- OpenClaw optional export: `<openclaw_workspace>/.agents/skills/{slug}/`

Treat `characters/{slug}/` as the canonical source.  
The Codex install and the OpenClaw export are generated outputs and should not be edited by hand.

## Installation

### Claude Code

```bash
git clone https://github.com/tobemorelucky/dreamlover-skill ~/.claude/skills/dreamlover-skill
```

### Codex

```bash
git clone https://github.com/tobemorelucky/dreamlover-skill $CODEX_HOME/skills/dreamlover-skill
```

### Requirements

- Python 3.9+
- The current version is text-first
- `python3` is required if you want conditional memory at runtime

## Usage

### 1. Create a character with the top-level skill

```text
$dreamlover-skill
Help me create a Rem character skill
```

The generator should run intake first, confirm the draft, install the Codex package, and then optionally export an OpenClaw package.

### 2. Create from CLI

```bash
python tools/skill_writer.py --action create --interactive
python tools/skill_writer.py --action create --slug rem --name "Rem"
python tools/skill_writer.py --action create --slug rem --name "Rem" --openclaw-workspace /path/to/openclaw-workspace
```

### 3. Use the generated child skill in Codex

After generation, the Codex child skill should be at:

```text
./.agents/skills/{slug}/
```

Check and invoke it with:

```text
/skills
$rem
```

### 4. Use the exported package in OpenClaw

If export is enabled, the OpenClaw package should be at:

```text
<openclaw_workspace>/.agents/skills/{slug}/
```

Then:

- refresh skills or start a new session
- let OpenClaw discover the child skill from the workspace
- trigger it through normal conversation

## Conditional Memory

Generated child skills keep conditional memory:

- small talk should usually skip memory
- memory is only read or written when the gate is hit
- runtime data lives in `<workspace>/.dreamlover-data/memory.sqlite3`
- `.dreamlover-data/` is not copied into the skill package

If `python3` is unavailable, the child skill should fall back to no-memory mode instead of failing entirely.

## Minimal Verification

### Verify Codex primary install

```bash
python tools/skill_writer.py --action create --interactive
```

Expected result:

- `characters/{slug}/` contains the shared static source
- `./.agents/skills/{slug}/` contains the Codex-ready child skill

### Verify OpenClaw export

```bash
python tools/skill_writer.py --action create --slug rem --name "Rem" --openclaw-workspace /tmp/openclaw-demo
```

Expected result:

- `/tmp/openclaw-demo/.agents/skills/rem/` exists
- static files match the Codex package
- only `SKILL.md` and required `runtime/` differ by platform

## License

MIT
