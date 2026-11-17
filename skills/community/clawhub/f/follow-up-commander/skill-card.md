## Description:

Organizes meeting notes into reviewable action items, owner mappings, follow-up cadence, email drafts, next-sync topics, and open issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external collaborators, and developers can use this skill to turn meeting notes, participant roles, and priorities into structured follow-up plans and reviewable email drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting notes may contain personal, confidential, or sensitive business information.

Mitigation: Redact sensitive details before use and keep generated reports in approved local storage.

Risk: Draft follow-ups or action lists may be incomplete or inaccurate if the input notes are ambiguous.

Mitigation: Review generated drafts and confirm owners, deadlines, and open questions before sending or executing.

Risk: The helper can write a local report file when an output path is supplied.

Mitigation: Choose the output path deliberately and avoid writing sensitive reports to shared or untrusted locations.

Risk: The package includes unused audit helper code.

Mitigation: Document or remove audit behavior before exposing or relying on any audit mode.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/52yuanchangxing/skills/follow-up-commander)
- [Output Specification](resources/spec.json)
- [Output Template](resources/template.md)
- [Example Input](examples/example-input.md)
- [Example Output](examples/example-output.md)
- [Smoke Test](tests/smoke-test.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown by default, with optional JSON from the local helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can print to stdout or write a user-specified local report file; requires python3 and no third-party dependencies.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
