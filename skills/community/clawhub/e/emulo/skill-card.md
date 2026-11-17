## Description:

Load the user's Emulo profile, mined from their local Claude Code, Codex, and OpenCode session logs, so you work like them instead of a cold start.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ohad6k](https://clawhub.ai/user/ohad6k)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use Emulo before task work to load a locally mined working profile that captures the user's preferences, voice, and failure modes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Emulo reads local AI session histories and creates an agent-facing profile that can influence future task behavior.

Mitigation: Install only when that local access is acceptable, review the generated profile before use, and avoid running it on machines with sensitive unrelated session logs.

Risk: The skill can load an unpinned profile before task work, which may steer agent behavior in unintended ways.

Mitigation: Prefer a pinned, audited package version or sandboxed execution and re-check the profile content before allowing it to shape agent decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ohad6k/skills/emulo)
- [Emulo Project Homepage](https://github.com/ohad6k/emulo)
- [Emulo v0.5.0 Release Notes](https://github.com/ohad6k/emulo/releases/tag/v0.5.0)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and MCP usage notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate or load a local agent-facing profile derived from user session logs.]

## Skill Version(s):

0.5.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
