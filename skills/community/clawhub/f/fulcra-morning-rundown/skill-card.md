## Description: <br>
Delivers a personalized morning briefing that combines Fulcra sleep and calendar data, weather, recent subjective check-in context, and open loops, then adapts tone and depth to the user's current state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keng009](https://clawhub.ai/user/keng009) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and agent users use this skill to start the day with a concise briefing that blends sleep, calendar, weather, subjective mood, and prior open-loop context. It is intended for private personal planning, not public sharing of health or calendar details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive sleep, heart-rate, calendar, mood, and open-loop context. <br>
Mitigation: Use it only in private contexts, keep collector output private, summarize sensitive details, and avoid exposing exact health or calendar values in public or shared conversations. <br>
Risk: The package includes broader Fulcra and Attio write/delete utilities beyond the read-oriented morning briefing workflow. <br>
Mitigation: Review the installed files before use, install only from a trusted publisher, and avoid invoking write/delete helper commands unless they are explicitly needed and understood. <br>
Risk: Configurable API bases, CLI command, and concierge home settings can redirect calls or imports if set to untrusted values. <br>
Mitigation: Use trusted values for FULCRA_API_BASE, ATTIO_API_BASE, FULCRA_CLI_COMMAND, and FULCRA_CONCIERGE_HOME, and prefer the default Fulcra and Attio endpoints. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/keng009/skills/fulcra-morning-rundown) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown briefing with optional JSON context collection output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses best-effort data collection; missing sources are marked unavailable and should be skipped.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
