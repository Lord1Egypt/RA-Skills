## Description:

Turns supplied materials into a reviewable presentation or deck narrative structure with per-slide titles, evidence needs, transition logic, risk pages, and final actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external teams, and presentation authors use this skill to convert supplied audience, conclusion, and evidence materials into a structured Markdown deck plan for review before design or execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may produce incomplete or misleading deck guidance if the supplied materials omit audience, conclusion, or evidence.

Mitigation: Require human review of the draft, preserve open questions as confirmation items, and avoid treating generated slide titles as verified facts.

Risk: Sensitive presentation materials may be included in local inputs.

Mitigation: Use the skill only on intended presentation files and redact personal or confidential information before processing broad document sets.

Risk: Unused audit helper routines in the script could be misunderstood as part of the normal deck workflow.

Mitigation: Treat the normal workflow as local deck-outline generation; separately review audit routines before repurposing them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/52yuanchangxing/skills/deck-narrative-planner)
- [README](artifact/README.md)
- [Structured Specification](artifact/resources/spec.json)
- [Output Template](artifact/resources/template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown deck outline, with optional JSON report from the local helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local input content and a fixed section structure; no network access or third-party Python dependencies are required.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
