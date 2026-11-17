## Description:

Run Apify Actors, manage tasks, inspect datasets and key-value stores, and review usage via the Apify API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to automate Apify web scraping workflows, coordinate Actor and task runs, inspect run outputs, and manage datasets, key-value stores, request queues, schedules, logs, and usage from an agent chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill routes Apify API access through the ClawLink plugin and hosted service, which handles connected Apify credentials.

Mitigation: Install only if the user trusts ClawLink, use a narrowly scoped and revocable Apify token, and revoke the integration when it is no longer needed.

Risk: Actor runs and other Apify write operations can change account state or incur compute costs.

Mitigation: Preview and confirm the target resource and intended effect before write, delete, or run operations, and monitor Apify usage and billing.

Risk: The ClawLink plugin is installed without a pinned version in the artifact instructions.

Mitigation: Review the installed plugin before deployment and re-check security posture after plugin updates.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/apify-actors)
- [Publisher Profile](https://clawhub.ai/user/hith3sh)
- [Apify API Documentation](https://docs.apify.com/api/v2)
- [Apify Platform](https://apify.com/)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=apify-actors)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include previews before write operations, paginated retrieval guidance for large datasets, and operational error-handling steps.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
