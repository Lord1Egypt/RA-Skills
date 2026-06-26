## Description: <br>
Agent Batch Guard helps agents handle large repetitive tasks by using script-based batching, checkpointing, circuit breakers, and configuration guidance to reduce session transcript growth and compaction failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evan966890](https://clawhub.ai/user/evan966890) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to plan large scraping, export, and batch-processing tasks so agents write durable scripts, persist outputs to files, resume from checkpoints, and stop after repeated failures instead of filling the conversation transcript. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated batching scripts may operate on real devices, accounts, output paths, or collected data. <br>
Mitigation: Review generated scripts before running them and keep device targets, accounts, output paths, and data scope explicit. <br>
Risk: Randomized-delay guidance could be misused to evade service rules or anti-abuse systems. <br>
Mitigation: Use delay and retry patterns only for reliability and rate-limit respect, not to bypass service policies or anti-abuse controls. <br>
Risk: The artifact contains an incorrect checklist item about unsupported compaction rolling and maxTurns settings. <br>
Mitigation: Follow the corrected OpenClaw guidance that compaction tuning is limited to safeguard mode and avoid unsupported configuration options. <br>


## Reference(s): <br>
- [Agent Batch Guard on ClawHub](https://clawhub.ai/evan966890/agent-batch-guard) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with code, shell command, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; generated scripts and configuration should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
