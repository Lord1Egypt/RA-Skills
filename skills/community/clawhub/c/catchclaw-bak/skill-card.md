## Description:

Search, install, and export agentars from the CatchClaw marketplace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aliezu](https://clawhub.ai/user/aliezu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to search CatchClaw marketplace agentars, install selected agent templates into OpenClaw workspaces, export local agents as distributable ZIP archives, and roll back workspace changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install unverified marketplace content into persistent agent workspaces.

Mitigation: Install only content from trusted CatchClaw publishers and inspect downloaded agentars before use.

Risk: Overwrite installs can replace the main OpenClaw workspace.

Mitigation: Prefer creating a new agent and use overwrite mode only after explicit user selection and backup awareness.

Risk: API keys may be written during installs that use command-line credential options.

Mitigation: Avoid passing API keys on the command line and review generated credential files after installation.

Risk: Custom install names containing path separators or traversal sequences may weaken containment.

Mitigation: Use simple workspace names without path separators or traversal such as '..' until this behavior is fixed.

## Reference(s):

- [CatchClaw skill page](https://clawhub.ai/aliezu/skills/catchclaw-bak)
- [CatchClaw homepage](https://github.com/OpenAgentar/catchclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and write local agent workspace paths and may call the CatchClaw API when searching or installing agentars.]

## Skill Version(s):

1.0.11 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
