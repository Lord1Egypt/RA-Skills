## Description:

Formats APA, MLA, Vancouver, BibTeX, or free-text citation inputs into AMA-style citation text using local parsing helpers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googolme](https://clawhub.ai/user/googolme)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and researchers can use this skill to reformat citation strings or batches of citation lines into AMA-style output before manuscript or grant-reference review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documentation claims broad citation-style conversion, validation, and reference-manager integration beyond the included local AMA formatter behavior.

Mitigation: Treat the skill as a simple AMA formatter for supported input patterns, and confirm any broader capability in code before relying on it.

Risk: Citation output may be incomplete or incorrect for publication-critical references.

Mitigation: Manually check formatted citations against the target journal requirements and authoritative reference data before submission.

Risk: Batch mode reads and writes local files supplied by command-line paths.

Mitigation: Run batch formatting in a controlled workspace and review input and output paths before execution.

## Reference(s):

- [AMA Citation Style Guide](artifact/references/ama-guidelines.md)
- [Example Citations for Testing](artifact/references/examples.md)
- [ClawHub skill page](https://clawhub.ai/googolme/skills/citation-formatter)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Plain text citation output with Markdown documentation, Python examples, and command-line examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single citation input, stdin, interactive prompts, and batch line-based file input; output should be manually checked before publication-critical use.]

## Skill Version(s):

0.1.0 (source: server release metadata and tile.json; SKILL.md metadata reports 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
