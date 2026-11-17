## Description:

Lifecycle management for autonomous AI agents - birth, forking, succession, migration, retirement - with genealogy tracking, reputation inheritance, and identity continuity across agent evolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexfleetcommander](https://clawhub.ai/user/alexfleetcommander)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to register agent births, record forks, process retirement and succession, and inspect genealogy for autonomous agents. It helps maintain lifecycle records and identity continuity as agents evolve.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup uses an unpinned pip package install.

Mitigation: Install in a virtual environment and pin or review the agent-lifecycle-protocol package before use.

Risk: The skill can create or update local lifecycle JSONL records in the working directory.

Mitigation: Run it in the intended project directory and review lifecycle record changes before committing or sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexfleetcommander/skills/agent-lifecycle-protocol)
- [Publisher profile](https://clawhub.ai/user/alexfleetcommander)
- [PyPI package](https://pypi.org/project/agent-lifecycle-protocol/)
- [Agent Lifecycle Protocol whitepaper](https://vibeagentmaking.com/whitepaper/lifecycle-protocol/)
- [Vibe Agent Making](https://vibeagentmaking.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation or updates of local lifecycle JSONL records in the working directory.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
