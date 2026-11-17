## Description:

Helps developers diagnose acpx bridge connection failures, initialization timeouts, gateway token issues, Claude Code authentication failures, channel routing problems, and model endpoint configuration mistakes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roger0808](https://clawhub.ai/user/roger0808)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to troubleshoot OpenClaw ACP/acpx bridge connectivity, token setup, Claude Code CLI configuration, channel compatibility, and gateway reachability issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes credential-handling guidance that could overwrite an existing persistent gateway token or encourage unsafe token sharing.

Mitigation: Back up or verify any existing gateway token before changing it, use only the intended token from trusted local configuration, avoid the hardcoded example value, set restrictive file permissions, and do not paste token or API key contents into chat.

## Reference(s):

- [ACP Bridge Config Reference](references/acp-bridge-config-reference.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include diagnostic steps, configuration examples, and token-file handling guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
