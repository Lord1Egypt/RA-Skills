## Description:

Builds and manages reusable Cargo audience segments, counts matching records, and shows membership changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Cargo workspace users and developers use the skill to define reusable audiences, count or preview matching records, and inspect which records joined or left a segment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnostic reports may contain sensitive information, and the skill's security review identifies instructions that could submit them without user review.

Mitigation: Show a sanitized support report and get approval before submitting it.

Risk: Full exports and segment changes can expose data or alter an audience; the external CLI and omitted sibling instructions were not audited.

Mitigation: Require explicit authorization for full exports and segment changes, use restricted Cargo permissions, and pin a reviewed CLI version.

## Reference(s):

- [Cargo Skills repository](https://github.com/getcargohq/cargo-skills)
- [Segmentation response shapes](references/response-shapes.md)
- [Segmentation troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON filter examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands and filter examples are adapted to the requested model and audience criteria.]

## Skill Version(s):

1.2.2 (source: release evidence, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
