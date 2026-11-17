## Description:

Analyze DNA, RNA, and protein sequences with alignment, variant calling, and expression analysis pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers, bioinformaticians, and research teams use this skill to inspect sequencing inputs, plan reproducible genomic workflows, and generate command guidance for alignment, variant calling, RNA-seq analysis, and sequence file conversion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store bioinformatics project context and activation preferences across sessions, including sensitive sample, patient, unpublished, or regulated study details if the user asks it to save them.

Mitigation: Keep persistence limited to ~/bioinformatics/memory.md, ask before saving sensitive information, and review or delete that file when sensitive context should not be retained.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/bioinformatics)
- [Skill homepage](https://clawic.com/skills/bioinformatics)
- [Setup](artifact/setup.md)
- [Memory Template](artifact/memory-template.md)
- [File Formats](artifact/formats.md)
- [Tool Reference](artifact/tools.md)
- [RNA-seq Pipeline](artifact/rnaseq.md)
- [Variant Calling Pipeline](artifact/variants.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell, Python, and R code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory and may include local command sequences, pipeline plans, file-format checks, and configuration notes for user-provided bioinformatics data.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
