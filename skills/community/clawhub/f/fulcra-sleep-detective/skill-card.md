## Description: <br>
AI sleep investigation that uses Fulcra sleep, biometric, calendar, exercise, supplement, and lifestyle context to generate theories, proactive alerts, daily insights, and follow-up questions about sleep quality. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arc-claw-bot](https://clawhub.ai/user/arc-claw-bot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
People using Fulcra health data and agent runtime use this skill to correlate sleep, biometrics, calendar, exercise, nutrition, supplements, and lifestyle context into sleep theories, alerts, daily insights, and follow-up questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill collects and reasons over sensitive Fulcra health data, calendar context, and conversation-derived health notes. <br>
Mitigation: Use it only in a private, trusted environment and avoid group or public channels. <br>
Risk: Agent access to Fulcra authentication can expose sensitive account-backed data if credentials or device authorization details are mishandled. <br>
Mitigation: Use a fixed trusted Fulcra CLI command, share device authorization URLs and codes only through the active trusted user channel, and never send access tokens or credential files. <br>
Risk: Persistent health memory can retain calendar, CGM, nutrition, and conversation-derived notes longer than the user expects. <br>
Mitigation: Define retention, deletion, and opt-in rules before use. <br>


## Reference(s): <br>
- [Fulcra Sleep Detective on ClawHub](https://clawhub.ai/arc-claw-bot/fulcra-sleep-detective) <br>
- [Fulcra Biometric Intelligence System Blueprint](docs/fulcra-agent-blueprint.md) <br>
- [Fulcra](https://fulcradynamics.com) <br>
- [agent runtime](https://github.com/agent-runtime) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, plain text, and JSON produced by Fulcra data analysis scripts and agent-facing command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include sleep theories, proactive alerts, daily insight summaries, follow-up questions, and local state updates.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
