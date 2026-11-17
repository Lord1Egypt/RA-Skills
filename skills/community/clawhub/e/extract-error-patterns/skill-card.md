## Description:

Extracts error patterns from server logs and generates actionable alert rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjipeng977](https://clawhub.ai/user/wangjipeng977)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and SREs use this skill to analyze server logs, classify recurring error patterns by severity, and draft alert rules with source samples for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports can copy sensitive log contents without redaction.

Mitigation: Use redacted or synthetic logs when possible, review outputs before sharing, and write reports only to controlled locations with appropriate access restrictions.

Risk: Generated Markdown reports may contain untrusted log content.

Mitigation: Review generated Markdown before rendering or publishing it, and avoid unsafe Markdown rendering paths.

Risk: The artifact documentation mentions an API key requirement without explaining why it is needed.

Mitigation: Do not provide an API key unless the publisher explains the requirement and the intended data flow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangjipeng977/skills/extract-error-patterns)
- [Publisher profile](https://clawhub.ai/user/wangjipeng977)
- [Metadata source: MiniMax-AI skills](https://github.com/MiniMax-AI/skills)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown report or JSON list of alert rules with regex patterns, counts, severity, and samples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include source log samples and can be written to a user-selected output path.]

## Skill Version(s):

1.0.1 (source: server release metadata and changelog, released 2026-05-27)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
