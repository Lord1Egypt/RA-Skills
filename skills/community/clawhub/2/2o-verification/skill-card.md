## Description:

Human verification for AI agents. Submit claims, draft responses, or observation requests to human domain experts via the 2O API. Returns structured verdicts with confidence scores and evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[russellshen1992](https://clawhub.ai/user/russellshen1992)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to request human review of factual claims, sensitive draft responses, and real-world observation tasks through the 2O API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted text, context, and location details may be shared with the 2O service and human reviewers.

Mitigation: Get explicit user approval before sending content, and remove secrets, regulated personal data, private addresses, exact GPS coordinates, and photos unless they are necessary and approved.

Risk: Witness observation requests may enable tracking, surveillance, harassment, or physical harm.

Mitigation: Decline or narrow requests that could identify, locate, monitor, or endanger a person; use coarse or non-sensitive location context when possible.

Risk: The skill can create paid external requests.

Mitigation: Confirm the intended task type, budget, urgency, and consent before submitting API calls that spend credits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/russellshen1992/skills/2o-verification)
- [2O API registration](https://www.2oapi.xyz/register)
- [2O factual verification endpoint](https://www.2oapi.xyz/api/v1/verify)
- [2O empathy review endpoint](https://www.2oapi.xyz/api/v1/empathize)
- [2O witness observation endpoint](https://www.2oapi.xyz/api/v1/witness)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with curl commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TWO_O_API_KEY and can create paid verification, empathy review, and witness observation requests.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
