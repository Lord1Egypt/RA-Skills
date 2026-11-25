# Documentation Skill Model

The source bundle contains:

- `scripts/create-docs-skill.sh` to scaffold the bundle;
- generated `scripts/generate-docs-skill.sh` to refresh the mirror;
- `skills/<skill-name>/SKILL.md` and `references/` as the installable skill.

The installable skill is only navigation plus mirrored references. Keep the
generator in the source bundle. The default source mode is the latest default
branch; pinned refs, release tags, package versions, and local checkouts are
explicit offline or reproducibility exceptions.

## Runtime Distribution

OpenClaw's [native skill installer](https://docs.openclaw.ai/cli/skills) accepts
a local directory containing `SKILL.md`:

```bash
openclaw skills install /absolute/path/to/skills/<skill-name> --agent main
openclaw skills list --agent main
openclaw skills check --agent main
```

The default destination is the selected agent's workspace `skills/` folder.
`--global` targets `~/.openclaw/skills`, shared by local agents, and cannot be
combined with `--agent`. Verify discovery in the target agent after install;
copying files is not discovery proof. Respect OpenClaw install-policy warnings
and blocks.

For Codex, install the generated directory under the selected
`CODEX_HOME/skills/<skill-name>` or use its native installer. Verify discovery
in that exact Codex home.

OpenClaw and Codex installations are separate. ClawHub publication is a third,
independent action and requires authority for the destination and reviewed
content. Keep generated docs local unless that authority is explicit.
