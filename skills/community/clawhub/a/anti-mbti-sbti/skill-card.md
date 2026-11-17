## Description:

Runs a Chinese-language entertainment personality quiz by asking about 30 questions, scoring 15 dimensions, and matching the user to one of 27 SBTI personality results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxgc](https://clawhub.ai/user/sxgc)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill for an entertainment-only Chinese-language personality quiz. The skill guides a conversational test, scores answers in the current chat, and presents a playful SBTI type result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: One bundled result contains an unrelated payment request, and the skill tells the agent to repeat result descriptions unchanged.

Mitigation: Review result text before deployment and remove payment requests or unacceptable labels from user-facing responses.

Risk: The quiz uses edgy humor and harsh joking labels that may not fit all user populations or brand contexts.

Mitigation: Limit deployment to users who want this entertainment style and add clear framing that results are playful, not diagnostic.

Risk: Some bundled reference files contain invalid JSON syntax due unescaped quotation marks, which may prevent strict JSON parsers from loading the quiz data.

Mitigation: Validate and repair reference JSON before packaging or runtime use.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sxgc/skills/anti-mbti-sbti)
- [Skill instructions](artifact/SKILL.md)
- [Question set 1](artifact/references/questions-1.json)
- [Question set 2](artifact/references/questions-2.json)
- [Special questions](artifact/references/questions-special.json)
- [Personality types](artifact/references/types.json)
- [Dimension definitions](artifact/references/dimensions.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Conversational Markdown with quiz prompts, scoring summary, and personality result text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces entertainment-only results; user answers are intended to remain in the current conversation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
