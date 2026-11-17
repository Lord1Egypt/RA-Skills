## Description:

Assists agents with construction-site safety inspections by analyzing uploaded site photos against GB30871-2022 and petrochemical safety standards, then producing structured hazard findings and corrective recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[112297720](https://clawhub.ai/user/112297720)

### License/Terms of Use:

MIT-0

## Use Case:

Construction safety reviewers, site managers, and safety auditors use this skill to inspect uploaded site photos for visible hazards and receive standard-aligned corrective actions. It is especially oriented toward special operations such as hot work, work at height, confined-space work, temporary electrical work, lifting, blind plate work, excavation, and road closure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded safety-management documents may be persisted into trusted reference files and influence future safety advice.

Mitigation: Keep packaged standards read-only or require explicit review before any learned content is saved.

Risk: Incorrect persisted rules could affect later hazard assessments.

Mitigation: Review learned content against authoritative safety standards before allowing it to shape future reports.

Risk: Photo-based inspection can miss hazards that are unclear, obstructed, or outside the image frame.

Mitigation: Treat unclear findings as uncertain and require onsite confirmation for unresolved or high-impact hazards.

## Reference(s):

- [GB30871-2022 Special Operation Safety Quick Reference](references/gb30871-2022.md)
- [Petrochemical Special Operation Safety Management Notes](references/petrochem-standards.md)
- [Daily Safety Knowledge Learning Log](references/learning-log.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown safety audit report with hazard tables, confidence labels, standards references, and corrective recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include immediate and time-bound remediation priorities; image findings should distinguish clear observations from uncertain or unavailable evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
