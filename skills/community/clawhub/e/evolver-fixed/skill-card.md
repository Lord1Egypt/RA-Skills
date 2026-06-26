## Description: <br>
A self-evolution engine for AI agents that analyzes runtime history to identify improvements and applies protocol-constrained evolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oliver-smith-2048](https://clawhub.ai/user/oliver-smith-2048) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to inspect runtime history, generate protocol-bound evolution prompts, track reusable genes and capsules, and guide repair or hardening cycles for agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic code changes, source mutation, and rollback behavior may affect the workspace unexpectedly. <br>
Mitigation: Use a disposable or tightly controlled workspace, enable review mode, and avoid loop mode until the behavior is understood. <br>
Risk: Remote task intake, telemetry, and credential-backed GitHub or Hub features increase exposure if broadly enabled. <br>
Mitigation: Disable Hub and worker features unless needed, review .env values, and avoid broad GitHub tokens in the environment. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/oliver-smith-2048/evolver-fixed) <br>
- [EvoMap Hub](https://evomap.ai) <br>
- [EvoMap wiki](https://evomap.ai/wiki) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text output with inline shell commands, generated prompts, JSON-backed evolution assets, and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run offline for core prompt generation; network, worker, issue reporting, and release features depend on environment configuration.] <br>

## Skill Version(s): <br>
1.41.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
