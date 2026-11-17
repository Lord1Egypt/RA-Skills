## Description:

Analyze laboratory alumni career trajectories and outcomes to provide data-driven career guidance for current students and postdocs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googolme](https://clawhub.ai/user/googolme)

### License/Terms of Use:

MIT-0

## Use Case:

External lab leaders, mentors, and training-program staff use this skill to maintain alumni career records, analyze career outcomes, generate reports, and support career guidance for students and postdocs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and can export identifiable alumni career and compensation data without enforced privacy safeguards.

Mitigation: Use only consented data in a protected local data path, avoid salary and private notes unless necessary, and share aggregate or anonymized reports instead of raw exports.

Risk: Generated reports or exported datasets may expose individual alumni records if shared directly.

Mitigation: Prefer aggregate reports, anonymize outputs before external sharing, and do not distribute raw exports containing names, salary ranges, or private notes.

Risk: Dependency and local file-permission controls are not hardened by the release evidence.

Mitigation: Pin dependencies before operational use and apply file-permission hardening for alumni data files and generated reports.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; generated reports may be JSON, CSV, PDF, DOCX, or HTML depending on user request.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read, write, import, and export local alumni records and reports.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
