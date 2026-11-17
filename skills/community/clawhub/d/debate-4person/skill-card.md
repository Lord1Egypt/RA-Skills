## Description:

A Chinese-language structured debate assistant that has AI roleplay affirmative and negative debate teams, run opening, cross-examination, rebuttal, and summary rounds, and optionally provide judge commentary and scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[woqigeshenmemingzibijiaoheshine](https://clawhub.ai/user/woqigeshenmemingzibijiaoheshine)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to simulate a standard Chinese four-person debate workflow for debate practice, scenario simulation, and assessment. The skill can use web search for supporting evidence when Tavily credentials are available, otherwise it falls back to the agent's general knowledge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive personal, workplace, legal, medical, or private debate topics may be transformed into web search queries when Tavily-backed search is used.

Mitigation: Avoid entering sensitive topics unless the user is comfortable with those topics or derived queries being sent to Tavily or web search.

Risk: Debate arguments and cited evidence may be incomplete or inaccurate, especially when search is unavailable and the skill falls back to general model knowledge.

Mitigation: Review important claims before relying on debate output for training, assessment, or decision-making.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/woqigeshenmemingzibijiaoheshine/skills/debate-4person)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Chinese-language Markdown or plain text debate transcript, judge commentary, scores, and improvement guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require TAVILY_API_KEY for Tavily-backed search evidence; otherwise uses the agent's general knowledge.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
