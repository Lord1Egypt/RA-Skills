## Description:

Checks meeting summaries for evidence, owner and date confirmation, privacy, and attribution to ensure output is accurate, clear, and ready for sharing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mindbomber](https://clawhub.ai/user/mindbomber)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and teams use this skill to review meeting summaries, minutes, action items, decisions, and follow-ups before sharing or applying them. It helps ensure claims, owners, dates, and privacy handling are grounded in transcript, notes, chat, agenda, calendar, or other available evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting summaries can create unsupported decisions, commitments, owners, dates, or attributions.

Mitigation: Require transcript, notes, chat, agenda, calendar, or other evidence; label uncertainty; and request confirmation before sharing.

Risk: Meeting content can include private, customer, employee, legal, financial, health, or confidential details.

Mitigation: Redact or minimize sensitive content and route high-impact or public-facing notes to review.

Risk: Using an external checker can expose more meeting content than needed.

Mitigation: Configure approved checker interfaces deliberately and send only minimal redacted payloads.

## Reference(s):

- [Skill instructions](artifact/SKILL.md)
- [README](artifact/README.md)
- [Meeting summary checker schema](artifact/schemas/meeting-summary-checker.schema.json)
- [Redacted meeting summary checker example](artifact/examples/redacted-meeting-summary-checker.json)
- [ClawHub skill page](https://clawhub.ai/mindbomber/skills/aana-meeting-summary-checker)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown or text checklist with status labels and recommended actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only; may use the bundled JSON schema for minimal redacted checker payloads.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
