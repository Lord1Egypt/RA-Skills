## Description: <br>
Cron Worker Guardrails helps agents harden OpenClaw cron and background workers against brittle shell execution, cwd/env drift, false pipeline failures, and noisy success output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phenomenoner](https://clawhub.ai/user/phenomenoner) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to design or review cron and background worker prompts, wrappers, and scripts so scheduled jobs are deterministic, low-noise, idempotent, and safer to rerun. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated cron or background worker changes could delete data, alter persistent configuration, or mutate control-plane settings without enough review. <br>
Mitigation: Require explicit approval for deletion, persistent configuration changes, or control-plane mutations before applying the skill to real scheduled jobs. <br>
Risk: Scheduled jobs can become brittle or noisy if generated scripts and commands are not reviewed for scope, idempotency, cwd/env assumptions, and success output. <br>
Mitigation: Review any scripts an agent creates, keep jobs narrowly scoped and idempotent, document required environment, and use silent-on-success behavior. <br>


## Reference(s): <br>
- [Cron Agent Contract](references/cron-agent-contract.md) <br>
- [Cron exec pitfalls](references/pitfalls.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown guidance with inline shell command patterns and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; no executable code is included in the skill artifact.] <br>

## Skill Version(s): <br>
1.0.5 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
