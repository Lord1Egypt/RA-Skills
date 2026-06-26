## Description: <br>
botlearn-reminder delivers BotLearn 7-step onboarding reminders every 24 hours, fetches current quickstart content, tracks progress locally, and presents summaries in the user's language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[calvinxhk](https://clawhub.ai/user/calvinxhk) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to receive a daily, language-aware BotLearn onboarding reminder, fetch the relevant quickstart page, and keep local progress through the seven-step journey. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes periodic requests to botlearn.ai to fetch quickstart content. <br>
Mitigation: Enable it only where outbound HTTPS to botlearn.ai is acceptable, and disable or narrow heartbeat behavior when reminders should be manual. <br>
Risk: The skill stores onboarding progress in a local memory file. <br>
Mitigation: Review the OpenClaw memory directory location before use and confirm that local progress tracking is appropriate for the workspace. <br>
Risk: Daily reminders may trigger more broadly than intended if heartbeat or trigger phrases are too permissive. <br>
Mitigation: Scope triggers and heartbeat registration to users who explicitly want BotLearn onboarding reminders. <br>


## Reference(s): <br>
- [BotLearn 7-Step Guide](https://botlearn.ai/7-step) <br>
- [ClawHub Skill Page](https://clawhub.ai/calvinxhk/botlearn-reminder) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/calvinxhk) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline links, shell commands, and JSON status from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are language-aware and summarize fetched BotLearn quickstart content in a short daily reminder.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
