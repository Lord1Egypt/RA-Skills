## Description: <br>
Engramai helps AI agents add, recall, and manage local memories using ACT-R activation, Hebbian learning, and cognitive consolidation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shing19](https://clawhub.ai/user/shing19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use Engramai to give agents persistent local memory for user preferences, important facts, procedural knowledge, feedback signals, and prior-context recall. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can keep persistent local memory about users and projects, which may accumulate sensitive personal or operational details over time. <br>
Mitigation: Use explicit save and recall rules, avoid secrets and sensitive personal data, and review stored memories periodically. <br>
Risk: Local memory data may be lost, stale, or over-pruned if the database location and maintenance behavior are not managed. <br>
Mitigation: Know where the database is stored, back it up before pruning or consolidation changes, and run maintenance deliberately. <br>
Risk: The installed engramai package behavior may change across releases. <br>
Mitigation: Pin the reviewed engramai package version for deployments that need reproducible behavior. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shing19/engramai) <br>
- [PyPI Package](https://pypi.org/project/engramai/) <br>
- [Engramai Usage Docs](https://github.com/tonitangpotato/neuromemory-ai/blob/main/docs/USAGE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline Python, shell, and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May involve local SQLite memory storage through the engramai package and optional MCP server configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
