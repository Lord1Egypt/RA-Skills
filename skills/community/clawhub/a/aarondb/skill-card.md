## Description: <br>
Distributed Datalog engine for sovereign agents that provides persistent fact management, querying, reasoning, and optional synchronization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[criticalinsight](https://clawhub.ai/user/criticalinsight) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add local or distributed Datalog-backed fact storage and querying to agents that need persistent, immutable state and reasoning over stored facts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent fact storage and optional synchronization can retain or share sensitive, credential-like, or unreviewed facts. <br>
Mitigation: Decide what facts are safe to persist or synchronize, and avoid storing secrets, credentials, or unreviewed instructions as reusable database facts. <br>
Risk: The skill depends on an external npm package and referenced repository that should be trusted before installation. <br>
Mitigation: Verify the npm package and repository before installing, and pin a trusted package version. <br>


## Reference(s): <br>
- [Aarondb ClawHub page](https://clawhub.ai/criticalinsight/aarondb) <br>
- [@criticalinsight/aarondb-edge npm package](https://www.npmjs.com/package/@criticalinsight/aarondb-edge) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes guidance for persistent fact storage and optional synchronization.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
