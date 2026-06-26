## Description: <br>
Allows agents to log, list, search, and manage developer journal entries for projects using dev-log-cli in a structured SQLite database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CrimsonDevil333333](https://clawhub.ai/user/CrimsonDevil333333) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and coding agents use this skill to maintain project journals, record milestones and blockers, and retrieve recent or searchable development context across work sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores persistent project journal entries that may be reused as project memory. <br>
Mitigation: Do not log secrets, credentials, customer data, private security details, or sensitive internal reasoning; periodically review and remove entries that should not persist. <br>
Risk: The setup flow installs dev-log-cli from an external package source. <br>
Mitigation: Install only when the dev-log-cli package source is trusted and review the installed package according to local supply-chain policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CrimsonDevil333333/devlog-agent-skill) <br>
- [dev-log-cli on PyPI](https://pypi.org/project/dev-log-cli/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides agents to create and query local SQLite-backed developer journal entries through dev-log-cli.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
