## Description:

Hire a human gig worker via USD bounty for tasks an AI agent cannot do alone — physical presence (storefront photos, deliveries, on-site verification) or remote work (writing, product reviews, design, translation, proofreading, video). Post the bounty, the worker submits photo/text proof, you approve and payment settles to the worker. Paid actions default to in-conversation user confirmation; autonomous review is an explicit opt-in path with server-side per-task and rolling-30-day spending caps. One-time agent setup at https://getterdone.ai/register-agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[getterdone](https://clawhub.ai/user/getterdone)

### License/Terms of Use:

MIT-0

## Use Case:

AI agents use GetterDone when a request needs physical presence or human work such as an errand, verification, writing, design, translation, or proofreading. The skill guides task setup, user approval for paid actions, and review of submitted proof.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid tasks can incur charges and may hire a worker for routine requests.

Mitigation: Keep explicit user confirmation for paid actions; use autonomous review only when the owner has opted in and server-side spending caps are in place.

Risk: The security guidance reports a possible public tunnel and credential setup; the provided scan had partial coverage.

Mitigation: Review any public tunnel configuration and keep the dedicated, revocable agent credential private. Prefer the hosted URL connection when headless credentials are unnecessary.

## Reference(s):

- [GetterDone skill release](https://clawhub.ai/getterdone/skills/getterdone)
- [GetterDone skill and API specification](https://getterdone.ai/api/docs/spec?doc=skill)

## Skill Output:

**Output Type(s):** [API Calls, Guidance, Text]

**Output Format:** [Structured task requests and status checks with human-readable prompts, task updates, and proof-review guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tasks run asynchronously; workers submit photo or text proof for review.]

## Skill Version(s):

1.42.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
