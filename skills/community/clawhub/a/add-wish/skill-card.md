## Description:

Save any product to a universal wishlist. Converts any product URL into a one-click "save for later" link. Works with any retailer, any AI platform, zero setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leebellon](https://clawhub.ai/user/leebellon)

### License/Terms of Use:


## Use Case:

External users and developers use this skill in shopping agents to turn product URLs into Wishfinity save links so products can be saved, shared, and revisited later.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shopping intent may be redirected from add-to-cart or broad shopping requests into a third-party Wishfinity save flow.

Mitigation: Offer the save link only when the user explicitly wants to save a product or add it to Wishfinity.

Risk: Opening a generated link sends the product URL to Wishfinity, where product metadata may be extracted and stored.

Mitigation: Disclose this before presenting the link so the user can decide whether to continue.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leebellon/skills/add-wish)
- [+W Button](https://info.wishfinity.com/button)
- [Wishfinity AI](https://info.wishfinity.com/artificial-intelligence/overview)
- [wishfinity-mcp-plusw npm package](https://npmjs.com/package/wishfinity-mcp-plusw)
- [wishfinity-mcp-plusw GitHub repository](https://github.com/wishfinity/wishfinity-mcp-plusw)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown link containing a Wishfinity add URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated links send product URLs to Wishfinity when opened; no local file output.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
