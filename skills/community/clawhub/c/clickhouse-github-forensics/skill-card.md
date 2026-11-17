## Description:

Query public GitHub event data through ClickHouse for supply chain investigations, actor profiling, anomaly detection, and incident timeline reconstruction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1an0rmus](https://clawhub.ai/user/1an0rmus)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security engineers, and incident responders use this skill to investigate public GitHub activity, reconstruct supply chain incident timelines, profile actors, and check for tag or release tampering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository names, usernames, dates, and other investigation terms are sent to ClickHouse's public playground.

Mitigation: Avoid private incident details, secrets, and confidential identifiers unless sharing them with the public playground is acceptable.

Risk: The skill only queries GitHub's public event stream and cannot access private repository data or raw event payloads.

Mitigation: Use it for public-event timeline and activity analysis, and corroborate conclusions with private logs or repository audit data when available.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/1an0rmus/skills/clickhouse-github-forensics)
- [ClickHouse Public GitHub Events Dataset](https://ghe.clickhouse.tech/)
- [GitHub Events Schema](references/schema.md)
- [Trivy Supply Chain Compromise Investigation](https://socket.dev/blog/trivy-under-attack-again-github-actions-compromise)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands]

**Output Format:** [Markdown guidance with SQL queries and curl command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public GitHub event data and sends query terms to ClickHouse's public playground.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
