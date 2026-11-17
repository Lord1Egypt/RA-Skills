## Description:

Design clinical trial CRFs with proper validation rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Clinical data managers, trial builders, and developers use this skill to create electronic case report form specifications, validation rules, skip logic patterns, and data dictionaries for clinical trial data collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script can write to any user-supplied output file path accessible to the running account.

Mitigation: Run it in a sandboxed workspace and provide explicit workspace-relative output paths; avoid directories where overwriting files would matter until path validation or overwrite protection is added.

Risk: Generated CRF specifications may need study-specific and regulatory review before operational use.

Mitigation: Review generated forms, validation rules, skip logic, and data dictionaries against the study protocol, CDISC SDTM expectations, and EDC configuration requirements before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/ecrf-designer)
- [AIPOCH publisher profile](https://clawhub.ai/user/aipoch-ai)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Console text and JSON file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a CRF JSON file to the requested output path.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
