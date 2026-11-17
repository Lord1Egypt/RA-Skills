## Description:

Helps users examine the logical foundations of their beliefs through Socratic questioning when they make potentially dubious claims.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asgraf](https://clawhub.ai/user/asgraf)

### License/Terms of Use:


## Use Case:

External users and agent developers use this skill to guide respectful Socratic examination of potentially questionable claims, especially around sensitive or controversial topics. It can support offline reasoning or external fact-checking when the user explicitly consents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive beliefs, reasoning history, conclusions, or inferred emotional state may be retained by an agent with memory.

Mitigation: Use only with explicit, minimal, opt-in memory behavior, and give users a clear way to decline or remove stored discussion state.

Risk: The artifact includes memory behavior after a user declines to continue a discussion.

Mitigation: Disable silent persistence after opt-out, and require user consent before saving postponed claim stacks or emotional-state notes.

Risk: External verification can transmit user claims to search, fact-checking, or other services.

Mitigation: Keep external verification consent-based and disclose which tool or service will receive the claim before use.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Conversational Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May suggest external verification only with user consent; may also guide offline Socratic questioning.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
