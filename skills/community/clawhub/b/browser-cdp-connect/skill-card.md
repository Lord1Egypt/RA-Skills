## Description:

Connects an agent's browser tooling to a user's regular Chrome profile through Chrome DevTools Protocol when headless browsing is blocked.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuancaoyaohw](https://clawhub.ai/user/yuancaoyaohw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and browser-automation users use this skill to switch an agent from a default headless browser to a Chrome profile with the user's existing session state. It is intended for authorized browsing tasks where headless automation is blocked and the user intentionally wants agent control of their browser profile.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting to a logged-in Chrome profile can expose accounts, cookies, tabs, and browser actions to the agent.

Mitigation: Use a dedicated Chrome profile with only the minimum needed accounts and avoid email, financial, admin, or identity-provider sessions.

Risk: Agent browser control can act through the user's authenticated sessions.

Mitigation: Confirm each use, close tabs created by the agent, and clear browser.cdp_url immediately after the task.

Risk: The skill can be misused to bypass access controls or site rules.

Mitigation: Use it only for browsing or collection tasks the user is authorized to perform and do not use it to evade rules or controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuancaoyaohw/skills/browser-cdp-connect)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces commands and setup guidance for connecting or clearing a Chrome CDP endpoint.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
