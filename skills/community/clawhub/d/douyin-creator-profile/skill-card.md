## Description:

This skill lets agents query public Douyin creator, content, hot-list, and comment data for short-video research, competitor monitoring, trend tracking, and content analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to retrieve structured public Douyin search results, hot-list entries, creator posts, and video comments for marketing analysis, social listening, and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Douyin search terms, creator or video URLs, and the Guaikei API token to guaikei.com.

Mitigation: Install only when that third-party data flow is acceptable, keep the API token secret, and rotate the token if it may have been exposed.

Risk: The skill automatically saves collected Douyin data locally, including public user identifiers, comments, IP-region labels, and analysis targets.

Mitigation: Protect or clean the generated logs directory, and avoid sharing logs without review and any needed redaction.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/why20261/douyin-creator-profile)
- [ClawHub skill page](https://clawhub.ai/why20261/skills/douyin-creator-profile)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON on stdout with operational logs on stderr]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and may save collected Douyin data to a local logs directory.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
