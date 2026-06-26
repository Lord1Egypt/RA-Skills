## Description: <br>
ClawGuard Guardian v3 - Runtime guardian with behavior monitoring, interception, session freeze/replay, and emergency response <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stardreaming](https://clawhub.ai/user/stardreaming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to ask an agent to start, inspect, freeze, unfreeze, replay, and audit local Guardian monitoring sessions for AI agent operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill presents itself as runtime protection, but the security evidence says it should be treated as a local audit/replay helper rather than a proven enforcement layer. <br>
Mitigation: Use it as advisory monitoring only, keep existing platform safeguards in place, and review any blocked or frozen operation before relying on the result. <br>
Risk: The implementation depends on a shared rules module that is not included in the artifact. <br>
Mitigation: Verify or remove the missing shared rules dependency before running the CLI so monitoring commands fail predictably instead of silently losing rule coverage. <br>
Risk: Audit, replay, and export workflows may expose sensitive operational details stored under ~/.clawguard/logs/. <br>
Mitigation: Restrict local access to the log directory, review replay/export output before sharing it, and manually clean up logs that are no longer needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/stardreaming/clawguard-guardian) <br>
- [Publisher profile](https://clawhub.ai/user/stardreaming) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with inline shell commands and JSON log examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and display local audit logs from ~/.clawguard/logs/ during status, replay, and log review workflows.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
