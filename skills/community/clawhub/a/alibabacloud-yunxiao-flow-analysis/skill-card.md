## Description: <br>
Diagnoses Yunxiao Flow pipeline execution failures and provides fix recommendations across build, test, deployment, and variable-substitution scenarios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and DevOps engineers use this skill to inspect Yunxiao Flow pipeline runs, retrieve failed-step logs, identify root causes, and prepare concrete remediation steps for CI/CD failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access pipeline logs that may contain sensitive build, repository, or deployment details. <br>
Mitigation: Use the least-privileged read-only Yunxiao Personal Access Token available and treat retrieved logs as sensitive. <br>
Risk: The included live build-container terminal capability is broader than normal read-only troubleshooting. <br>
Mitigation: Use terminal access only when explicitly needed, review every command before it runs, and avoid terminal use on builds that may contain secrets until TLS verification and stricter command controls are fixed. <br>
Risk: terminalUrl values grant time-limited access to live build environments. <br>
Mitigation: Handle terminalUrl values as sensitive access material and avoid sharing or persisting them outside the troubleshooting session. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-yunxiao-flow-analysis) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Yunxiao Flow Troubleshooting Guide](artifact/references/troubleshooting-guide.md) <br>
- [RAM Policies](artifact/references/ram-policies.md) <br>
- [Related Commands](artifact/references/related-commands.md) <br>
- [Verification Methods](artifact/references/verification-method.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown analysis report with inline shell commands, JSON excerpts, and remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include pipeline status, failed stage and step details, log summaries, root cause analysis, and solution recommendations.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
