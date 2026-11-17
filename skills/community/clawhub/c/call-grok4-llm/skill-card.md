## Description:

Provides agent behavior guidance for call Grok4 LLM tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[urrrich](https://clawhub.ai/user/urrrich)

### License/Terms of Use:


## Use Case:

External users and developers can use this skill to guide an agent's language matching, meeting-context reading, and brainstorming response behavior for tasks framed as Grok4 LLM calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package claims to be a Grok 4 calling skill, but server security evidence says its only artifact mainly changes agent behavior and instruction hierarchy.

Mitigation: Review before installing and ask the publisher to provide narrow Grok 4 invocation instructions with clear input and output boundaries.

Risk: Meeting-minutes content may influence the agent's responses without explicit untrusted-content handling.

Mitigation: Require explicit handling for untrusted meeting-minutes content before relying on the skill in production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/urrrich/skills/call-grok4-llm)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Natural-language responses, typically Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are directed to match the user's requested or initial language.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
