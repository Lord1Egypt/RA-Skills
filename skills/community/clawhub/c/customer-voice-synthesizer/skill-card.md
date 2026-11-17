## Description:

Aggregates customer feedback from support, sales, reviews, and interviews, then organizes customer voice by jobs-to-be-done and journey stage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Product, marketing, and research teams use this skill to turn interviews, reviews, support conversations, and sales notes into a reviewable customer-voice brief with JTBD categories, journey stages, pain points, value language, and validation suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer feedback may contain personal, sensitive, or confidential information.

Mitigation: Review or redact customer data before use, and choose input and output paths deliberately.

Risk: Summaries can overemphasize convenient themes or omit negative customer voices.

Mitigation: Keep negative feedback in scope, mark missing evidence as items to confirm, and review the draft before reuse.

Risk: Generated briefs may include incorrect or misleading synthesis if the source material is sparse.

Mitigation: Treat outputs as reviewable drafts, require traceability to provided input, and validate conclusions before product or marketing decisions.

Risk: Dormant audit code may confuse maintainers if the skill configuration changes later.

Mitigation: Remove or document inactive audit behavior before enabling alternate modes.

## Reference(s):

- [Customer Voice Synthesizer on ClawHub](https://clawhub.ai/52yuanchangxing/skills/customer-voice-synthesizer)
- [Output Template](resources/template.md)
- [Structured Specification](resources/spec.json)
- [Example Input](examples/example-input.md)
- [Example Output](examples/example-output.md)
- [Smoke Test](tests/smoke-test.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Structured Markdown brief, optionally JSON containing the generated report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local input material and writes to stdout or a user-selected output path; no network access required.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
