## Description: <br>
Give AI agents a persistent journal backed by BlueColumn semantic memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let an agent store observations, user preferences, decisions, and session notes, then recall that context in later sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Journal entries, preferences, session notes, URLs, or search queries may be stored by the provider's external backend. <br>
Mitigation: Use the skill only when external storage is acceptable, and avoid saving secrets, credentials, regulated data, or private client information unless retention, deletion, and access controls are documented. <br>
Risk: The skill requires a BlueColumn API key. <br>
Mitigation: Store the API key securely, do not log it, and rotate it if it may have been exposed. <br>


## Reference(s): <br>
- [Agent Journal API Reference](references/api.md) <br>
- [BlueColumn](https://bluecolumn.ai) <br>
- [ClawHub skill page](https://clawhub.ai/bluecolumnconsulting-lgtm/agent-journal) <br>
- [Publisher profile](https://clawhub.ai/user/bluecolumnconsulting-lgtm) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown guidance with inline bash examples and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a BlueColumn API key and sends journal content to an external backend.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
