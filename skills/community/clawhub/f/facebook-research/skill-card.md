## Description:

Searches Facebook Marketplace listings and looks up public Facebook Page details (name, follower/like counts, category, contact info) via the Crawlora API, returning clean JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to research public Facebook Marketplace listings by location, category, or query and to retrieve public Facebook Page profile details without browser automation or a logged-in session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Facebook search terms, page identifiers, and the Crawlora API key are sent to Crawlora.

Mitigation: Set CRAWLORA_API_KEY only in the environment, review requests before execution, and avoid sending sensitive identifiers.

Risk: Results may include public business contact details from Facebook Pages.

Mitigation: Use returned contact details in line with Facebook terms and applicable privacy expectations.

## Reference(s):

- [Endpoint reference](reference/endpoints.md)
- [Crawlora](https://crawlora.net)
- [Crawlora API base](https://api.crawlora.net/api/v1)
- [ClawHub skill page](https://clawhub.ai/crawlora-org/skills/facebook-research)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CRAWLORA_API_KEY; requests are limited to documented GET routes for public Facebook Marketplace and Page data.]

## Skill Version(s):

1.0.16 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
