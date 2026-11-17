## Description:

Decision-making advisor using Tree of Thoughts for exploring options, analyzing trade-offs, and providing data-driven recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[banxian87](https://clawhub.ai/user/banxian87)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical teams, business users, and individuals use this skill to compare options, define weighted criteria, analyze trade-offs, and generate structured decision recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Decision prompts can contain confidential business or personal details that may be sent to the configured LLM backend.

Mitigation: Use a trusted LLM backend and avoid entering sensitive information unless sharing it with that backend is approved.

Risk: Generated scores and recommendations can be incomplete or misleading for consequential decisions.

Mitigation: Treat outputs as decision support and review the criteria, assumptions, scores, and recommendation before acting.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured text or Markdown decision analysis with scores, reasoning, risks, alternatives, and a recommendation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the configured LLM backend when generating options, criteria, and scores; falls back to simple default scoring behavior when no backend is provided.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
