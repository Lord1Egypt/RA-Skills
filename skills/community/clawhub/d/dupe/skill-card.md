## Description:

Uses dupe.com APIs in order to find similar products for the product found in the input URL given by the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crisanmm](https://clawhub.ai/user/crisanmm)

### License/Terms of Use:


## Use Case:

External users and shopping assistants use this skill to find similar products from a product page URL or direct image URL through dupe.com.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends product or image URLs to dupe.com, which may expose private, internal, signed, or token-bearing URLs.

Mitigation: Use only public product or image URLs and avoid submitting private or token-bearing URLs.

Risk: The shell-command instructions may mishandle user-supplied URLs in a way that allows command injection.

Mitigation: Do not run the curl snippets with literal text substitution; construct a safely serialized HTTP request.

## Reference(s):

- [Dupe API endpoint](https://api.dupe.com/api/dupes/agent-skill)
- [ClawHub skill page](https://clawhub.ai/crisanmm/skills/dupe)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, guidance]

**Output Format:** [Markdown with curl command examples and formatted product-match results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns product titles, prices, stores, and links from the dupe.com matches array.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
