## Description:

Checks embedded C MCU register writes against a chip's CMSIS SVD and groups the results into reported, undetermined, and passed findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liujycode](https://clawhub.ai/user/liujycode)

### License/Terms of Use:

MIT-0

## Use Case:

Embedded developers use it to review register writes in initialization code and AI-generated firmware against the target chip's SVD before flashing; it can also provide a grouped review checklist.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flagged a mismatch between reported capabilities and the stated firmware review purpose; its analysis is incomplete, and some unresolvable register writes may be marked as passed.

Mitigation: Review the lookup and reference behavior, manually inspect unresolvable writes, and verify hardware-specific results against the target chip's official SVD or datasheet.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/liujycode/skills/embedded-register-verify)
- [Register verification rules](references/rules.md)
- [Supported syntax and limitations](references/syntax.md)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON]

**Output Format:** [Plain text or JSON, with an optional grouped review checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are grouped as reported, undetermined, and passed; hardware-specific checks require the matching device SVD.]

## Skill Version(s):

1.17.0 (source: SKILL.md frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
