## Description:

Calculates gestational age and follow-up date windows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and care-operation teams use this skill to calculate gestational age from last menstrual period dates and compute follow-up visit windows for scheduling workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional output path can overwrite files that the running process can write.

Mitigation: Run the skill in a sandbox or read-only workspace, or restrict --output to a dedicated output directory with overwrite protection.

Risk: Medical date calculations can be misapplied if treated as clinical advice.

Mitigation: Use results as scheduling support only and require appropriate human review for clinical decisions.

## Reference(s):

- [Date Calculator References](references/guidelines.md)
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/date-calculator)
- [AIPOCH Publisher Profile](https://clawhub.ai/user/aipoch-ai)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with bash examples and structured JSON calculator output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional JSON output file when an output path is supplied]

## Skill Version(s):

0.1.0 (source: server release evidence; skill frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
