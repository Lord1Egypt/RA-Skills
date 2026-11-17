## Description:

Captures clipboard snippets into a local knowledge base by adding source context, tags, importance notes, follow-up actions, and suggested archive locations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn clipboard text, source notes, and tagging intent into reviewable Markdown knowledge cards and follow-up checklists for a local notes workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags this release as suspicious because the bundled script contains local audit and scanning modes beyond the headline clipboard-capture workflow.

Mitigation: Review before installing if a narrow clipboard formatter was expected, run it only on deliberate non-sensitive local inputs, and avoid pointing it at broad private directories.

Risk: Clipboard material may contain secrets, personal data, or claims without source context that could be copied into a knowledge base.

Mitigation: Redact sensitive content before use, require source information, and treat generated cards and action checklists as reviewable drafts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/clipboard-knowledge-capture)
- [README](artifact/README.md)
- [Skill specification](artifact/resources/spec.json)
- [Output template](artifact/resources/template.md)
- [Smoke test](artifact/tests/smoke-test.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Structured Markdown brief or JSON report, with optional local file output from the bundled Python script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 only; supports dry-run behavior and reviewable drafts before any execution or follow-up action.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
