## Description:

Compares competitor messaging, information architecture, and narrative differences to identify useful lessons, avoid imitation, and surface validation suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, positioning, and competitive strategy users apply this skill to turn competitor copy, page excerpts, and audience context into a structured review of architecture differences, narrative differences, lessons, risks to avoid, differentiation opportunities, and validation suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input files and directories are visible to the agent and local helper when used for analysis.

Mitigation: Use only intended local inputs, and remove or redact personal, confidential, or sensitive material before running the skill.

Risk: Modified versions of the helper may be pointed at broad private directories or used for wider audit-style reports than the advertised messaging workflow.

Mitigation: Review modified scripts and specs before use, prefer narrow input paths, and use dry-run or review-only outputs for sensitive work.

Risk: Competitive analysis can become misleading or infringing if the agent fabricates facts or copies competitor wording.

Mitigation: Require source-backed inputs, list missing information as confirmation items, and keep outputs focused on strategy analysis rather than copied messaging.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/competitor-message-differ)
- [Output template](artifact/resources/template.md)
- [Structured skill specification](artifact/resources/spec.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Structured Markdown report; the helper script can also wrap the report in JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Python 3 local helper uses local input only, supports dry-run behavior, and can write reports to a selected output file.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
