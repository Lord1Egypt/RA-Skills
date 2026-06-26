## Description: <br>
Produce a practical 3-day northern lights planning and live-update workflow for Tim in Dereham, Norfolk, with alert-day escalation, North Norfolk coast comparison, and conservative go or no-go decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[timcoy47](https://clawhub.ai/user/timcoy47) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to maintain a practical Norfolk aurora watch for Dereham and the North Norfolk coast, including 3-night outlooks, alert-day briefs, change alerts, and live-night updates. It supports conservative travel decisions by blending space-weather signals with local sky conditions, darkness, moonlight, and horizon advantage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring checks and local state could create unnecessary noise or retain more history than needed. <br>
Mitigation: Keep scheduled checks limited to the intended Norfolk aurora watch and store only the small state record described by the skill in a known limited location. <br>
Risk: Broad tool access could fetch or write outside the intended forecast workflow. <br>
Mitigation: Limit the agent to public forecast sources and its own state file, using browser automation only if normal web or HTTP access cannot retrieve the needed data. <br>
Risk: Aurora forecasts can be stale, conflicting, or too uncertain for confident travel advice. <br>
Mitigation: Follow the skill's confidence rules, reduce confidence when key feeds are stale or disagree, and prefer watch or stand_down for weak or marginal signals. <br>


## Reference(s): <br>
- [Source checklist](references/source-checklist.md) <br>
- [Message rules](references/message-rules.md) <br>
- [OpenClaw setup notes](references/openclaw-setup.md) <br>
- [ClawHub release page](https://clawhub.ai/timcoy47/aurora-norfolk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown tables and concise text briefs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Europe/London local time, practical percentages, confidence labels, and one conservative action per update.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
