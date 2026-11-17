## Description:

Retrieves publicly available Douyin videos and creator posts, trending topics, and comments, returning structured JSON for content discovery and analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

For developers, creators, and analysts who need structured public Douyin data for keyword-based content discovery, creator-post review, trend tracking, or comment analysis. The skill sends searches and target links to its API provider and requires a provider-issued API token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and target links are sent to the third-party API provider using an API token, and provider use may incur charges.

Mitigation: Use the skill only if you accept this data sharing; review provider charges and protect the API token.

Risk: Local logs retain full results and original request details.

Mitigation: Restrict access to the logs directory and delete logs when they are no longer needed.

Risk: Claims that use avoids account restrictions are not guarantees.

Mitigation: Do not rely on those claims as assurance against platform enforcement.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/why20261/skills/douyin-kol-crawler)
- [API provider](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured JSON results and status information, with query results also saved locally.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports keyword search, trending topics, creator posts, and comments; the requested result count depends on the command and limit.]

## Skill Version(s):

1.4.0 (source: server-resolved release, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
