## Description:

Browsex guides an agent using OpenClaw browser controls to read X/Twitter content and, when authenticated, perform account actions such as posting, liking, reposting, replying, searching, and following.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coding-commits](https://clawhub.ai/user/coding-commits)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to have an agent navigate X/Twitter in a browser for profile viewing, tweet lookup, search, timeline reading, and authenticated account actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated use can let an agent perform visible X/Twitter account actions such as posting, liking, reposting, replying, or following.

Mitigation: Use read-only browsing by default and require explicit final confirmation before any account action.

Risk: Browser UI changes or stale element references can cause the agent to act on the wrong X/Twitter control.

Mitigation: Take a fresh browser snapshot before each action and verify the target account, tweet, and control before clicking.

## Reference(s):

- [ClawHub browsex skill page](https://clawhub.ai/coding-commits/skills/browsex)

## Skill Output:

**Output Type(s):** [guidance, configuration, browser commands]

**Output Format:** [Markdown with browser command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only browsing can work without login; posting, liking, reposting, replying, timeline reading, and following require an authenticated X/Twitter browser session.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
