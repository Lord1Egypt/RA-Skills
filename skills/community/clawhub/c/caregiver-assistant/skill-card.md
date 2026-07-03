## Description: <br>
护工助手 helps caregiving teams manage patient profiles, care logs, medication, vital signs, diet records, family reports, emergency handling, multi-patient workflows, and shift handoffs through an interactive HTML dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External caregiving teams, elder-care organizations, and home-care coordinators use this skill to generate and operate a local browser-based dashboard for tracking patient care activities, medications, vital signs, reports, emergency contacts, and shift handoffs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive care records may be stored in browser localStorage and exported as JSON backups. <br>
Mitigation: Use only trusted devices and browser profiles, avoid entering real patient or protected health information unless local storage meets the user's privacy requirements, and protect exported backup files as sensitive medical records. <br>
Risk: Imported backup files can replace local dashboard data. <br>
Mitigation: Import only trusted JSON backups, keep a current export before importing, and review imported records before relying on them for care coordination. <br>
Risk: The skill requests broader agent authority than the local dashboard requires. <br>
Mitigation: Deploy with the minimum required tool permissions and remove Bash access unless a reviewed workflow explicitly needs it. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/bettermen/caregiver-assistant) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Caregiver HTML dashboard](artifact/assets/caregiver.html) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Files, Guidance] <br>
**Output Format:** [Markdown guidance that produces or opens a single-file interactive HTML dashboard] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dashboard data is stored in browser localStorage and can be imported or exported as JSON backups.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
