## Description: <br>
AI Agent Training Manual is an onboarding guide for OpenClaw agents covering operating principles, workspace conventions, communication, tool use, cron and heartbeat automation, common mistakes, recommended skills, and an onboarding checklist. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrot90-code](https://clawhub.ai/user/harrot90-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agent operators, and teams use this skill to onboard or retrain OpenClaw agents with practical working norms, safety checks, and setup checklists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The manual encourages agents to locate credential material such as tokens. <br>
Mitigation: Require explicit user approval and a narrow task scope before credential discovery; never expose, copy, or reuse credentials outside the authorized workflow. <br>
Risk: The manual includes guidance for public document sharing and outbound messages. <br>
Mitigation: Require user confirmation of recipients, access permissions, and content before external sharing or messaging. <br>
Risk: The manual asks agents to delete setup files and manage persistent memory. <br>
Mitigation: Use reversible deletion where available and confirm any file deletion or persistent memory update with the user unless a prior policy authorizes it. <br>
Risk: The manual teaches recurring cron and heartbeat automation. <br>
Mitigation: Create recurring automation only with explicit user approval, clear schedule and delivery settings, and routine checks for failures or unwanted messages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrot90-code/agent-training-manual) <br>
- [Publisher profile](https://clawhub.ai/user/harrot90-code) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with checklists, tables, command examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Non-executable training material for agents; includes operational checklist and setup guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and README) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
