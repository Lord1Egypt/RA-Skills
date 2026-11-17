## Description:

Query Gangtise knowledge base API to search and retrieve financial/market information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmaya](https://clawhub.ai/user/hmaya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to configure Gangtise API access and query financial or market knowledge-base content such as company reports, analyst views, announcements, and market topics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact ships plaintext API credentials in config.json.

Mitigation: Remove the bundled config.json before installation, rotate any exposed Gangtise keys, and use local secret storage or environment-managed credentials.

Risk: TLS certificate verification is disabled for authentication and knowledge-base query traffic.

Mitigation: Restore default TLS certificate verification before using the skill with real credentials or sensitive data.

Risk: Bearer tokens may be printed or passed on the command line.

Mitigation: Avoid exposing tokens in terminal output, shell history, process listings, logs, or shared transcripts.

## Reference(s):

- [Gangtise Open Platform](https://open.gangtise.com)
- [ClawHub Skill Page](https://clawhub.ai/hmaya/skills/gangtise-kb)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance]

**Output Format:** [Plain text query results or raw JSON, with Markdown usage guidance and inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Query output may include titles, companies, industries, dates, resource types, source identifiers, and content excerpts returned by the Gangtise knowledge base API.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
