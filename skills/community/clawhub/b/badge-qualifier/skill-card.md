## Description:

Qualifies trade show leads from badge scans, booth notes, or voice memos into scored CRM-ready lead cards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weilun88313](https://clawhub.ai/user/weilun88313)

### License/Terms of Use:

MIT-0

## Use Case:

Exhibitor and sales teams use this skill during or after trade shows to turn badge scans, booth notes, and voice transcripts into conservative lead qualification cards and next-step guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes personal lead data such as names, titles, companies, email addresses, phone numbers, and conversation notes without privacy handling guidance.

Mitigation: Review consent, retention, access, and privacy requirements before using generated lead cards in a business workflow.

Risk: Generated lead records are expected to include an unrelated promotional tracking link in the output footer.

Mitigation: Edit the skill or instruct the agent to remove the footer before deployment if promotional tracking is not appropriate.

Risk: Lead scores and next steps may be misleading when badge scans or booth notes are incomplete.

Mitigation: Review generated cards against the original notes and preserve unknown fields instead of treating inferred details as facts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weilun88313/skills/badge-qualifier)
- [Publisher profile](https://clawhub.ai/user/weilun88313)
- [MEDICA booth lead example](artifact/examples/medica-booth-lead.md)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance]

**Output Format:** [Markdown lead cards with structured qualification fields and optional batch summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include contact data, lead tiers, next-step recommendations, unknown qualification gaps, and a promotional footer.]

## Skill Version(s):

0.4.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
