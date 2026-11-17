## Description:

Installs an OpenClaw internal hook that auto-titles each new chat session using the session's current model on message receipt, with a fallback to truncating the first message.

This skill is ready for commercial/non-commercial use.

## Publisher:

[woohahahaaa](https://clawhub.ai/user/woohahahaaa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to install and enable a background hook that automatically labels new chat sessions. It helps keep session lists readable without requiring the agent to invoke a manual naming workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an always-on hook with broad activation language.

Mitigation: Require explicit operator confirmation before installation and disable the hook when automatic session labeling is not wanted.

Risk: The security scan reports a real path-scoping flaw around agent IDs.

Mitigation: Patch and review agent ID path validation before deployment in shared or sensitive environments.

Risk: First-message content may be sent to the active model provider for title generation.

Mitigation: Document this data flow for users and avoid enabling the hook for sessions that may contain sensitive first-message content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/woohahahaaa/skills/auto-rename-session-label)
- [OpenClaw project homepage](https://github.com/openclaw/openclaw)
- [README](artifact/README.md)
- [Hook documentation](artifact/hook/HOOK.md)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell commands and bundled TypeScript hook files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Installs an operator-managed hook that writes session labels and may send the first user message to the active model provider for title generation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
