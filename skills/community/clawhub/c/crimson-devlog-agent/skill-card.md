## Description: <br>
A standardized journaling skill for OpenClaw agents to track progress, tasks, and project status using dev-log-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CrimsonDevil333333](https://clawhub.ai/user/CrimsonDevil333333) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw agents use this skill to keep structured project journals, task status, milestones, blockers, and searchable project context in dev-log-cli. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup script may install pipx and the current dev-log-cli package from PyPI. <br>
Mitigation: Review installation behavior before running setup.sh and install only in environments where Python user-level tooling and PyPI packages are acceptable. <br>
Risk: Developer logs may contain secrets, tokens, customer data, or confidential project details in a local SQLite database. <br>
Mitigation: Avoid logging sensitive data unless storage location, retention, and removal procedures are understood. <br>


## Reference(s): <br>
- [dev-log-cli GitHub repository](https://github.com/CrimsonDevil333333/dev-log-cli) <br>
- [dev-log-cli on PyPI](https://pypi.org/project/dev-log-cli/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents to use devlog commands that create, list, search, view, edit, and summarize local developer log entries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
