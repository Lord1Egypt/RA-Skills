## Description:

Looks up MCU peripheral registers, bit fields, reset values, and addresses from CMSIS SVD files, with sourced results and tools for decoding values, calculating settings, comparing definitions, and checking SVD quality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liujycode](https://clawhub.ai/user/liujycode)

### License/Terms of Use:

MIT-0

## Use Case:

Embedded developers use this skill to inspect or compare MCU register definitions, decode register values, and calculate settings from a selected SVD file. Verify hardware-specific values against the official datasheet for the target part.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment has medium confidence because one script was only partially analyzed.

Mitigation: Review the skill files before installation and verify hardware-specific register values against the official datasheet for the target part.

## Reference(s):

- [Glossary](artifact/references/glossary.md)
- [Query syntax and output fields](artifact/references/query-syntax.md)
- [SVD support](artifact/references/svd-support.md)
- [ClawHub skill page](https://clawhub.ai/liujycode/skills/embedded-register-lookup)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code]

**Output Format:** [Register lookup results, Markdown tables, JSON, and CMSIS-style C macros]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output depends on the requested query and the available SVD data.]

## Skill Version(s):

1.11.3 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
