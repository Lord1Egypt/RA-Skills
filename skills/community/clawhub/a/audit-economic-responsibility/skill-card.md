## Description:

Provides a Chinese-language, 10-step economic responsibility audit workflow with four checkpoints for ongoing, departure, and natural resource asset audits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rc17777](https://clawhub.ai/user/rc17777)

### License/Terms of Use:

MIT-0

## Use Case:

Audit teams and agents use this skill to run a structured Chinese-language economic responsibility audit workflow for public-sector leadership reviews, including audit planning, financial analysis, decision review, internal control testing, evidence classification, working papers, report drafting, and report review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit inputs and generated findings may contain sensitive organizational, personnel, financial, or legal information.

Mitigation: Handle audit materials under the user's applicable confidentiality, access-control, and retention procedures.

Risk: The workflow depends on external local scripts that are not included as authoritative safety evidence in the card context.

Mitigation: Review and approve pipeline_engine.py, audit_workflow.py, and audit_router.py in the deployment environment before running the workflow.

Risk: Generated evidence assessments, legal citations, and responsibility determinations may be incomplete or inaccurate.

Mitigation: Require review by qualified audit or legal personnel before relying on outputs for decisions or reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rc17777/skills/audit-economic-responsibility)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell command examples and workflow-generated audit text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language audit workflow outputs; depends on external pipeline_engine.py, audit_workflow.py, and audit_router.py scripts.]

## Skill Version(s):

1.0.0 (source: evidence release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
