# Skill Eval Fixtures

These fixtures are intentionally agent-agnostic. The harness consumes normalized
trace JSON only:

- `runner` is descriptive metadata, not a required CLI or model runtime.
- `shell_commands`, `read_paths`, `write_paths`, `artifact_paths`, token counts,
  and `skill_evidence` are the stable contract.
- Unit tests and release verification never call Codex, Claude, Qoder, OpenClaw,
  or any other live agent.

If a maintainer wants to evaluate an external run, capture that run outside this
repo, convert it into `normalized-v1`, then pass it with `--runner trace
--normalized-trace <file> --case-id <id>`.
