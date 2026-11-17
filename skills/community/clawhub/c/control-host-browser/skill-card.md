## Description:

Controls the host machine's Chrome browser to open specific URLs in new tabs when the user explicitly asks to open or search for a page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevenxie66](https://clawhub.ai/user/stevenxie66)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to open user-requested HTTP/HTTPS links or search pages in the host Chrome browser for local viewing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can open pages in a real Chrome browser through a DevTools port, potentially using a signed-in browser profile.

Mitigation: Review requested destinations before execution and enable the skill only for trusted agents and users.

Risk: Security evidence says the skill gives host-browser navigation power without enforcing the promised URL limits.

Mitigation: Add URL scheme and destination validation before enabling the skill broadly.

Risk: The skill depends on a host Chrome remote debugging port being available.

Mitigation: Restrict the debugging port to the expected local environment and avoid exposing it to untrusted networks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stevenxie66/skills/control-host-browser)
- [Publisher profile](https://clawhub.ai/user/stevenxie66)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and command output strings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces host-browser navigation instructions and reports tab creation or CDP error output.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
