## Description:

References and refreshes a local OpenClaw documentation snapshot for product usage, deployment, configuration, CLI commands, channels, gateway behavior, tools, troubleshooting, and docs-version verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lueashes](https://clawhub.ai/user/lueashes)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to answer product, deployment, configuration, CLI, channel, gateway, tool, and troubleshooting questions from a pinned local documentation snapshot. When explicitly requested, they use it to refresh, validate, index, and summarize changes in that snapshot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Refresh mode can clone upstream OpenClaw documentation and rewrite the local docs snapshot when explicitly requested.

Mitigation: Use refresh mode only after an explicit user request, treat upstream refs as read-only, limit writes to the skill's docs and state files, and run validation, index rebuild, and diff generation before reporting success.

Risk: Documentation examples may include installer commands or sample secrets that should not be executed or treated as credentials.

Mitigation: Review quoted installer commands before running them, do not execute downloaded scripts from documentation examples, and treat example tokens or passwords as documentation text only.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lueashes/skills/claw-wiki)
- [SKILL.md](SKILL.md)
- [README.md](README.md)
- [SECURITY.md](SECURITY.md)
- [Update workflow](references/update-workflow.md)
- [Snapshot source lock](state/source-lock.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with file-path citations and occasional shell command snippets for explicit refresh workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers should be grounded in files read from the bundled OpenClaw docs snapshot; refresh output should include validation and diff status.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
