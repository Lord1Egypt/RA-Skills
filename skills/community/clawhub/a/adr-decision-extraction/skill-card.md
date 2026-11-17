## Description:

Extracts architectural decisions from conversations, session transcripts, or design discussions before ADR writing by identifying problem-solution pairs, trade-offs, technology choices, and explicit [ADR] tags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn design discussions and session transcripts into structured decision records for downstream ADR writing. It prepares JSON decision summaries with confidence and context rather than authoring full ADR documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Extraction output may include confidential details or secrets from the conversations and transcripts supplied by the user.

Mitigation: Review and redact source material and generated decision summaries before sharing or publishing them.

Risk: Inferred architectural decisions can be incomplete or misleading when the source discussion is ambiguous.

Mitigation: Verify low-confidence decisions against the original discussion before using them as ADR inputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anderskev/skills/adr-decision-extraction)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [JSON object, typically shown in a Markdown code block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Decision objects include title, problem, chosen option, alternatives, drivers, confidence, and source context; low-confidence items should explain what was missing, weak, or contradictory.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
