## Description:

Converts TXT, Markdown, DOCX, and PDF documents into a reusable skill ZIP with normalized Markdown, extracted images, and a grounded JSONL knowledge index.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jarvisyaoht](https://clawhub.ai/user/jarvisyaoht)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and agent builders use DocToSkill to turn uploaded document sets into portable retrieval skills that an agent can install and query.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted document text can influence generated skills.

Mitigation: Review generated skills before sharing, installing, or using them in a trusted agent workspace.

Risk: The build step can package unintended asset files.

Mitigation: Use fresh task directories and do not allow attacker-controlled files or symlinks in the assets directory.

Risk: PDF conversion can invoke an unexpected pdftoppm binary if PDFTOPPM_BIN is set unsafely.

Mitigation: Leave PDFTOPPM_BIN unset or point it only to a trusted pdftoppm binary.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jarvisyaoht/skills/doc-to-skill)
- [Batch indexing contract](references/indexing.md)
- [Skill metadata contract](references/metadata.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell commands, JSON metadata, JSONL index data, and a generated skill ZIP path.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a self-contained skill archive that packages normalized Markdown, extracted assets, a retrieval index, agent metadata, and a search helper.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
