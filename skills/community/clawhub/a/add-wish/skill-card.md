## Description: <br>
Converts product URLs into one-click Wishfinity links so users can save items from any retailer to a universal wishlist. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leebellon](https://clawhub.ai/user/leebellon) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External shopping agents, gift assistants, deal finders, and product research assistants use this skill to offer a Wishfinity save link when a user wants to remember, compare, or share a product. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated links send the product URL and related shopping metadata to Wishfinity when opened. <br>
Mitigation: Tell users before they click that Wishfinity may store the product URL and extracted shopping details. <br>
Risk: Users need a Wishfinity account and must complete the save on Wishfinity. <br>
Mitigation: Present the link as an external Wishfinity save action rather than as a completed local wishlist update. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/leebellon/add-wish) <br>
- [+W Button](https://info.wishfinity.com/button) <br>
- [Wishfinity AI](https://info.wishfinity.com/artificial-intelligence/overview) <br>
- [The Wish Economy](https://info.wishfinity.com/insights/the-wish-economy) <br>
- [For Retailers and Brands](https://info.wishfinity.com/mall/universal-social-mall) <br>
- [wishfinity-mcp-plusw npm package](https://npmjs.com/package/wishfinity-mcp-plusw) <br>
- [wishfinity-mcp-plusw GitHub repository](https://github.com/wishfinity/wishfinity-mcp-plusw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown link or plain URL using the Wishfinity add endpoint] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a product URL; the generated link opens Wishfinity for the user to complete the save.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
