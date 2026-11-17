## Description:

Searches 1688 products through official 1688 Open Platform APIs, including category lookup, keyword search, image search, product details, seller listings, recommendations, and product-pool pulls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search and compare 1688 marketplace products, retrieve product and seller details, and generate recommendation or sourcing results from authorized 1688 API access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires 1688 account API credentials and may cache access tokens for reuse across 1688 skills.

Mitigation: Install only in trusted workspaces, use scoped credentials where possible, protect environment variables and token cache files, and review token handling before deployment.

Risk: Image search can process user-supplied image URLs and may download or submit image data to the 1688 API.

Mitigation: Prefer trusted 1688 or alicdn.com image URLs, avoid untrusted image URLs, and validate image URL destinations before use.

Risk: Product, price, seller, and availability data comes from external 1688 API responses.

Mitigation: Verify commercial decisions against 1688 product pages and seller records before purchasing or publishing results.

## Reference(s):

- [1688 Product Search API Reference](references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/1688aiinfra/skills/1688-product-search)
- [1688 Open Platform](https://open.1688.com)
- [1688 API Invocation Documentation](https://open.1688.com/doc/apiInvoke.htm)
- [1688 Signature Documentation](https://open.1688.com/doc/signature.htm)
- [1688 Authorization Documentation](https://open.1688.com/doc/apiAuth.htm)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON API responses with human-readable text or Markdown summaries and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires 1688 API credentials; product-search results should expose product IDs and links for follow-up detail queries.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
