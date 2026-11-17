## Description:

Return earning rates, caps, exclusions, activation requirements, and merchant-coding caveats for one major-US credit card.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiahongc](https://clawhub.ai/user/jiahongc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to research the earn-side details for one exact major-US credit-card variant, including rates, caps, exclusions, activation requirements, merchant-coding caveats, and confidence notes.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Credit-card earning rates, caps, exclusions, and merchant-coding caveats can change or vary by exact card variant.

Mitigation: Resolve the exact card first, prioritize the issuer page, use one approved secondary source only when issuer copy is vague, and include confidence notes.

Risk: The skill references companion card-identity and card-shared policy or contract files that may be absent in some installations.

Mitigation: Verify the companion skills or policy files are installed before relying on the referenced source rules, normalization rules, confidence rules, and formatting contract.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jiahongc/skills/card-rate)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown sections with hidden source metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on earning-rate details for a single resolved card variant; sources are kept out of the visible response.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
