## Description:

Intelligent educational curriculum generation system with strict step enforcement and human escalation policies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tarasinghrajput](https://clawhub.ai/user/tarasinghrajput)

### License/Terms of Use:


## Use Case:

Educators, curriculum owners, and POD operators use this skill to assess existing curricula or design new curricula through structured questionnaires, resource research, escalation checkpoints, and CSV/Excel draft outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run shell-based web searches from user-provided curriculum topics.

Mitigation: Review and narrow the search behavior before installation, treat curriculum topics as untrusted input, and run searches in a controlled environment.

Risk: The skill may persist sensitive education context locally, including details about students, teacher capability, infrastructure, and operational constraints.

Mitigation: Avoid entering student-identifying or sensitive disability or socioeconomic details unless storage is explicitly disabled or controlled, and confirm where records are kept and how they can be deleted.

Risk: The release depends on external search behavior and local dependency controls.

Mitigation: Review the neo-ddg-search dependency and local runtime requirements before deployment, and limit installation to environments where dependency behavior can be audited.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tarasinghrajput/skills/curriculum-generator)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with structured curriculum tables and CSV/Excel file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are draft curricula pending human review and may include resource links, assumptions, risks, and local memory records.]

## Skill Version(s):

1.0.0 (source: server release metadata, OpenClaw frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
