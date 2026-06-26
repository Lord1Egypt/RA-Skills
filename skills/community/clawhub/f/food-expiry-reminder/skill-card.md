## Description: <br>
Records food inventory in a local JSON file, calculates expiry dates from production dates and shelf-life days, lists inventory status, and reports foods that are expired or nearing expiry. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Unlimitwave](https://clawhub.ai/user/Unlimitwave) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to maintain a household or small-team food inventory, add food records, check expiry status, and surface reminders for items that should be used soon. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Food inventory and notes are stored in a local JSON file and may include personal household information. <br>
Mitigation: Review and clear bundled sample records before personal use, and avoid storing sensitive notes in data/food_data.json. <br>
Risk: Local inventory data can be lost if data/food_data.json is deleted or overwritten. <br>
Mitigation: Back up data/food_data.json if the inventory matters. <br>
Risk: Scheduled reminders can create recurring local command execution if a user adds cron or similar automation. <br>
Mitigation: Only configure scheduled checks intentionally, and review the exact command and working directory before enabling automation. <br>


## Reference(s): <br>
- [Data Structure](references/data_structure.md) <br>
- [Usage Examples](references/examples.md) <br>
- [FAQ](references/faq.md) <br>
- [ClawHub skill page](https://clawhub.ai/Unlimitwave/food-expiry-reminder) <br>
- [Publisher profile](https://clawhub.ai/user/Unlimitwave) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local JSON file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Python standard-library scripts and stores food records locally in data/food_data.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
