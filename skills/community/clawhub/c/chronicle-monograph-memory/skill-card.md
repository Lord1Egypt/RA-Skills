## Description: <br>
Hippocampus provides durable local memory for agents, including chronicle and monograph storage, checkpoints, workflow recall, proactive triggers, and failure-pattern warnings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gabe-luv-nancy](https://clawhub.ai/user/gabe-luv-nancy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to preserve and recall local conversation context, project checkpoints, workflows, and lessons learned across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill saves and reuses local conversation context, which can include sensitive personal, credential, or project information if users store it. <br>
Mitigation: Avoid saving secrets, credentials, personal data, or confidential project details, and periodically inspect or delete files under assets/hippocampus. <br>
Risk: Auto-save, proactive triggers, and reading-between-the-lines behavior can load or preserve context without an explicit recall command. <br>
Mitigation: Review USER_CONFIG.md before enabling scheduled jobs, and narrow or disable AUTO_SAVE, PROACTIVE_TRIGGERS_ENABLED, and READINGBETWEENTHELINES_ENABLED when durable memory is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gabe-luv-nancy/chronicle-monograph-memory) <br>
- [README.md](artifact/README.md) <br>
- [USER_CONFIG.md](artifact/USER_CONFIG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and command-oriented guidance with local memory files and SQLite-backed indexes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and reads local assets/hippocampus memory files when initialized and configured.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and artifact version files) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
