## Description: <br>
Query GitHub event data via ClickHouse for supply chain investigations, actor profiling, anomaly detection, and incident timeline reconstruction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1aN0rmus](https://clawhub.ai/user/1aN0rmus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security engineers, incident responders, and developers use this skill to generate ClickHouse queries against public GitHub event data for supply chain investigations, actor profiling, tag or release tampering checks, and incident timeline reconstruction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A review helper may run nested tooling with broad filesystem access and approvals bypassed. <br>
Mitigation: Review the helper before use and prefer --no-yolo or disable automatic review and test execution unless that behavior is explicitly intended. <br>
Risk: Queries are sent to ClickHouse's public playground. <br>
Mitigation: Use only public GitHub event data and avoid placing private repository details, credentials, or sensitive incident notes in shared queries. <br>


## Reference(s): <br>
- [GitHub Events Full Schema](references/schema.md) <br>
- [ClickHouse GitHub Events Dataset](https://ghe.clickhouse.tech/) <br>
- [ClickHouse Public Playground](https://play.clickhouse.com/?user=play) <br>
- [Trivy Supply Chain Compromise Investigation](https://socket.dev/blog/trivy-under-attack-again-github-actions-compromise) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown with SQL and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public GitHub event data queried through ClickHouse endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
