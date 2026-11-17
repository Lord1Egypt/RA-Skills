## Description:

Track product prices across ecommerce sites and alert on offers or target-price hits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pbalajiips](https://clawhub.ai/user/pbalajiips)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to monitor product URLs or item queries, compare current and previous ecommerce prices, and produce alert-ready summaries when prices drop or target prices are reached.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make outbound requests from the user's machine to supplied URLs or discovered links, including internal or private-network targets via direct input or redirects.

Mitigation: Use only trusted public ecommerce URLs, avoid internal, localhost, private-network, or sensitive URLs, and review redirect handling before relying on trusted-store filtering as a security boundary.

Risk: Price extraction is best-effort and can be blocked by stores or misread page content.

Mitigation: Review alert payloads before acting on them and add store-specific adapters or validation for production monitoring.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON alert payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local watcher records and alert summaries containing product id, title, URL, price fields, drop percent when available, and timestamp.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
