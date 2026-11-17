## Description:

Neuroscience-grounded memory for AI agents. Add, recall, and manage memories with ACT-R activation, Hebbian learning, and cognitive consolidation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shing19](https://clawhub.ai/user/shing19)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use Engramai to add local cognitive memory to AI agents, including storing and recalling preferences, facts, procedural knowledge, feedback, and consolidation state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing an unpinned package version may introduce unexpected behavior or dependency changes.

Mitigation: Install in a virtual environment and pin and review the engramai package version where possible.

Risk: The local memory database may store personal data, preferences, operational details, or secrets if agents save them.

Mitigation: Protect the memory database and avoid storing secrets or sensitive personal data unless explicitly intended.

Risk: Scheduled forgetting or pruning can remove useful memories if thresholds are too aggressive.

Mitigation: Keep backups and define clear retention thresholds before scheduling automatic forget operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shing19/skills/engramai)
- [PyPI package](https://pypi.org/project/engramai/)
- [npm package](https://www.npmjs.com/package/neuromemory-ai)
- [Project repository](https://github.com/tonitangpotato/neuromemory-ai)
- [Usage documentation](https://github.com/tonitangpotato/neuromemory-ai/blob/main/docs/USAGE.md)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with Python, bash, and YAML snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes CLI, MCP server, and package installation guidance for local SQLite-backed memory use.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
