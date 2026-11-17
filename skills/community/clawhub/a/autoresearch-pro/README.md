# autoresearch-pro

Version 2.0.0 updates the existing autoresearch-pro package. It shares its core workflow
with [the GitHub source](https://github.com/0xcjl/autoresearch-pro).

Default to one reversible experiment, at most three rounds. Keep the baseline,
compare actual artifacts, preserve permission boundaries, and mark unavailable
runtime tests as unverified. This package needs no scripts, dependencies or keys.

## Agent setup

Install this directory as autoresearch-pro, keeping SKILL.md and references
together. Use only one active version per client.

| Client | User-level entry point | Discovery check |
|---|---|---|
| Codex | ~/.agents/skills/autoresearch-pro | Skill picker or codex debug prompt-input |
| Claude Code | ~/.claude/skills/autoresearch-pro | /autoresearch-pro in command picker |
| Hermes | $HERMES_HOME/skills/autoresearch-pro; default ~/.hermes/skills | hermes skills list --source local --enabled-only, then skill_view |
| OpenClaw | Managed ~/.openclaw/skills or personal shared skill root | openclaw skills info autoresearch-pro --agent YOUR_AGENT_ID --json |

Codex, Claude Code and Hermes can share one source using per-client directory
links where supported. For OpenClaw, check discovery first and otherwise use its
native local installer. Profile paths, filters and symlink support vary by host.
The core does not require client-specific tools, hooks, or plugins.

Back up an old installation outside active roots, compare local edits, then update
the active directory name and references. The registry retains its existing
autoresearch-pro slug; existing local directories are not automatically renamed.
Keep historical provenance. Local discovery checks do not prove behavioral
quality on every model. See the GitHub README for the five-case test limitations.

Inspired by Karpathy/autoresearch and 0xcjl/openclaw-autoresearch-pro.
This registry distribution is authorized under ClawHub's MIT-0 terms. The
GitHub source remains MIT; original attribution is retained here voluntarily.
