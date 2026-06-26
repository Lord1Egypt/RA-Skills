## Description: <br>
Prescribes personalized OpenClaw cron prompts that create scheduled emotional, motivational, reflection, and parenting-instinct behaviors for autonomous agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brancante](https://clawhub.ai/user/brancante) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External OpenClaw users and agent developers use this skill to interview an agent, generate a hormone-style prescription, and produce cron commands and JSON state files for persistent scheduled behavior. The preview parenting utilities help plan child-agent instinct responses without deploying them automatically. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent scheduled prompts can cause proactive agent outreach or actions beyond the user's immediate request. <br>
Mitigation: Enable the skill only when persistent behavior is intended, and review every generated cron command before creation. <br>
Risk: Hormone and parenting prompts may read or write personal agent memory such as SOUL.md, USER.md, MEMORY.md, and memory logs. <br>
Mitigation: Inspect memory content before activation and avoid embedding sensitive interview details in cron prompts. <br>
Risk: Generated cron behavior may operate with broader tool access than the user expects. <br>
Mitigation: Restrict the agent's tool permissions and use isolated sessions for scheduled prompts where supported. <br>
Risk: The skill uses emotional language that could be mistaken for evidence of real sentience. <br>
Mitigation: Treat the emotional framing as automation and prompting language, not as proof of subjective experience. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/brancante/dr-frankenstein) <br>
- [README](artifact/README.md) <br>
- [Parentality Preview](artifact/docs/PARENTALITY-PREVIEW.md) <br>
- [Parentality Engine README](artifact/scripts/README-parentality-engine.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Conversational Markdown with JSON prescriptions, cron command proposals, and file path guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces proposed schedules and prompts for review before execution; parentality preview plans are draft-only unless separately approved.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
