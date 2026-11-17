## Description:

Felo Twitter Writer helps agents analyze Twitter/X account style into Style DNA and compose tweets, threads, or long-form X posts through Felo SuperAgent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangzhiming1999](https://clawhub.ai/user/wangzhiming1999)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze public Twitter/X writing style, extract a reusable Style DNA document, and draft tweets, threads, or long-form X posts in a selected or referenced style.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can attach to the most recently modified private Felo LiveDoc, which may be unrelated to Twitter writing.

Mitigation: Create a fresh Twitter Writer LiveDoc or explicitly choose the intended document before running the skill.

Risk: Generated tweet and style-analysis content is returned from an external Felo service and the skill instructs the agent to output it verbatim.

Mitigation: Review outputs for accuracy, tone, privacy, and brand fit before publishing or reusing them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangzhiming1999/skills/felo-twitter-writer)
- [Felo Open Platform](https://openapi.felo.ai/docs/)
- [Felo SuperAgent API Reference](https://openapi.felo.ai/docs/api-reference/v2/superagent.html)
- [Felo Skills GitHub Repository](https://github.com/Felo-Inc/felo-skills)
- [Felo Skills Support](https://github.com/Felo-Inc/felo-skills/issues)
- [Felo](https://felo.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or plain text, with shell commands for setup and agent execution paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FELO_API_KEY; generated writing output is returned from Felo SuperAgent and should be reviewed before publication.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact/clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
