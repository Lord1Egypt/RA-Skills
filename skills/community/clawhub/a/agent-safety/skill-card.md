## Description: <br>
Outbound safety for autonomous AI agents that scans output before publication and provides local shell tools for pre-publish scanning, git pre-commit enforcement, and health checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[compass-soul](https://clawhub.ai/user/compass-soul) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and autonomous-agent operators use this skill to check files, staged git changes, and local workspace health before publishing or committing work. It is intended to reduce accidental release of secrets, PII, internal paths, and other sensitive content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the git hook can overwrite or change an existing repository pre-commit workflow. <br>
Mitigation: Check for an existing pre-commit hook before installation and merge or back up local hook logic when needed. <br>
Risk: Scans and health checks can reveal secrets, PII, internal paths, workspace size, update status, or other local security details. <br>
Mitigation: Run the scripts only on files or repositories intended for review and keep scan and health-check output local unless it has been sanitized. <br>
Risk: The hook can block commits based on scanner findings and may require human review for warnings. <br>
Mitigation: Review findings before publishing, fix blocking issues, and rotate any secret that may already have been committed or exposed. <br>


## Reference(s): <br>
- [Agent Safety on ClawHub](https://clawhub.ai/compass-soul/agent-safety) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and local script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Running the install script can create or replace a repository pre-commit hook; scanner and health-check output should be reviewed locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
