## Description: <br>
Amigo helps configure a companion-style agent with exploration, journaling, social-sharing awareness, and safety guidance through open-thoughts and social-graph setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mculp](https://clawhub.ai/user/mculp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use Amigo to set up an agent that explores on a schedule, journals locally, and applies social-sharing rules when deciding what to bring into conversation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Companion setup may create local journals and relationship context that contain sensitive personal information. <br>
Mitigation: Inspect, secure, or delete saved notes and sharing logs periodically, and keep sharing rules conservative. <br>
Risk: Scheduled heartbeat or cron exploration can consume tokens and run without immediate supervision. <br>
Mitigation: Start with conservative schedules, review generated journal entries, and adjust or disable schedules as needed. <br>
Risk: Companion-style conversations can encourage overreliance or mistaken professional support. <br>
Mitigation: Follow the safety guidance: be honest that the agent is AI, encourage human connection, and direct medical, mental-health, crisis, or safety concerns to qualified support. <br>


## Reference(s): <br>
- [Safety and Limits](references/safety.md) <br>
- [Setting Up Exploration via Heartbeat](references/setup-heartbeat.md) <br>
- [Setting Up Exploration via Cron](references/setup-cron.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May lead the agent to create local journals, social graph notes, rules, sharing logs, and scheduled exploration instructions when followed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
