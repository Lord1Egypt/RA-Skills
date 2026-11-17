# Docs Skill Model

The Hindsight-style docs skill model is a source folder that generates a skill:

- `scripts/generate-docs-skill.sh` for deterministic refresh/generation;
- `skills/<skill-name>/SKILL.md` for trigger rules and navigation;
- `skills/<skill-name>/references/` for local documentation;
- installed skill shape is only `SKILL.md` plus `references/`, matching `hindsight-docs`;
- the builder itself stays small; generated docs skills may have large `references/` by design.

The only allowed functional difference for a new tool is the source mapping step:
the agent must inspect the target repo layout first because docs directories vary.
After paths are chosen, generation/update should look like Hindsight.

The default source mode is repo/latest. For GitHub or Git repository sources,
the skill should fetch the current default branch HEAD unless the operator
explicitly requests a pinned ref, release tag, or offline local checkout.

## Update Script Requirements

An update script should:

- fetch only the declared source;
- refresh the current default branch HEAD by default for Git sources;
- use explicit docs paths chosen after a repo mapping pass;
- require an explicit flag for pinned/offline/local-checkout refreshes;
- write only inside the source bundle and generated skill folder;
- avoid secrets and private data;
- fail closed if the source layout changes unexpectedly.

## Install Guidance

For Codex-only install, the target is:

```text
$CODEX_HOME/skills/<skill-name>
```

For installer-backed portable install, the generated skill must live in a GitHub repo/path accepted by:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo owner/repo \
  --path path/to/skill
```
