## Description:

Guides agents through submitting and managing CurlShip directory listings, including optional paid upgrades and featured bids.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcindudekdev](https://clawhub.ai/user/marcindudekdev)

### License/Terms of Use:

MIT-0

## Use Case:

Product owners and agents use this skill to publish and maintain public CurlShip directory listings and optionally purchase higher placement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitting a listing shares the product URL, owner email, and listing details with CurlShip and makes the listing public.

Mitigation: Require explicit approval before submission and confirm the URL, contact email, and public-listing impact.

Risk: Upgrades and featured bids can incur charges; an agent may sign an on-chain USDC payment without a checkout page, and an outbid featured listing has no refund.

Mitigation: Require explicit approval before checkout, bidding, or USDC signing; verify the quoted amount, destination, payment terms, and refund policy.

Risk: Edits, URL changes, and removals can alter or take down a public listing.

Mitigation: Require explicit approval and verify the target listing and intended change before applying it.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/marcindudekdev/skills/curlship)
- [CurlShip homepage](https://curlship.com)
- [CurlShip agent actions](https://curlship.com/agents.md)
- [CurlShip agent tools](https://curlship.com/agents.json)
- [CurlShip listing edits](https://curlship.com/edit)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls]

**Output Format:** [Markdown with curl examples and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Listings are public; paid actions may involve card checkout or USDC signing.]

## Skill Version(s):

1.3.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
