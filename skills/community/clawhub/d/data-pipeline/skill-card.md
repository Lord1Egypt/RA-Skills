## Description:

Data Pipeline helps agents produce JavaScript guidance and code for composable ETL, data cleaning, validation, analysis, retry, timeout, and metrics workflows over array and object data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pagoda111king](https://clawhub.ai/user/pagoda111king)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design and explain JavaScript data-processing pipelines for cleaning, transforming, validating, merging, aggregating, and analyzing structured records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Attacker-controlled field names, rename maps, join keys, or defaults could exercise unsafe special-key behavior in transforms.

Mitigation: Use trusted schemas, maps, join keys, and defaults, or validate them before execution; audit special-key handling before accepting untrusted configuration.

Risk: The JavaScript dev dependency tree may need review before deployment.

Mitigation: Install from the lockfile and audit or update development dependencies as part of release qualification.

Risk: Chinese-language source comments and documentation may slow or weaken review for teams without Chinese fluency.

Mitigation: Assign a reviewer who can read the source language or translate the comments and examples before production use.

## Reference(s):

- [ClawHub Data Pipeline release page](https://clawhub.ai/pagoda111king/skills/data-pipeline)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript code snippets and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include pipeline stage definitions, transformer and validator usage, error-handling patterns, metrics guidance, and test commands.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact package.json reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
