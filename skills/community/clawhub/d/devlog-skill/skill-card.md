## Description: <br>
A standardized journaling skill for OpenClaw agents to track progress, tasks, and project status using dev-log-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CrimsonDevil333333](https://clawhub.ai/user/CrimsonDevil333333) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to record project progress, blockers, milestones, task status, and searchable development context through dev-log-cli. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup script may install Python tooling and dev-log-cli from PyPI. <br>
Mitigation: Review setup.sh and install only in environments where PyPI package installation through pip or pipx is acceptable. <br>
Risk: Developer log entries may become persistent local records and could contain sensitive information. <br>
Mitigation: Avoid logging secrets, credentials, customer data, sensitive incident details, or confidential project information unless storage, deletion, and redaction behavior has been verified. <br>


## Reference(s): <br>
- [Devlog Skill on ClawHub](https://clawhub.ai/CrimsonDevil333333/devlog-skill) <br>
- [dev-log-cli GitHub repository](https://github.com/CrimsonDevil333333/dev-log-cli) <br>
- [dev-log-cli on PyPI](https://pypi.org/project/dev-log-cli/) <br>
- [pipx installation guidance](https://github.com/pypa/pipx#install-pipx) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are intended for local dev-log-cli usage and may create persistent local journal entries.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
