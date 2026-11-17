## Description:

Search prospects, accounts, contacts, and outreach data in Apollo.io via the Apollo API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, growth, and CRM users use this skill to find leads, enrich company and contact data, manage Apollo sequences, and update CRM records through a connected Apollo account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and allowlist an unpinned third-party plugin that can proxy Apollo reads and writes.

Mitigation: Review the ClawLink plugin publisher, version, and permissions before installing or allowlisting it.

Risk: ClawLink stores or proxies Apollo API access for the connected account.

Mitigation: Use the skill only when the user accepts ClawLink handling Apollo credentials and API access.

Risk: Apollo write operations can create, update, delete, or sequence CRM records.

Mitigation: Preview and explicitly confirm the target resource and intended effect before any write or destructive operation.

Risk: Apollo enrichment and search operations may consume Apollo credits or hit rate limits.

Mitigation: Confirm large or bulk operations before running them and respect retry guidance for rate-limited calls.

## Reference(s):

- [Apollo API Documentation](https://apolloio.github.io/apollo-api-docs/)
- [Apollo Contact Search API](https://apolloio.github.io/apollo-api-docs/#search-contacts)
- [Apollo Organization Enrichment](https://apolloio.github.io/apollo-api-docs/#organization-enrichment)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Configuration]

**Output Format:** [Markdown with inline bash commands and JSON tool parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the live Apollo tool catalog and connected-account context when available.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
