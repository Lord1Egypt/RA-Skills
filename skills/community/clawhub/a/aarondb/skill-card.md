## Description:

Distributed Datalog engine guidance for sovereign agents, enabling persistent fact management, querying, reasoning, and synchronization patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[criticalinsight](https://clawhub.ai/user/criticalinsight)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to help agents install and apply AaronDB Edge for immutable Datalog fact storage, retrieval, reasoning, and cross-agent synchronization workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned external npm package, so install-time behavior may change as the package evolves.

Mitigation: Pin and review the @criticalinsight/aarondb-edge package version before installation, preferably in a least-privileged environment.

Risk: Persisted or synchronized facts may contain sensitive, stale, or incorrect agent state.

Mitigation: Be deliberate about which facts are stored or synchronized, review persisted data, and apply appropriate access controls for shared back ends.

## Reference(s):

- [Aarondb on ClawHub](https://clawhub.ai/criticalinsight/skills/aarondb)
- [@criticalinsight/aarondb-edge npm package](https://www.npmjs.com/package/@criticalinsight/aarondb-edge)
- [aarondb-edge repository](https://github.com/criticalinsight/aarondb-edge)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JavaScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides use of an external npm package and Datalog fact-management patterns.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
