## Description:

Detect hype cycles and neutralize emotional triggers by rewriting claims into verifiable structures and explicit risk/uncertainty.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzfshark](https://clawhub.ai/user/mzfshark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, community managers, analysts, and agent users can use this skill to evaluate hype-heavy messages, identify unsupported urgency or certainty, and convert claims into evidence-seeking responses with explicit risk and uncertainty.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generic hype trigger words can activate the filter when the user did not intend anti-hype review.

Mitigation: Use the skill when hype filtering is requested or when the message clearly contains urgency, certainty, vague upside, or unsupported social-proof claims.

Risk: A message may be framed as manipulation risk without enough context.

Mitigation: Label risk rather than intent, avoid accusations of malice, and require falsifiable evidence requests before treating the message as manipulation risk.

## Reference(s):

- [Anti-Hype Filter ClawHub page](https://clawhub.ai/mzfshark/skills/anti-hype-filter)
- [Publisher profile](https://clawhub.ai/user/mzfshark)

## Skill Output:

**Output Type(s):** [Text, Analysis, Guidance]

**Output Format:** [Structured text with anti_hype_result fields for classification, detected triggers, missing information, rewrite, and response draft]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May apply max_response_words guidance; default response draft target is 100 words when policy does not override it.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
