## Description:

Interact with the system clipboard (text only) using `xclip` from any OpenClaw session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xejrax](https://clawhub.ai/user/xejrax)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to ask an agent to copy text or file contents to the Linux system clipboard and read text from it using xclip.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can read from and write to the text clipboard when the skill is invoked, and clipboard or copied file contents may contain sensitive data.

Mitigation: Review what is copied or pasted, avoid invoking the skill with sensitive clipboard contents, and clear the clipboard after sensitive use.

Risk: The install guidance uses sudo to install xclip through dnf.

Mitigation: Install xclip only from trusted configured dnf repositories and review package installation before granting elevated access.

## Reference(s):

- [ClawHub Clipboard skill page](https://clawhub.ai/xejrax/skills/clipboard)
- [ClawHub publisher profile](https://clawhub.ai/user/xejrax)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Text-only clipboard operations; requires xclip on Linux.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
