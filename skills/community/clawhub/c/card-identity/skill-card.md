## Description:

Resolve a card name to an exact issuer, family, and variant before card research when shorthands, ambiguous names, or personal-versus-business variants appear.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiahongc](https://clawhub.ai/user/jiahongc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill before credit card research to resolve a shorthand or ambiguous card name into a specific issuer, family, and variant. When the match is unsupported, ambiguous, or unavailable, the skill returns a clear stop message or numbered options instead of merging facts across variants.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill appears to depend on shared card-rule files that are not included in this artifact, so behavior may be incomplete without companion shared rules.

Mitigation: Install and review the referenced card-shared rule files before relying on the skill in a card research workflow.

Risk: Ambiguous card names can refer to both personal and business variants.

Mitigation: Stop and present numbered choices when the requested variant is not clear, and do not merge facts across variants.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/jiahongc/skills/card-identity)
- [Source policy](../card-shared/source-policy.yaml)
- [Card identity rules](../card-shared/card-identity-rules.md)
- [Normalization rules](../card-shared/normalization-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Concise text or markdown with optional hidden YAML identity keys and numbered choices]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May stop with an unsupported issuer, ambiguous choice list, or no-match message.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
