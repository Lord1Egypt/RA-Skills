## Description: <br>
Helps patients organize pre-visit questions, prior records, checklists, and timelines before clinic visits without providing diagnoses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Patients, caregivers, and clinic support users use this skill to turn symptoms, prior tests, records, and questions into a structured pre-visit preparation draft for review with a clinician. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat organized visit-prep text as medical advice or a diagnosis. <br>
Mitigation: Use the output only as an editable preparation draft and review clinical decisions with a qualified clinician. <br>
Risk: User notes may contain sensitive health or personal information. <br>
Mitigation: Use only intentionally selected local files, de-identify details when possible, and review the output before sharing it. <br>
Risk: Pointing the local script at broad or unrelated folders may expose more local content than intended. <br>
Mitigation: Run it on the specific input file or folder needed for clinic-visit preparation and avoid changing bundled resources to inspect unrelated locations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/52YuanChangXing/clinic-visit-prep) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/52YuanChangXing) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Shell commands] <br>
**Output Format:** [Structured Markdown or JSON generated from user-provided notes and local templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include visit goals, timelines, documents to bring, suggested questions, medication or testing reminders, post-visit note slots, and items to confirm.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
