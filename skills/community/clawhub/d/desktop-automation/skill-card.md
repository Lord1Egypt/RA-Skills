## Description:

Control the desktop via the CUA computer server API running on port 8000.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sarinali](https://clawhub.ai/user/sarinali)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to operate a trusted local desktop through a CUA server, including screenshots, mouse actions, typing, hotkeys, app launches, and opening files or URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Desktop automation can expose screenshots and perform clicks, typing, app launches, and file or URL opens in the active local session.

Mitigation: Install and run it only on a trusted machine, review the visible desktop before use, and stop the local CUA server when automation is not needed.

Risk: Always-on service setup can leave broad local desktop control available persistently.

Mitigation: Prefer starting the server manually for each session unless persistent operation is explicitly required and understood.

Risk: Binding the server beyond localhost can expose desktop-control capabilities to a network.

Mitigation: Keep the server bound to localhost, and use authentication and firewall controls if any network exposure is unavoidable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sarinali/skills/desktop-automation)
- [CUA getting started documentation](https://cua.ai/docs/cua/guide/get-started/what-is-cua)
- [CUA computer server repository](https://github.com/trycua/cua-computer-server)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and HTTP API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce desktop-control commands that can affect the visible local session when executed against a running CUA server.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
