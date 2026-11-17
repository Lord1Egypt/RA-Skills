## Description:

Builds structured scorecard dimensions, observable behaviors, examples, coaching recommendations, and review cadence for sales, support, or interview calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, support, and interview teams use this skill to turn call goals, roles, and good or bad examples into reviewable coaching scorecards. It is intended for training and quality review, not as a replacement for formal human evaluation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated scorecards may be mistaken for final evaluation decisions.

Mitigation: Use outputs as reviewable coaching drafts and keep human review before performance, quality, or personnel decisions.

Risk: Call transcripts or business context may include sensitive personal, customer, or business information.

Mitigation: Provide only content intended for local processing and de-identify sensitive material before use.

Risk: Dormant audit modes can inspect local files or repositories if the resource configuration is changed.

Mitigation: Leave resources/spec.json in structured_brief mode unless local repository or file inspection is deliberately reviewed and authorized.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/52yuanchangxing/skills/call-scorecard-builder)
- [Skill Definition](artifact/SKILL.md)
- [Output Specification](artifact/resources/spec.json)
- [Output Template](artifact/resources/template.md)
- [Example Output](artifact/examples/example-output.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown by default; JSON wrapper available from the local script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local input only; the script can write the generated report to a requested output path.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
