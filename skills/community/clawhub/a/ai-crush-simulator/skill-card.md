## Description:

A fun, safe, youth-friendly skill that helps users navigate crush situations by analyzing situations, decoding texts, generating reply options, and recommending thoughtful next moves.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vajih](https://clawhub.ai/user/vajih)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill for lightweight crush and relationship communication guidance, including reading social signals, interpreting ambiguous texts, drafting respectful replies, and choosing a next move. The skill is framed for youth-friendly, G-rated use with no certainty claims about another person's feelings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat crush or relationship advice as factual knowledge about another person's feelings.

Mitigation: Keep the 'based on what you shared' disclaimer visible and frame all outputs as lightweight suggestions rather than facts or predictions.

Risk: The reply generation feature omits the promised disclaimer.

Mitigation: Add or verify a disclaimer on reply outputs before relying on the skill in user-facing flows.

Risk: Development dependencies may need routine maintenance.

Mitigation: Refresh and review development dependencies before packaging or redistributing the skill.

## Reference(s):

- [AI Crush Simulator on ClawHub](https://clawhub.ai/vajih/skills/ai-crush-simulator)
- [Publisher profile: vajih](https://clawhub.ai/user/vajih)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured plain text or Markdown with scores, possible readings, reply options, recommendations, tips, and disclaimers.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Heuristic scores are bounded from 0 to 100; reply generation returns Bold, Chill, and Safe options.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
