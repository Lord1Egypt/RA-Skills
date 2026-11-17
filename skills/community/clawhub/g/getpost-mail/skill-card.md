## Description:

Buy shipping labels, get rates, and track parcels via API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dommholland](https://clawhub.ai/user/dommholland)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to call the GetPost mail API for shipping rates, label purchases, and parcel tracking. It is suited to workflows where an agent drafts or executes shipping API requests with user-approved shipment data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable live shipping label purchases with a production API key.

Mitigation: Use test or redacted data first and require explicit user approval before buying labels with a live key.

Risk: Shipping requests may send names, addresses, parcel details, and tracking identifiers to a third-party service.

Mitigation: Store API keys securely, minimize address data, and confirm user consent before sending shipment details.

## Reference(s):

- [GetPost Mail API Documentation](https://getpost.dev/docs/api-reference#mail)
- [ClawHub Skill Page](https://clawhub.ai/dommholland/skills/getpost-mail)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance]

**Output Format:** [Markdown with curl examples and API request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a GetPost API key; live label purchases should require explicit user approval.]

## Skill Version(s):

1.0.0 (source: server evidence release version and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
