## Description:

Gets local business and POI details for up to 20 POI IDs obtained from web search, including ratings, hours, and contact information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sprintmint](https://clawhub.ai/user/sprintmint)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve full local business details after obtaining POI IDs from a prior web search. It supports local business lookup, restaurant discovery, business-hours checks, and location-aware applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags a wallet-backed paid flow using an unpinned payment client.

Mitigation: Review before installing, use a pinned and reviewed payment client, prefer a low-value dedicated wallet, and confirm payment details before signing.

Risk: Optional location headers can send precise latitude and longitude.

Mitigation: Avoid sending exact coordinates unless needed; reduce coordinate precision when approximate distance is sufficient.

Risk: POI IDs are short-lived and must come from a prior web search.

Mitigation: Fetch fresh POI IDs with web search when IDs expire and do not cache IDs beyond the documented approximately 8-hour validity window.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sprintmint/skills/cpbox-local-pois)
- [x402 payment setup prerequisites](https://github.com/springmint/cpbox-skills#prerequisites)
- [CPBox API provider](https://www.cpbox.io)
- [CPPay facilitator](https://www.cppay.finance)
- [Local POIs endpoint](https://www.cpbox.io/api/x402/local-pois)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls]

**Output Format:** [Markdown with HTTP, bash, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The documented API response is JSON containing local POI result objects.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
