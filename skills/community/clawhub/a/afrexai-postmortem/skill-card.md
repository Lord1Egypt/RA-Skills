## Description: <br>
Generates structured, blameless incident postmortems from raw incident notes, including summaries, timelines, root-cause analysis, impact, action items, and prevention measures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1kalin](https://clawhub.ai/user/1kalin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, SREs, incident commanders, and operations teams use this skill to turn raw incident notes, Slack or PagerDuty text, and bullet points into a postmortem draft with clear follow-up actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incident notes may contain secrets, credentials, customer personal data, hostnames, or confidential operational details. <br>
Mitigation: Sanitize copied incident material before using the skill and remove sensitive details that are not necessary for the postmortem. <br>
Risk: A generated postmortem can contain incomplete or inaccurate conclusions if the source notes are sparse or ambiguous. <br>
Mitigation: Review the generated draft, resolve flagged information gaps, and confirm timeline, impact, root cause, and action items before sharing or publishing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/1kalin/afrexai-postmortem) <br>
- [AfrexAI Context Packs](https://afrexai-cto.github.io/context-packs/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Guidance] <br>
**Output Format:** [Markdown postmortem draft] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes severity, timeline, root-cause analysis, impact assessment, action items, lessons learned, prevention measures, and flagged information gaps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
