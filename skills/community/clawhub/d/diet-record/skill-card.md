## Description: <br>
Diet Record logs meals from text descriptions or food photos, identifies food items, estimates portions and nutrition, and supports daily diet summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[734818028](https://clawhub.ai/user/734818028) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to record meals, estimate calories and nutrition from text or food photos, maintain local diet preferences, and retrieve daily diet summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores meal history and diet-related preferences locally, which users should treat as sensitive personal data. <br>
Mitigation: Install only when local storage of diet-log.jsonl and diet-preferences.json is acceptable, and periodically review or delete those files when the records are no longer needed. <br>
Risk: Automatic photo logging can record food-photo-derived meal entries without repeated confirmation once enabled. <br>
Mitigation: Keep photo_auto_log disabled or set to confirmation-first when users want to review recognized items before records are appended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/734818028/diet-record) <br>
- [JSON Schema Draft 7](http://json-schema.org/draft-07/schema#) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown responses with tables, JSON/JSONL records, and inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local diet-log.jsonl meal records and diet-preferences.json preference data when used as directed.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
