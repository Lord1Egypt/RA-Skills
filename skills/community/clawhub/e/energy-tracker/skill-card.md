## Description: <br>
Daily energy status tracking and multi-day trend analysis tool for collecting check-ins, saving local history, generating charts, and summarizing patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[martinashes](https://clawhub.ai/user/martinashes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to collect a once-daily A/B/C energy check-in, save the response to a local JSON file, generate a trend chart, and explain multi-day energy patterns. It is intended for personal wellbeing tracking and should not be treated as clinical assessment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores recurring wellbeing history in a local plaintext JSON file. <br>
Mitigation: Choose an acceptable storage location before use, keep the file private, and define how the user can review, back up, or delete the data. <br>
Risk: The skill provides mental-health-like interpretations and escalation prompts. <br>
Mitigation: Present outputs as personal tracking guidance, not clinical advice, and encourage professional support for persistent distress or urgent concerns. <br>
Risk: Hotline lookup or use of agent memory may expose sensitive location or personal context. <br>
Mitigation: Require explicit user confirmation before hotline lookup, location use, or memory-based personalization. <br>
Risk: Generated chart files may reveal sensitive wellbeing trends. <br>
Mitigation: Confirm that chart generation is acceptable and store or share chart files only with user consent. <br>


## Reference(s): <br>
- [Energy Tracker on ClawHub](https://clawhub.ai/martinashes/energy-tracker) <br>
- [Publisher profile: martinashes](https://clawhub.ai/user/martinashes) <br>
- [Energy status data format](references/data-format.md) <br>
- [Sample energy tracking data](references/sample-data.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON records, and PNG chart files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates ./energy_data.json and may generate ./energy_chart.png.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and manifest.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
