## Description:

Creates and populates Annotated Research Contexts (ARCs) following the nfdi4plants ARC specification, guiding users through investigation, study, assay, workflow, run, metadata, and DataHUB sync steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ingogiebel](https://clawhub.ai/user/ingogiebel)

### License/Terms of Use:


## Use Case:

Researchers, data stewards, and developers use this skill to organize experimental research data into nfdi4plants ARC structures, collect ISA metadata, and prepare local Git-backed ARCs for optional DataHUB publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied metadata and paths could be executed as shell syntax if copied directly into command templates.

Mitigation: Pass collected values as separate command arguments, validate local paths, and escape shell-sensitive values before execution.

Risk: A DataHUB push could upload unpublished research data or personal contact details to the wrong host, repository, or visibility setting.

Mitigation: Before pushing, confirm the DataHUB host, repository visibility, credentials in use, and the data or contact details included.

## Reference(s):

- [ARC Specification Reference](references/arc-spec.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local filesystem, Git, and DataHUB operations for user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
