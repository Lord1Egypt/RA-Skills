## Description: <br>
Calorie Counter helps agents track daily calorie and protein intake, set calorie goals, log weight, and maintain local SQLite daily totals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cnqso](https://clawhub.ai/user/cnqso) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and their agents use this skill to manually log food, calories, protein, calorie goals, and weight in a local tracker. It supports quick progress checks, entry deletion, history review, and offline personal tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Food, calorie, protein, goal, and weight history are saved locally in plaintext SQLite storage. <br>
Mitigation: Install only where local files and backups are acceptable for this data, and avoid shared or synced workspaces unless that exposure is intended. <br>
Risk: Broad food mentions could cause an agent to persist food or weight information without clear user confirmation. <br>
Mitigation: Configure or instruct the agent to log entries only when the user explicitly asks to log or track the information. <br>


## Reference(s): <br>
- [Calorie Counter ClawHub listing](https://clawhub.ai/cnqso/calorie-counter) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text and Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates a local SQLite database named calorie_data.db.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
