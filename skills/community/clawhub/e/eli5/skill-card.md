## Description:

Explains complex topics in simple words with analogies, concrete examples, no jargon, and freshness notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coghost](https://clawhub.ai/user/coghost)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use ELI5 to turn complex concepts into approachable explanations for non-experts. It is also useful as a self-check for whether the explainer understands a topic well enough to explain it with familiar analogies and concrete examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Simplified explanations can omit important details or make an analogy feel more complete than the underlying understanding.

Mitigation: Use ELI5 for orientation and self-checking, then verify precise, technical, mathematical, or high-stakes content against authoritative sources.

Risk: Optional web fetching can disclose the requested topic to web search or external retrieval systems.

Mitigation: Enable fetch only for topics appropriate to send to web search; leave fetch off for sensitive or private topics.

Risk: Fast-moving topics and real-time news can be stale or unsuitable for simplified judgment.

Mitigation: Use the freshness indicator as a prompt to fetch current information, and treat real-time or exact-answer use cases as requiring independent validation.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown explanations with short command responses and freshness indicators]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional web fetching depends on host capability; language and step count can be adjusted by command or environment setting.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
