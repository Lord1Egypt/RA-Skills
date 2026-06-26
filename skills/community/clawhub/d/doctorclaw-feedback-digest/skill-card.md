## Description: <br>
Customer feedback digest that collects, categorizes, and summarizes reviews, survey responses, and support tickets for weekly or on-demand use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ceobotson-bot](https://clawhub.ai/user/ceobotson-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Customer success, support, product, and operations teams use this skill to turn reviews, surveys, support tickets, and social mentions into sentiment summaries, topic trends, urgent issue alerts, and draft responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feedback sources may contain customer identifiers or sensitive support details. <br>
Mitigation: Limit the sources the agent may read and redact customer identifiers where practical before sharing or archiving digests. <br>
Risk: Digests and urgent alerts may expose private customer feedback if delivered or stored in broad channels. <br>
Mitigation: Use private delivery channels and define retention or deletion rules for archived feedback digests. <br>
Risk: Draft responses to reviews or tickets could be posted without sufficient review. <br>
Mitigation: Require explicit approval before any customer-facing or public response is posted. <br>


## Reference(s): <br>
- [DoctorClaw Website](https://www.doctorclaw.ceo) <br>
- [ClawHub Skill Page](https://clawhub.ai/ceobotson-bot/doctorclaw-feedback-digest) <br>
- [Publisher Profile](https://clawhub.ai/user/ceobotson-bot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown digest with sentiment and topic summaries, urgent issue flags, recommendations, and draft customer responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include immediate alerts and archived Markdown digests when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
