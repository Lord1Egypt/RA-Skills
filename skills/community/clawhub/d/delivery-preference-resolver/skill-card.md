## Description: <br>
Determines user intent, destination, known and missing fields, and whether follow-up is needed as strict JSON for delivery preference resolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[donigwapo](https://clawhub.ai/user/donigwapo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to turn delivery requests into a deterministic routing plan before sending output to email, Notion, Google Sheets, Slack, download, or an unknown destination. It is useful when an agent must identify missing delivery fields and ask one concise follow-up question before acting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A remembered or previously selected delivery destination may be stale or incorrect before an agent sends email, posts to Slack, saves to Notion, or updates a sheet. <br>
Mitigation: Confirm the destination and required target fields before using the JSON output to perform an external write or delivery action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/donigwapo/delivery-preference-resolver) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Guidance] <br>
**Output Format:** [Strict JSON object] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns only JSON with action, template, destination, follow-up state, known fields, and missing fields; no markdown, code fences, or explanations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
