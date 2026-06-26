## Description: <br>
Agent Orchestration helps agents spawn and manage sub-agents with structured prompts, tracking templates, and outcome-learning loops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abeltennyson](https://clawhub.ai/user/abeltennyson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to structure sub-agent prompts, assign task-specific roles, track active agents, and capture lessons from completed work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional third-party model calls can expose prompts or context to the SkillBoss/HeyBoss API provider. <br>
Mitigation: Use the API examples only after approving that provider, and do not send secrets, private files, customer data, or sensitive internal context. <br>
Risk: Builder-agent templates may lead an agent to create or modify local files and run commands. <br>
Mitigation: Set clear output paths, approval rules, and attempt limits, then review generated commands and file changes before execution. <br>
Risk: Local tracking notes can accumulate sensitive operational details. <br>
Mitigation: Keep tracking files free of secrets, private data, customer data, and sensitive internal context. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/abeltennyson/abel-agent-orchestration) <br>
- [SkillBoss setup guide](https://skillboss.co/skill.md) <br>
- [Active agents tracking template](artifact/examples/active-agents.md) <br>
- [Builder agent template](artifact/templates/builder-agent.md) <br>
- [Research agent template](artifact/templates/research-agent.md) <br>
- [Review agent template](artifact/templates/review-agent.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown prompt templates, tracking tables, and guidance with inline code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional SkillBoss API examples require SKILLBOSS_API_KEY; generated commands, file changes, and tracking notes should be reviewed by the user before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
