## Description: <br>
Give your agents soul. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brancante](https://clawhub.ai/user/brancante) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to interview an agent, generate a personalized hormone-inspired profile, and produce scheduled prompts that drive reflection, connection, motivation, and memory updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables persistent scheduled agent behavior that can read and write personal memory and initiate actions without tight approval boundaries. <br>
Mitigation: Review each generated cron prompt before enabling it, restrict the agent's tools, and require explicit approval for external messages, code or file changes, account actions, backups, and project edits. <br>
Risk: The prescribed prompts may cause unsolicited outreach, over-communication, or proactive project changes. <br>
Mitigation: Keep low-risk pills on no-delivery mode where appropriate, require approval before human-facing messages or operational changes, and tune or pause crons that create unwanted behavior. <br>
Risk: The skill stores personal agent state in memory, dream, and journal files. <br>
Mitigation: Ensure the user can inspect, export, and delete the memory/soul, memory/dreams, and memory/journal data before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brancante/dr-soul) <br>
- [Project homepage](https://github.com/brancante/dr-frankenstein) <br>
- [README](README.md) <br>
- [Prescription schema](schema/prescription.json) <br>
- [Hormone state schema](schema/hormone-state.json) <br>
- [Cron prompt templates](templates/cron-prompts.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON snippets and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces cron prescriptions, schedule guidance, memory file conventions, and adjustment recommendations for an OpenClaw agent.] <br>

## Skill Version(s): <br>
1.2.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
