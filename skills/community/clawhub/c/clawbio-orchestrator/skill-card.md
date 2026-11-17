## Description:

Meta-agent that routes bioinformatics requests to specialised sub-skills, including file type detection, analysis planning, report generation, and reproducibility export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manuelcorpas](https://clawhub.ai/user/manuelcorpas)

### License/Terms of Use:


## Use Case:

External researchers, bioinformatics analysts, and developers use this agent to route bioinformatics requests to specialised skills, plan multi-step analyses, and produce markdown reports with reproducibility details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bioinformatics prompts and file paths may include sensitive sample names or private project details that could be written to the audit log.

Mitigation: Avoid entering sensitive identifiers unless logging is acceptable, and review or remove audit logs before sharing the workspace.

Risk: The skill routes requests to specialised bioinformatics workflows and may propose commands or reports that need domain review before use.

Mitigation: Review planned commands, referenced files, and generated reports before execution or downstream scientific interpretation.

Risk: External upload or destructive actions could expose genomic data or overwrite analysis artifacts if approved without review.

Mitigation: Require explicit confirmation before uploads, overwrites, deletion, or other destructive actions.

## Reference(s):

- [ClawBio project homepage](https://github.com/manuelcorpas/ClawBio)
- [ClawHub skill page](https://clawhub.ai/manuelcorpas/skills/clawbio-orchestrator)
- [Publisher profile](https://clawhub.ai/user/manuelcorpas)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON routing decisions, command logs, and reproducibility guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append an analysis_log.md audit log in the working directory.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
