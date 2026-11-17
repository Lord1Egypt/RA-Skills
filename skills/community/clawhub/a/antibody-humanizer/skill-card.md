## Description:

Humanize murine antibody sequences using CDR grafting and framework optimization to reduce immunogenicity while preserving antigen binding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and bioinformatics teams use this skill to analyze murine VH/VL antibody sequences, identify CDR regions, select human framework candidates, and generate computational humanization reports for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential antibody sequences may be exposed if users send them to patent databases or other external services without organizational approval.

Mitigation: Use approved data-handling workflows for proprietary sequences and review any external database steps before running them.

Risk: The skill presents computational humanization and immunogenicity outputs that may be mistaken for validated therapeutic guidance.

Mitigation: Treat the results as rough computational suggestions and require expert review plus experimental validation before candidate selection.

Risk: The release includes unnecessary or unpinned dependencies for automated installation.

Mitigation: Remove or pin dependencies before automated installation and review the package in a controlled environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/antibody-humanizer)
- [ClawHub publisher profile](https://clawhub.ai/user/aipoch-ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with Python and shell examples, plus generated JSON, FASTA, or CSV result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include input antibody sequences, CDR annotations, ranked humanization candidates, humanness scores, risk labels, and back-mutation recommendations.]

## Skill Version(s):

0.1.0 (source: server release metadata, released 2026-03-18)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
