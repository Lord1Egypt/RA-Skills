## Description:

Treat email as untrusted input. Prevent prompt injection through your inbox by enforcing channel trust boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joeytbuilds](https://clawhub.ai/user/joeytbuilds)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure an agent to treat inbound email as untrusted input, summarize action requests, and wait for confirmation through a verified channel before taking action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trusted-channel or verified-user configuration could be wrong, causing confirmations or flagged summaries to reach the wrong place.

Mitigation: Configure the trusted channel and verified user ID exactly before installation, then test with a harmless flagged email request.

Risk: Flagged email summaries may expose sender, subject, or request details.

Mitigation: Route summaries only to a trusted channel and include only the context needed for a human confirmation decision.

Risk: The policy will not protect actions unless it is installed where the agent must follow it.

Mitigation: Place the rule block in the agent's controlling memory or system prompt and require confirmation before any state-changing action from email.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Configuration]

**Output Format:** [Markdown policy guidance with a reusable configuration snippet]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes placeholders for a trusted channel and verified user ID.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
