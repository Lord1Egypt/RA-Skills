## Description: <br>
Smart garden irrigation that reads Tuya soil sensors, checks recent and forecast weather, decides whether each zone should be watered, and can generate bilingual irrigation reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bowlderstudio](https://clawhub.ai/user/bowlderstudio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and garden operators use this skill to assess soil moisture, weather, and recent watering history, then produce irrigation recommendations or run configured watering actions for greenhouse and outdoor zones. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can open physical irrigation valves without confirmation when full automation is enabled. <br>
Mitigation: Set automation.require_confirmation to true or use scripts/run_with_confirmation.py until valve IDs, sensor IDs, and watering durations have been verified. <br>
Risk: Operational reports can be sent externally when bot reporting is enabled. <br>
Mitigation: Disable bot reporting unless needed, and carefully verify bot_account_id and bot_target before enabling report delivery. <br>
Risk: Tuya credentials grant device-control capability and local parent config overrides can affect runtime behavior. <br>
Mitigation: Provide Tuya credentials only in intended deployments and ensure the parent ../config directory is not writable by untrusted processes. <br>


## Reference(s): <br>
- [Garden Irrigation ClawHub page](https://clawhub.ai/bowlderstudio/garden-irrigation) <br>
- [tuya-cloud dependency](https://clawhub.ai/minshi-veyt/tuya-cloud) <br>
- [Tuya OpenAPI endpoint configured by the skill](https://openapi.tuyaeu.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown irrigation reports, JSONL history files, console status text, and optional message-send instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may actuate Tuya irrigation valves and optionally send reports through an OpenClaw or Telegram bot when configured.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
