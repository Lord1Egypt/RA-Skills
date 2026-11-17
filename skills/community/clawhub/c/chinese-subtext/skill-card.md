## Description:

Interprets subtext in Chinese conversations, chats, and emails when the user provides enough context to assess whether a phrase is a polite refusal, hint, complaint, pleasantry, probe, or other indirect intent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chujindan-dotcom](https://clawhub.ai/user/chujindan-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to understand likely subtext in Chinese interpersonal, workplace, business, family, and social conversations. The skill asks for missing relationship, scene, exact wording, and prior-context details before giving a grounded reading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may present subjective social readings too confidently for relationships, workplace disputes, legal issues, or other major decisions.

Mitigation: Treat outputs as hypotheses based only on the supplied conversation and verify important matters through direct communication or appropriate professional advice.

Risk: Users may provide sensitive conversation text for analysis.

Mitigation: Share only conversation content that is appropriate to disclose to the agent and avoid unnecessary private, confidential, or identifying details.

## Reference(s):

- [High-Frequency Chinese Subtext Scenario Patterns](references/scenarios.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown analysis with quoted phrase-by-phrase interpretation and optional response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided conversation context; includes a fixed disclaimer that readings are not factual determinations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
