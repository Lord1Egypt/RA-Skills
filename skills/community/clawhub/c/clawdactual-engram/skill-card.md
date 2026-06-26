## Description: <br>
Build, query, and maintain persistent structured knowledge graphs for AI agents across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[morpheis](https://clawhub.ai/user/morpheis) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use Engram to persist local knowledge graphs for code architecture, service dependencies, organizations, infrastructure, and concepts so future sessions can query and update relationships. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill maintains a long-lived local knowledge graph that can persist sensitive operational, people, infrastructure, or relationship data across agent sessions. <br>
Mitigation: Avoid storing secrets, credential contents, private email details, sensitive relationship notes, or trust labels unless that persistence is explicitly intended. <br>
Risk: Export, import, and delete commands can expose, overwrite, or remove persisted graph data. <br>
Mitigation: Review the configured database path and exported files before sharing, importing, or deleting graph data. <br>
Risk: Stored graph entries can become stale and later mislead future agent sessions. <br>
Mitigation: Use the skill's verification, stale-checking, and git-diff workflows to refresh or remove outdated nodes and edges. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/morpheis/clawdactual-engram) <br>
- [Publisher profile](https://clawhub.ai/user/morpheis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local SQLite persistence at a configurable database path.] <br>

## Skill Version(s): <br>
0.1.10 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
