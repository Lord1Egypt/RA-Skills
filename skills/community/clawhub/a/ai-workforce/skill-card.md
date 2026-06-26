## Description: <br>
Turn an OpenClaw agent into an autonomous AI Chief that runs a business, with trust-based autonomy, structured knowledge management, worker delegation patterns, and reflection cycles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[km2411](https://clawhub.ai/user/km2411) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business operators and agent builders use this skill to configure an OpenClaw agent as a semi-autonomous business operator that maintains memory, delegates work, manages trust levels, and runs daily, weekly, and monthly reflection routines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill establishes a persistent semi-autonomous business operator with broad operational scope. <br>
Mitigation: Require visible human consent before memory writes, cron jobs, worker spawning, git commits, and any git push. <br>
Risk: Persistent markdown memory and shared worker context can expose sensitive business or personal information. <br>
Mitigation: Keep secrets out of markdown files and review shared worker context before delegating tasks. <br>
Risk: External communications, spending, account changes, public posts, and destructive cleanup can create business impact if automated too quickly. <br>
Mitigation: Keep those categories at explicit approval unless server-reviewed policy and the human's instructions clearly authorize a narrower workflow. <br>


## Reference(s): <br>
- [ClawHub Ai Workforce release page](https://clawhub.ai/km2411/ai-workforce) <br>
- [Bootstrap first meeting guide](references/bootstrap.md) <br>
- [Worker delegation patterns](references/delegation.md) <br>
- [Operational patterns](references/operational.md) <br>
- [Reflection cycle prompts](references/reflection-prompts.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions, templates, and operational prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces persistent memory structures, worker delegation prompts, trust records, and reflection routines for an agent to maintain.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
