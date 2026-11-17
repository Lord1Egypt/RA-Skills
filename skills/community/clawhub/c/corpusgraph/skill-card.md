## Description:

Document ETL, entity extraction, and relationship graphing engine. Convert 1,000+ file formats into searchable, structured data with automatic entity and relationship mapping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aingestigate](https://clawhub.ai/user/aingestigate)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use CorpusGraph to ingest document collections, convert varied file formats into searchable structured data, extract entities, and query relationship evidence across a corpus.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches a mutable remote agent guide using the user's token.

Mitigation: Treat the remote guide as reference material only and keep the local skill safety constraints authoritative.

Risk: A misconfigured API base URL could point the agent at an untrusted host.

Mitigation: Configure INGESTIGATE_BASE_URL only through trusted platform settings and avoid arbitrary or user-supplied hosts.

Risk: The skill can search, read, upload, and process corpus data within the user's token permissions.

Mitigation: Install only for trusted Ingestigate deployments and rely on organization-scoped permissions and audit trails for operational control.

Risk: The access token is short-lived and may expire during use.

Mitigation: When a 401 response occurs, generate a new token through the documented Ingestigate flow and update secure platform settings.

## Reference(s):

- [CorpusGraph homepage](https://ingestigate.com/corpusgraph)
- [CorpusGraph ClawHub release](https://clawhub.ai/aingestigate/skills/corpusgraph)
- [Ingestigate platform](https://ingestigate.com)
- [Authenticated API guide](https://app1.ingestigate.com/api/agent/guide)
- [Skill README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration guidance]

**Output Format:** [Markdown with API endpoint descriptions and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be grounded in API responses and must call out incomplete corpus processing when readiness signals indicate it.]

## Skill Version(s):

1.0.4 (source: server release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
