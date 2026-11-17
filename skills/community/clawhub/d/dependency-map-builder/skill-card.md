## Description:

Builds cross-team dependency maps, identifies critical paths and fragile nodes, and produces textual dependency diagrams and risk chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineering managers, and program leads use this skill to turn task lists, owner teams, and sequencing constraints into reviewable dependency maps, critical-path notes, escalation points, and follow-up checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive project details or personal data in local input files may appear in generated dependency maps.

Mitigation: Use only files intended for analysis, redact sensitive content before sharing outputs, and prefer dry-run or stdout for sensitive inputs.

Risk: Shell examples can be misused when paths are interpolated unsafely.

Mitigation: Quote paths or invoke the helper script through an argument-array API instead of concatenating shell strings.

Risk: Changing resources/spec.json to an audit mode can broaden local scanning beyond the normal dependency-map workflow.

Mitigation: Keep the default structured_brief mode unless broader local scanning is explicitly desired and reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/dependency-map-builder)
- [Skill manifest](artifact/SKILL.md)
- [Specification](artifact/resources/spec.json)
- [Output template](artifact/resources/template.md)
- [Smoke test](artifact/tests/smoke-test.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown dependency reports with optional JSON output from the local helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Mermaid drafts, review checklists, escalation points, and explicit items needing confirmation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
