## Description: <br>
Guides users through personalized cold-exposure progression, session logging, reminders, safety checks, and escalation prompts while the user performs the physical exposure work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[howtousehumans](https://clawhub.ai/user/howtousehumans) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to plan and track a progressive at-home cold-exposure routine, including safety screening, local supply research prompts, logs, and medical escalation drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cold exposure can be physically risky, especially for users with cardiovascular conditions, Raynaud's, pregnancy, recent illness, dizziness, chest pain, or extreme water temperatures. <br>
Mitigation: Use only after considering medical clearance, start with conservative exposure, stop immediately for concerning symptoms, and avoid unsupervised natural-water plunges or breath-hold cold activities. <br>
Risk: The skill asks users to log health-related data such as fitness, symptoms, mood, energy, and session details. <br>
Mitigation: Keep logs local, minimize sensitive details, and only allow filesystem writes after the user approves where data will be stored. <br>
Risk: Some described reminders, calendar actions, research, and email drafting depend on tools the agent may not actually have. <br>
Mitigation: Treat those actions as unavailable unless the running agent has the required tools and the user approves each external lookup, message, or integration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/howtousehumans/deliberate-cold-exposure) <br>
- [Skill source](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with install command, checklists, logs, reminders, and draft messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local markdown logs when the agent has filesystem access and the user approves.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
