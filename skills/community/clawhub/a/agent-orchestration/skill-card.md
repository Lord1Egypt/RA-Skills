## Description: <br>
Helps agents structure prompts, coordinate sub-agents, track active work, and capture learnings from outcomes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawdnw](https://clawhub.ai/user/clawdnw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to design structured prompts for builder, research, and review agents, coordinate active sub-agent work, and record learnings after completion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broadly scoped sub-agent prompts can lead to unintended writes, command use, installs, or long-running work. <br>
Mitigation: Set clear write locations, command and install limits, time budgets, and approval rules for destructive or sensitive actions before using the skill. <br>
Risk: Local tracking notes may expose secrets, credentials, personal data, or confidential project details. <br>
Mitigation: Do not record secrets, credentials, personal data, or confidential project information in active-agents.md or LEARNINGS.md. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/clawdnw/agent-orchestration) <br>
- [Active agents tracking template](artifact/examples/active-agents.md) <br>
- [Builder agent prompt template](artifact/templates/builder-agent.md) <br>
- [Research agent prompt template](artifact/templates/research-agent.md) <br>
- [Review agent prompt template](artifact/templates/review-agent.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance and reusable prompt templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; server security evidence reports no hidden execution, credential use, exfiltration, or destructive behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
