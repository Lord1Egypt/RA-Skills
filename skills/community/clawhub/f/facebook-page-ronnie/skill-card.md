## Description:

Facebook Page publishing and engagement skill for Ronnie's Page operations, including text and photo posting, permission testing, token diagnostics, and browser fallback when comment or reply APIs are blocked.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ronnine6527](https://clawhub.ai/user/ronnine6527)

### License/Terms of Use:

MIT-0

## Use Case:

External operators and developers use this skill to manage a Facebook Page through Graph API workflows, including publishing posts, checking Page token configuration, diagnosing permission failures, and falling back to browser automation for blocked engagement actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles powerful Facebook Page access tokens that can publish content publicly.

Mitigation: Use least-privilege tokens, avoid logged or shared token-generation environments, and redact API output that may contain credentials or sensitive Page data.

Risk: Live post, comment, reply, or browser-driven actions can affect a business-critical Facebook Page.

Mitigation: Review the skill before installation for business-critical Pages and require manual confirmation before any live publishing or engagement action.

Risk: Comment and reply workflows may fail when Page engagement permissions are missing, stale, or not approved.

Mitigation: Verify the required Page permissions and regenerate tokens after permission or app-mode changes before attempting engagement actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ronnine6527/skills/facebook-page-ronnie)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, API Calls, Configuration]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Graph API request examples, environment checks, token lifecycle guidance, permission diagnostics, and operational recommendations.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
