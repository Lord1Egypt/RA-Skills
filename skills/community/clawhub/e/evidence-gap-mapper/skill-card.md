## Description:

Reviews reports, proposals, or presentations to identify conclusions with weak supporting evidence and prioritize evidence-gathering next steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, reviewers, and teams use this skill to review report or presentation drafts, map unsupported claims, identify evidence gaps, and prioritize follow-up evidence collection before decisions or publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inputs may contain sensitive report, presentation, or evidence material, and the local script can read the file path supplied by the user.

Mitigation: Review and minimize inputs before use; remove sensitive material unless the local review is intended for that content.

Risk: The script can write a report file when an output path is provided.

Mitigation: Use a deliberate output path or dry-run/stdout behavior when a persistent file is not desired.

Risk: Evidence-gap recommendations can be misleading if users treat draft analysis as verified facts.

Mitigation: Use the output as an auditable review draft and verify claims against source evidence before decisions, publication, or system changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/evidence-gap-mapper)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [Output specification](artifact/resources/spec.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Structured Markdown report, with optional JSON wrapping when the local script is invoked in JSON mode.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs sections for key conclusions, evidence status, gaps, evidence collection priority, downgraded wording, next steps, and pending confirmations.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
