## Description:

Provides read-only Meta Ads reporting for Facebook and Instagram accounts through the Graph API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thinhbuiii](https://clawhub.ai/user/thinhbuiii)

### License/Terms of Use:

MIT-0

## Use Case:

Advertisers and analysts use this skill to retrieve account and campaign metrics, review trends and check token validity without changing ads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An access token could expose Meta Ads reporting data if shared or committed.

Mitigation: Use an ads_read-only token, keep it out of chats and commits, and rotate or remove it when no longer needed.

## Reference(s):

- [Meta Ads Report on ClawHub](https://clawhub.ai/thinhbuiii/skills/ent-meta-ads-report)
- [Meta Graph API Explorer](https://developers.facebook.com/tools/explorer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Concise narrative or bullet reports with optional curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only reporting; calculated metrics are identified separately from API values.]

## Skill Version(s):

1.0.3 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
