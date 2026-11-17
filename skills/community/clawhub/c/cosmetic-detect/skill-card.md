## Description:

Analyzes facial or body photos for possible signs of cosmetic surgery or aesthetic procedures using probabilistic, limitation-aware visual indicators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deusyu](https://clawhub.ai/user/deusyu)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to review uploaded images or before/after comparisons for cautious, non-diagnostic observations about possible cosmetic or aesthetic procedures. The skill is intended to return uncertainty-aware visual analysis, not factual determinations about identity, health, ethnicity, age, or cosmetic history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to make sensitive appearance-based judgments about ethnicity, age, cosmetic procedures, and naturalness from photos.

Mitigation: Do not use outputs as factual determinations or for employment, insurance, healthcare, identity, moderation, or reputational decisions.

Risk: Analyzing private individuals or third-party images can create consent and reputational risks.

Mitigation: Use only with appropriate consent and avoid analyzing private people or third-party images without permission.

Risk: Image quality, lighting, makeup, filters, editing, genetics, aging, and weight changes can produce misleading indicators.

Mitigation: State visible limitations, use low/medium/high confidence labels, and phrase findings as possible or suggestive rather than certain.

## Reference(s):

- [Cosmetic Surgery Detection: Region-by-Region Analysis Guide](references/analysis-framework.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown analysis report with confidence labels, regional observations, overall assessment, and disclaimer]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses probability language and depends heavily on image quality, lighting, angle, makeup, filters, and editing.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
