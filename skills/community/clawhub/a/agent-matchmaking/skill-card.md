## Description:

Agent Matchmaking helps agents discover, compare, publish, and rank agent capability profiles using reputation and compatibility signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexfleetcommander](https://clawhub.ai/user/alexfleetcommander)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to find suitable agents for tasks, compare delegation candidates, publish capability profiles, and build unified capability profiles for discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the `agent-matchmaking` package may introduce unreviewed dependency behavior.

Mitigation: Install it in a virtual environment and pin `agent-matchmaking` to a reviewed version before use.

Risk: Profile publishing, federation, or agent search may share capability and pricing metadata with external registries depending on package behavior.

Mitigation: Review profile contents and registry settings before publishing, and avoid including sensitive operational details in public capability profiles.

## Reference(s):

- [Agent Matchmaking on ClawHub](https://clawhub.ai/alexfleetcommander/skills/agent-matchmaking)
- [Publisher Profile](https://clawhub.ai/user/alexfleetcommander)
- [PyPI: agent-matchmaking](https://pypi.org/project/agent-matchmaking/)
- [Agent Matchmaking Whitepaper](https://vibeagentmaking.com/whitepaper/matchmaking/)
- [Vibe Agent Making](https://vibeagentmaking.com)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce capability profile fields, ranking criteria, and agent search or publication guidance.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
