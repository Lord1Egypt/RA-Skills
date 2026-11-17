## Description:

Fast OpenAI Codex account switching for OpenClaw via the local cs command, including relogin start, OAuth callback completion, and status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anjun](https://clawhub.ai/user/anjun)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to switch the local OpenAI Codex account in OpenClaw, complete a relogin callback, or inspect account-switching status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive OAuth callback input is handled through a shell-style command pattern.

Mitigation: Use the skill only when intentionally switching the local Codex account, avoid callback text from untrusted sources, require explicit confirmation for callback completion, and pass callback data as structured input where possible.

Risk: Raw authentication errors may expose sensitive details.

Mitigation: Redact authentication errors before showing them and avoid displaying full tokens or secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anjun/skills/cs-relogin)
- [Publisher profile](https://clawhub.ai/user/anjun)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Concise Markdown text with shell command snippets, login URLs, callback instructions, and status summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command stderr on failure; should avoid exposing full tokens or secrets.]

## Skill Version(s):

1.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
