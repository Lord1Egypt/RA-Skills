## Description:

Official Amazon PA API for product info, prices, and reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcbuer](https://clawhub.ai/user/jcbuer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure and run Amazon Product Advertising API lookups by ASIN for product title, price, rating, image, and URL data.

### Deployment Geography for Use:

Germany

## Known Risks and Mitigations:

Risk: Amazon access keys, secret keys, and partner tags may be exposed if stored in a shared ~/.env file.

Mitigation: Use a protected secret store or a tightly permissioned dedicated configuration file instead of a shared ~/.env file.

Risk: The included client may not work as a real authenticated PA API client because authenticated request signing is not implemented in the request path.

Mitigation: Validate the client in a controlled environment and implement proper PA API request signing before relying on it for production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jcbuer/skills/amazon-paapi)
- [Amazon Associates Product Advertising API setup](https://affiliate-program.amazon.de/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text CLI output with Markdown setup instructions and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Amazon Associates credentials and targets the Amazon.de Product Advertising API endpoint.]

## Skill Version(s):

1.0.0 (source: server release metadata, skill frontmatter, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
