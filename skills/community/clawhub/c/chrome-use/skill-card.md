## Description:

Automates browser tasks in the user's real, logged-in Chrome and returns information from web pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leeguooooo](https://clawhub.ai/user/leeguooooo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can use the skill to search, read, and verify live web pages, or carry out browser workflows such as form entry and web-app testing using an existing Chrome session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends automatically running changeable installation scripts and provides updates that may affect other installed tools.

Mitigation: Review and verify a fixed release before installing; limit updates to chrome-use unless you explicitly intend to update the wider tool family.

Risk: Browser automation can access accounts available in the active Chrome profile and may perform consequential actions.

Mitigation: Use a profile containing only accounts the agent should access, and explicitly authorize consequential account actions.

## Reference(s):

- [Chrome Use on ClawHub](https://clawhub.ai/leeguooooo/skills/chrome-use)
- [Publisher profile](https://clawhub.ai/user/leeguooooo)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Browser-derived results]

**Output Format:** [Natural-language instructions and text or structured results from browser tasks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results vary by task and may include extracted page content or screenshots.]

## Skill Version(s):

1.0.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
