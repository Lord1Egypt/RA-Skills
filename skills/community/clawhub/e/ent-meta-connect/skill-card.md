## Description:

Helps users connect Meta Ads by validating an access token, saving connection settings, and checking ad account read access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thinhbuiii](https://clawhub.ai/user/thinhbuiii)

### License/Terms of Use:

MIT-0

## Use Case:

Meta Ads account owners use this skill to connect an agent to their ad account without manually editing configuration. The agent validates the provided token, saves connection settings, restarts the gateway, and checks read access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An access token pasted into chat or stored in gateway settings may be exposed.

Mitigation: Accept tokens only from the machine or account owner, keep them out of replies and logs, and rotate a token if it was exposed or is no longer needed.

Risk: Updating connection settings and restarting the gateway can affect the owner's running agent.

Mitigation: Confirm the request comes from the owner before making changes, preserve existing settings, and disclose the restart.

## Reference(s):

- [ENT Meta Connect on ClawHub](https://clawhub.ai/thinhbuiii/skills/ent-meta-connect)
- [Meta Graph API Explorer](https://developers.facebook.com/tools/explorer/)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports token validity and ad account read access without repeating the token.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
