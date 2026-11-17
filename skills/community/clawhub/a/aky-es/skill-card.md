## Description:

AKY-ES helps agents store, index, search, and retrieve persistent data with Elasticsearch 8.17, prioritizing localhost:9200 and falling back to Elastic Cloud when configured.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangfromchu-ai](https://clawhub.ai/user/wangfromchu-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use AKY-ES to maintain searchable long-term memory, index documents and skill outputs, run CRUD and search operations, and bulk import JSONL records into an Elasticsearch-backed store.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent searchable storage may retain sensitive material.

Mitigation: Avoid storing sensitive data unless retention, access, deletion, and review expectations are acceptable.

Risk: The skill presents local Elasticsearch usage while also allowing automatic Elastic Cloud fallback.

Mitigation: Disable cloud fallback or require explicit destination confirmation before indexing or searching data.

Risk: The skill depends on unaudited external workspace scripts and a keepalive cron job.

Mitigation: Review the scripts before installing, pin dependencies, and approve any cron or keepalive behavior.

## Reference(s):

- [Elasticsearch Reference](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [ClawHub Skill Page](https://clawhub.ai/wangfromchu-ai/skills/aky-es)
- [Publisher Profile](https://clawhub.ai/user/wangfromchu-ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell, Python, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May interact with persistent Elasticsearch storage through external workspace scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
