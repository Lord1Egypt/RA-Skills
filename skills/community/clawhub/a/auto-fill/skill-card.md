## Description:

Reads the current page's form structure through Chrome Debug Protocol (CDP), matches user-provided data to fields, fills the form, and returns a screenshot for confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scottliu007](https://clawhub.ai/user/scottliu007)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to fill web forms in a real Chrome session from free-form user input. The agent identifies and fills fields while the user remains responsible for navigation clicks, CAPTCHA handling, and final submission unless explicitly delegated.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can start and control a real Chrome debug session, which may expose logged-in browser state or sensitive page data.

Mitigation: Use a pinned and reviewed MCP package, run the skill in a dedicated temporary browser profile, require explicit approval before launching Chrome or navigating, and close the debug browser with temporary data cleaned up after use.

Risk: Automatic field matching and navigation can place user-provided data into the wrong form or page when labels are ambiguous.

Mitigation: Ask for user confirmation on uncertain fields, passwords, file uploads, and submission actions, and rely on screenshot confirmation before the user submits the form.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scottliu007/skills/auto-fill)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct browser actions through Chrome Debug Protocol and may return screenshot confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
