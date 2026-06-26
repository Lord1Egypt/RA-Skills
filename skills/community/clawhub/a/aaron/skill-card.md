## Description: <br>
Persistent receptionist/orchestrator agent for all CFO dental appointments. Aaron manages scheduling, reminders, pre-appointment prep, post-appointment follow-up, and insurance coordination. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ironiclawdoctor-design](https://clawhub.ai/user/ironiclawdoctor-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Used by an individual or their delegated agent to manage dental appointments, reminders, insurance details, treatment follow-up, and local dental records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores sensitive dental, insurance, and location-related profile details in local plaintext JSON files. <br>
Mitigation: Use it only when local plaintext storage is acceptable, avoid entering insurance identifiers unless needed, and confirm how to delete records and logs. <br>
Risk: Built-in commute and location assumptions may be sensitive or inaccurate. <br>
Mitigation: Review reminder text and travel assumptions before relying on them for appointment timing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ironiclawdoctor-design/aaron) <br>
- [Publisher profile](https://clawhub.ai/user/ironiclawdoctor-design) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text status reports, reminders, command examples, and local JSON records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists dental records and logs locally in JSON/JSONL files.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
