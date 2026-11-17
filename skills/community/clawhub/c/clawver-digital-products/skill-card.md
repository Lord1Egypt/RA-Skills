## Description:

Create and sell digital products on Clawver by uploading files, setting pricing, publishing listings, and tracking downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nwang783](https://clawhub.ai/user/nwang783)

### License/Terms of Use:


## Use Case:

External creators and marketplace sellers use this skill to create, upload, publish, manage, and track downloadable digital products on Clawver.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live API commands can publish, modify, or delete Clawver marketplace listings.

Mitigation: Review commands before execution, use only an intended Clawver API key, and verify product IDs before PATCH or DELETE requests.

Risk: Commands may send digital files, file URLs, order identifiers, or product data to the live API.

Mitigation: Confirm files, URLs, order IDs, and product details are intended for Clawver before submitting requests.

## Reference(s):

- [Digital Products API Examples](references/api-examples.md)
- [Clawver](https://clawver.store)
- [ClawHub Skill Page](https://clawhub.ai/nwang783/skills/clawver-digital-products)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLAW_API_KEY and uses live Clawver API endpoints.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
