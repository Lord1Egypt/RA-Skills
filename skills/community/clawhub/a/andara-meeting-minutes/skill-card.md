## Description: <br>
Capture meeting summaries and action items from voice or text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[atiati82](https://clawhub.ai/user/atiati82) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Team members and employees use this skill to turn meeting notes into structured records, save action items in PostgreSQL, and receive a concise German confirmation summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting notes may contain sensitive business or personal information that is stored in PostgreSQL. <br>
Mitigation: Use only an approved database with retention and access policies suitable for the meeting content. <br>
Risk: Database writes are triggered from broad voice or text cues and have under-specified write controls. <br>
Mitigation: Use a dedicated least-privilege PostgreSQL role and add a confirmation step before writing records. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/atiati82/andara-meeting-minutes) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands] <br>
**Output Format:** [German structured Markdown summary with PostgreSQL psql command execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses DATABASE_URL and writes meeting records and action items to PostgreSQL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
