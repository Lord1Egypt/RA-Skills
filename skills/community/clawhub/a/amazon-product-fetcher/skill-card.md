## Description:

Fetches Amazon product details, including title, current price, currency, rating, review count, availability, main image, and product URL, from an Amazon URL or ASIN without requiring an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mysmth2003](https://clawhub.ai/user/mysmth2003)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to look up public Amazon product information by URL or ASIN and receive product fields suitable for quick review or downstream agent responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The marketplace setting can direct network requests to arbitrary HTTPS hosts instead of only Amazon domains.

Mitigation: Restrict the marketplace setting to known Amazon domains and constrain redirects before using the skill in sensitive environments.

Risk: Amazon may return CAPTCHA, 503, or page variants that leave fields empty.

Mitigation: Treat missing fields as lookup failures, retry later, or use an authenticated Amazon data source for high-volume or reliability-sensitive workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mysmth2003/skills/amazon-product-fetcher)
- [Publisher profile](https://clawhub.ai/user/mysmth2003)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Plain text table or JSON object containing Amazon product fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs ASIN, title, price, currency, rating, review count, availability, image URL, and product URL when available.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
