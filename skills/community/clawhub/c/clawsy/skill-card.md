## Description:

Clawsy is a native macOS companion app that gives an OpenClaw agent access to the user's Mac through screenshots, clipboard, camera, files, location, and live Mission Control over WebSocket with SSH fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iret77](https://clawhub.ai/user/iret77)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Clawsy to let an OpenClaw agent interact with a user's macOS environment for visual context, clipboard exchange, camera input, sandboxed shared-folder file transfer, location lookup, and progress reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The companion app and connected agents can access sensitive Mac data such as screenshots, camera images, clipboard contents, files, and location.

Mitigation: Install only when that access is acceptable, use the app permission prompts deliberately, and limit the shared folder to files intended for agent access.

Risk: Gateway setup details and authentication tokens may be exposed during pairing or setup.

Mitigation: Avoid sharing long-lived tokens, rotate credentials when exposure is possible, and verify the app download through a trusted release or signature path.

Risk: Automatic location or file actions can disclose data without additional context once configured.

Mitigation: Disable or avoid automatic location and file actions where possible, and remove propagation or heartbeat rules that are not explicitly desired.

## Reference(s):

- [Clawsy Skill Page](https://clawhub.ai/iret77/skills/clawsy)
- [Clawsy GitHub Repository](https://github.com/iret77/clawsy)
- [Clawsy Latest Release](https://github.com/iret77/clawsy/releases/latest)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands, Python snippets, setup instructions, and command reference tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include setup codes, node commands, Mission Control status messages, and file-transfer guidance for a connected macOS companion app.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
