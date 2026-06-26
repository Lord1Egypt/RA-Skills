## Description: <br>
Daily Backup helps an agent inspect its Git workspace for changes and decide whether to commit and push a daily backup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axelhu](https://clawhub.ai/user/axelhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to keep an agent workspace backed up in Git on a daily schedule or on demand. It checks workspace state first so the agent can review pending changes before committing and pushing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can support committing and pushing the agent workspace to a Git remote. <br>
Mitigation: Set AGENT_WORKSPACE explicitly, review changed files and .gitignore for secrets before committing, and confirm the Git remote and SSH credentials point to a destination the user controls. <br>


## Reference(s): <br>
- [Daily Backup ClawHub Page](https://clawhub.ai/axelhu/daily-backup) <br>
- [Remote Repo Creation Guide](references/spec.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration guidance] <br>
**Output Format:** [Markdown report with shell command guidance and status strings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The pre-flight script emits NOT_GIT_REPO, NO_CHANGES, or HAS_CHANGES with change counts.] <br>

## Skill Version(s): <br>
1.9.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
