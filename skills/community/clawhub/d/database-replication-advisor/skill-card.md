## Description:

Analyze database replication topology, detect lag, and recommend replication strategy based on CAP tradeoffs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Database and platform engineers use this skill to assess replication health, investigate lag and conflicts, evaluate failover readiness, and design replication topologies with CAP tradeoff analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live database and cloud failover commands could disrupt production or change replication state if executed without review.

Mitigation: Require operator review, explicit approval, and change-management controls before any failover, promotion, rewind, or AWS RDS failover command.

Risk: Assessment probes may run against production databases with credentials that are broader than needed.

Mitigation: Use least-privilege credentials and run probes in non-production or only with explicit production approval.

Risk: Command examples may expose database passwords when passed directly on the command line.

Mitigation: Use approved secret handling such as protected client configuration or a secret manager, and avoid command-line database passwords.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/database-replication-advisor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports and runbooks with inline SQL, bash, Python, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operator-reviewed database assessment, topology recommendation, and failover guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
