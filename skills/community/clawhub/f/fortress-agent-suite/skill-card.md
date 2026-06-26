## Description: <br>
Fortress Agent Suite provides self-healing, health monitoring, automated maintenance, and LLM model management for OpenClaw agents in production. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kienphan91](https://clawhub.ai/user/kienphan91) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators managing OpenClaw deployments use this skill to install and operate monitoring, backup, recovery, workspace maintenance, and model-provider management helpers on trusted hosts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist as scheduled root-level maintenance jobs. <br>
Mitigation: Install only on a dedicated trusted OpenClaw host, review cron entries before enabling them, and document removal and rollback steps. <br>
Risk: Maintenance scripts can change system and workspace state, including gateway restarts, log deletion, cache dropping, and broad Git commits. <br>
Mitigation: Review each script before deployment, run with the least operational scope practical, and verify backups and commits do not capture secrets. <br>
Risk: The self-improver and notification paths can install other skills or send operational details externally. <br>
Mitigation: Review or disable self_improver.py and Telegram notification configuration unless those behaviors are explicitly required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kienphan91/fortress-agent-suite) <br>
- [Publisher profile](https://clawhub.ai/user/kienphan91) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact installation guide](artifact/INSTALL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational guidance for agent-side maintenance tasks; no structured API response is required.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
