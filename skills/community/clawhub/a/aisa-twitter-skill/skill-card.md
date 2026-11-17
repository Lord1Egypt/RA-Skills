## Description:

Searches and reads X (Twitter) profiles, timelines, mentions, followers, tweet search, trends, lists, communities, and Spaces, and publishes posts after the user completes OAuth in the browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bowen-dotcom](https://clawhub.ai/user/bowen-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to search, monitor, and analyze Twitter/X activity and to publish text or media posts through an OAuth-authorized account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured AIsa API key can appear in normal command output or logs.

Mitigation: Use only an AIsa key approved for this workflow, avoid sharing command output containing secrets, and remove API key fields from outputs before routine use.

Risk: Posting traffic can be redirected through a custom TWITTER_RELAY_BASE_URL.

Mitigation: Leave the default relay URL in place unless the destination is a trusted HTTPS host approved for the intended account and data.

Risk: Monitoring terms, tweet content, media files, and account actions may be sensitive or business-confidential.

Mitigation: Avoid confidential search terms and posting workflows unless the provider and destination service are approved for that data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bowen-dotcom/skills/aisa-twitter-skill)
- [OpenClaw Twitter OAuth posting workflow](references/post_twitter.md)
- [AIsa API Reference](https://docs.aisa.one/reference/)
- [OpenClaw homepage](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown guidance with shell commands, Python client commands, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY; posting requires browser OAuth authorization; media posting accepts local image or video file paths.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
