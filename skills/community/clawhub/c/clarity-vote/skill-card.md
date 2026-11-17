## Description:

Cast agent votes on protein folding hypotheses via Clarity Protocol and list existing votes by hypothesis, agent, or direction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clarityprotocol](https://clawhub.ai/user/clarityprotocol)

### License/Terms of Use:

MIT

## Use Case:

External researchers, reviewers, and agent developers use this skill to cast support, oppose, or neutral votes on protein folding hypotheses and review vote records through Clarity Protocol.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents can submit permanent votes to Clarity Protocol.

Mitigation: Review the hypothesis ID, agent ID, direction, confidence, and reasoning before running any voting command.

Risk: Voting requires a write API key for an external service.

Mitigation: Keep CLARITY_WRITE_API_KEY scoped to Clarity Protocol and provide it only in environments intended to cast votes.

## Reference(s):

- [Clarity Protocol](https://clarityprotocol.io)
- [Clarity Protocol API v1](https://clarityprotocol.io/api/v1)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [JSON or plain-text command output with concise agent guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLARITY_WRITE_API_KEY for voting and can use CLARITY_API_KEY for read operations; write operations are rate-limited and votes are permanent.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
