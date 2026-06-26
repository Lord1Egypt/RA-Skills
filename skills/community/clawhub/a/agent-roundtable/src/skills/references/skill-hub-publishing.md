# Skill Hub Publishing Notes for Roundtable

Use this when preparing the Roundtable skill for Hermes Skill Hub and OpenClaw/ClawHub release.

## Package shape

- Public skill directory: `src/skills/`
- Required files:
  - `src/skills/SKILL.md`
  - `src/skills/.clawhubignore`
- `SKILL.md` should include both metadata blocks:
  - `metadata.hermes.tags` and `metadata.hermes.related_skills`
  - `metadata.openclaw.requires.env`, `metadata.openclaw.requires.bins`, and `metadata.openclaw.primaryEnv`
- Keep the skill directory self-contained and generic: no private chat IDs, tokens, webhook URLs, local paths, or team-only instructions.

## CLI checks before release

```bash
hermes skills publish --help
clawhub publish --help
clawhub whoami
```

If `clawhub whoami` returns `Error: Not logged in. Run: clawhub login`, do not publish yet. Ask the user to log in or confirm the target account.

## Suggested commands

Hermes Skill Hub:

```bash
hermes skills publish src/skills --to github --repo <target-repo>
```

OpenClaw / ClawHub:

```bash
clawhub publish src/skills \
  --slug roundtable \
  --name "Roundtable" \
  --version 1.0.0 \
  --tags discussion,multi-agent,collaboration,debate,roundtable \
  --changelog "Initial Roundtable skill release for structured multi-agent discussions."
```

The current ClawHub CLI command shape is `clawhub publish <path>`; do not use older forms such as `clawhub skill publish` unless the CLI help has changed.

## ⚠️ Pitfalls

1. **MIT-0 license acceptance required server-side**: `clawhub publish` fails with `Error: MIT-0 license terms must be accepted to publish skills`. This acceptance **cannot be done via CLI** — the user must accept the MIT-0 terms on the ClawHub website first. The CLI has no `--accept-license` flag. Resolution: ask the user to visit ClawHub website → accept terms → retry publish.

2. **`clawhub login` is separate from publishing**: Login stores a token in `~/Library/Application Support/clawhub/config.json` (macOS). Even after successful login, the license acceptance gate still blocks publishing until accepted server-side.

3. **Hermes has no central Skill Hub registry**: `hermes skills publish --to github --repo <target>` publishes to a specific GitHub repo. There is no official `hermes-hub/skills` repo yet. To distribute a Hermes skill, create a dedicated GitHub repo (e.g., `your_github_username/hermes-skills-roundtable`) and tell users to add it as a tap or install from the raw repo. Alternatively, contribute to `hermes-hub/skills` if one exists at publish time — check with `hermes skills publish --help` for updated guidance.

4. **Python package (PyPI) is independent**: The `uv build` / `python -m build` step produces sdist+wheel for PyPI. This is separate from both Hermes and ClawHub publishing. PyPI upload uses `twine upload dist/*` or `uv publish` — not `clawhub` or `hermes` CLI.

## Hygiene validation

Run a lightweight metadata and secret scan before publishing:

```bash
python3 - <<'PY'
from pathlib import Path
import re
text = Path('src/skills/SKILL.md').read_text()
assert text.startswith('---\n')
assert '\n---\n' in text[4:]
for key in ['name: roundtable', 'description:', 'version:', 'platforms:', 'metadata:', 'hermes:', 'openclaw:', 'requires:']:
    assert key in text, f'missing {key}'
patterns = [r'Bearer\s+[A-Za-z0-9._-]+', r'oc_[0-9a-f]{20,}', r'ou_[0-9a-f]{20,}', r'cli_[0-9a-f]{10,}', r'sk-[A-Za-z0-9]{20,}']
for pat in patterns:
    assert not re.search(pat, text, flags=re.I), f'sensitive-looking content: {pat}'
print('SKILL.md validation OK')
PY
```

Validate Python package build separately; prefer `uv build` if the active Python lacks the `build` module:

```bash
uv build
# or
python -m build --sdist --wheel
```

Inspect artifacts and ensure no private/internal files are included:

```bash
python3 - <<'PY'
import tarfile, zipfile
from pathlib import Path
for f in sorted(Path('dist').glob('agent_roundtable-*')):
    if f.name.endswith('.tar.gz'):
        with tarfile.open(f) as t: names = t.getnames()
    elif f.suffix == '.whl':
        with zipfile.ZipFile(f) as z: names = z.namelist()
    else:
        continue
    bad = [n for n in names if any(x in n for x in ['docs/internal', '.env', 'node_modules', '.venv', '.DS_Store'])]
    assert not bad, (f, bad[:10])
    print(f, 'OK', len(names), 'entries')
PY
```

## Release gate

Do not perform the real publish until the user confirms:

1. The ClawHub/OpenClaw account is logged in and correct.
2. The Hermes Skill Hub target repo/registry/tap.
3. Whether the release should publish as a personal account or organization owner.

After publishing, verify search/inspect/install on both channels and confirm the installed skill exposes the expected roundtable tools.