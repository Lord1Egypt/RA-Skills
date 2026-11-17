## Description:

Hook and opening optimization for Chinese short-form content that diagnoses weak first seconds or sentences, checks whether the underlying material can support a strong opening, and generates multiple opening directions that match the content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cellinlab](https://clawhub.ai/user/cellinlab)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, content teams, and agent users use this skill to diagnose and improve Chinese short-form openings. It helps determine whether the opening is weak or the source material is under-fueled, then produces a concise hook pack with several viable directions and top recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default template and workflow are Chinese-focused, so results may be less suitable for other languages unless requested.

Mitigation: Ask the agent to respond in the desired language when the target content is not Chinese.

Risk: Opening suggestions can overpromise when the source material lacks a concrete result, contradiction, scene, detail, or judgment.

Mitigation: Use the skill's content viability diagnosis before accepting generated hooks, and strengthen the underlying material when it is marked under-fueled.

## Reference(s):

- [开头原则](references/hook-principles.md)
- [常见 Hook 类型](references/hook-types.md)
- [Skill homepage](https://github.com/cellinlab/cell-skills/tree/main/skills/hook-optimizer)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown hook pack with diagnostic notes, extracted materials, multiple opening directions, candidate openings, and ranked recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to Chinese output and emphasizes openings that the provided body can actually support.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
