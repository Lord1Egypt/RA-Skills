## Description:

Start a Claude Code remote control session in tmux with bypass permissions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oobagi](https://clawhub.ai/user/oobagi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to launch, list, send tasks to, stop, and resume headless Claude Code remote-control sessions for a target project. It is intended for workflows where persistent tmux-backed Claude sessions and remote session URLs are deliberately required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote Claude Code sessions run without normal permission prompts and expose a session URL that enables remote control.

Mitigation: Install only when remote control is deliberately required, treat session URLs as secrets, and prefer a sandboxed account or container.

Risk: The skill persists workspace trust for the target project directory.

Mitigation: Use it only with directories you intentionally trust, and avoid untrusted repositories or sensitive home-directory workspaces.

Risk: Security evidence identifies unsafe resume UUID handling until command construction is fixed.

Mitigation: Do not pass resume UUIDs from untrusted text.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/oobagi/skills/awesome-remote-control)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Awesome Remote Control repository link from artifact README](https://github.com/oobagi/awesome-remote-control.git)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands, session status text, and remote-control URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires tmux, python3, and claude. Sessions auto-close after 30 minutes idle and maintain local session registry state.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
