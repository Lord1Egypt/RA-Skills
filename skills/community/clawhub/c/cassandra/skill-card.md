## Description:

Design Cassandra tables, write efficient queries, and avoid distributed database pitfalls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and database operators use this skill for Cassandra data modeling, query design, consistency choices, and operational guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Operational Cassandra advice such as repairs, schema changes, or rolling restarts can affect production availability and data consistency if applied without review.

Mitigation: Review recommendations against the target cluster topology, operational runbooks, and change-management safeguards before applying them.

Risk: The skill requires external Cassandra administration tools such as cqlsh or nodetool for users who choose to act on the guidance.

Mitigation: Use normal access controls, least-privilege credentials, and environment-specific validation before running any Cassandra commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/cassandra)
- [ClawHub publisher profile](https://clawhub.ai/user/ivangdavila)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown with inline Cassandra and nodetool command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory text only; no executable code is included in the artifact.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
