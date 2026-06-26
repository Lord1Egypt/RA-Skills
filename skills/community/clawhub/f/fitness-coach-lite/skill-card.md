## Description: <br>
Fitness Coach Lite is a Telegram-native personal workout tracker for low-friction exercise logging, status tracking, dynamic training suggestions, and daily, weekly, and monthly reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youhan2021](https://clawhub.ai/user/youhan2021) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill with OpenClaw or Telegram-style chat to record workouts and body status with minimal interaction, maintain a local training plan, and generate progress reports. It is suited for personal fitness tracking rather than medical advice or clinical health management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can save sensitive workout, injury, sleep, menstrual-cycle, weight, body-fat, and status information as local JSON. <br>
Mitigation: Use it only in trusted workspaces, keep the data directory private, and avoid sharing generated history or body-status files. <br>
Risk: Broad chat triggers and import, reset, or same-day logging commands can overwrite or remove workout records. <br>
Mitigation: Use explicit commands for plan imports and resets, import plans only from trusted filesystem paths, and keep backups for workout history that matters. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/youhan2021/fitness-coach-lite) <br>
- [Skill definition](SKILL.md) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text responses with shell command invocations and JSON-backed workout, status, body, and plan records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may create or update local JSON files under data/ for plans, workout history, body status, and active workout/session state.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
