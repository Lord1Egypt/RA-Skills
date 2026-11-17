## Description:

AKM Fashion models body context, scenes, wardrobe assets, and functional constraints before producing wardrobe-aware outfit and purchase decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sirsws](https://clawhub.ai/user/sirsws)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to collect a reusable fashion profile and make scene-aware outfit or purchase decisions from real wardrobe, body, preference, and function constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may share body, wardrobe, lifestyle, or preference details while building the fashion profile.

Mitigation: Ask only for details needed for the styling decision and advise users to omit anything they are not comfortable storing in a styling profile.

Risk: The optional CLI install command references a repository without a pinned release or commit.

Mitigation: Prefer the ClawHub listing or a pinned release or commit before installation when reproducibility or supply-chain review is required.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/sirsws/skills/akm-fashion-strategist)
- [Public sample record](https://github.com/sirsws/akm/blob/main/branches/fashion/skill/SAMPLE_RECORD.md)
- [AKM fashion research paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6231466)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown with named decision sections such as SceneJudgment, OutfitRecommendation, GapAnalysis, PurchasePriority, and MissingInputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May elicit a structured FashionProfile before recommendations; exposes missing inputs when wardrobe, body, scene, or functional details are insufficient.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
