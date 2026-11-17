## Description:

chrome-cdp lets agents connect to open Chrome tabs through the Chrome DevTools Protocol to inspect pages and perform browser actions in the user's active session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adminlove520](https://clawhub.ai/user/adminlove520)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to let an agent inspect open Chrome tabs, capture page state, and perform controlled browser actions against a live Chrome session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access and control live, logged-in Chrome tabs, which may expose sensitive account data or perform unintended browser actions.

Mitigation: Use a separate Chrome profile with no sensitive accounts where possible, and require explicit approval before clicks, typing, navigation, screenshots, or JavaScript evaluation.

Risk: Security evidence reports unsafe installation and command execution patterns.

Mitigation: Review and pin the external chrome-cdp code, and fix shell command construction before installing or running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adminlove520/skills/chrome-cdp)
- [Publisher profile](https://clawhub.ai/user/adminlove520)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, Files]

**Output Format:** [JSON-like JavaScript objects, text output, and screenshot files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 22+, Chrome remote debugging, and an installed chrome-cdp script.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
