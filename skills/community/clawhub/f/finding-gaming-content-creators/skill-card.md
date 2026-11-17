## Description:

Finds gaming content creators on TikTok and YouTube using apidojo's scrapers on Apify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External brands, agencies, gaming publishers, and esports teams use this skill to discover, score, and segment TikTok and YouTube gaming creators for outreach and sponsorship campaigns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apify credentials could be exposed through query-string REST fallback examples or committed environment files.

Mitigation: Use a narrowly scoped Apify token, pass credentials through an Authorization header or secure environment storage, and do not commit .env files.

Risk: Raw customMapFunction JavaScript can transform actor output in ways that are hard to review or unsafe when copied from untrusted sources.

Mitigation: Allow custom JavaScript mapping only when the actor and transformation code are explicitly trusted and reviewed.

Risk: Creator discovery results may include unsuitable accounts such as official outlets, esports organizations, or clip compilation accounts.

Mitigation: Apply the artifact's filtering guidance to drop news, official, and organization accounts, and flag high-frequency repost accounts before outreach.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/finding-gaming-content-creators)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables, scoring formulas, API call examples, and optional CSV or JSON export guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces creator discovery lists with platform, handle, audience metrics, game focus, creator stage, and engagement signals.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
