## Description:

Prevent MSHA citations at cement plants before the inspector arrives with 30 CFR Part 56 hazard classification, stop-work authority, citation defense strategies, walk-through prep checklists, and rebuttal letter drafting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[larkinjoshuad](https://clawhub.ai/user/larkinjoshuad)

### License/Terms of Use:

MIT-0

## Use Case:

Plant safety managers, supervisors, safety consultants, and plant IT teams use this skill to classify cement-plant hazards, gate stop-work decisions, prepare for MSHA inspections, look up 30 CFR Part 56 citations, and draft counsel-reviewed citation response materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hazard text may be passed through an unsafe shell-style command pattern.

Mitigation: Invoke check_stopwork.py with structured arguments or stdin rather than a rendered shell command.

Risk: Blanket audit logging may capture sensitive operational or worker information without clear privacy controls.

Mitigation: Define an audit-log policy covering retention, access, minimization, and review before deployment.

Risk: Citation-defense outputs may be mistaken for legal advice or final contest strategy.

Mitigation: Use defense materials for factual preparation and abatement documentation only, and route formal responses through qualified legal counsel.

## Reference(s):

- [CementOps AI](https://cementops.ai)
- [ClawHub skill page](https://clawhub.ai/larkinjoshuad/skills/cementops-msha-compliance)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)
- [citation-rules.json](artifact/citation-rules.json)
- [stop-work-rules.json](artifact/stop-work-rules.json)
- [hazard-taxonomy.json](artifact/hazard-taxonomy.json)
- [check_stopwork.py](artifact/check_stopwork.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with structured hazard classifications, stop-work directives, CFR references, checklists, rebuttal outlines, and inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke a Python stop-work checker and use local JSON rule, citation, and taxonomy files.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
