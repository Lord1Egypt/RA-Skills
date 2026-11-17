## Description:

Brand Voice Architect helps agents analyze writing samples, define brand voice systems, and generate voice guides, prompt templates, platform pivots, and preferred or prohibited lexicons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[midnightstudioai](https://clawhub.ai/user/midnightstudioai)

### License/Terms of Use:

MIT-0

## Use Case:

Brand, marketing, product, and content teams use this skill to analyze a writing corpus, document the resulting voice architecture, and generate deployable brand voice prompts and style artifacts. Developers and agent builders can use its scripts to compute voice metrics and synthesize system prompts from structured brand configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill analyzes writing samples supplied by the user, which may include sensitive brand, customer, or internal content.

Mitigation: Provide only intended corpus or JSON files and avoid including sensitive material that should not be analyzed by the agent.

Risk: Generated system prompts and prohibited-word replacements depend on the downstream model following the prompt.

Mitigation: Review and test generated prompts before deploying them in another system.

## Reference(s):

- [Technical Methodology Reference](references/methodology.md)
- [ClawHub Skill Page](https://clawhub.ai/midnightstudioai/skills/brand-voice-architect)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown, structured text, and generated system-prompt text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include metrics reports, voice matrices, system prompts, platform pivots, and prohibited or preferred lexicons.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
