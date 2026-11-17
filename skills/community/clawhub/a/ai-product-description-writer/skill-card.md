## Description:

Generate product descriptions in professional, casual, luxury, and SEO styles from a product name and features using Grok AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog)

### License/Terms of Use:

MIT-0

## Use Case:

External users and e-commerce operators use this skill to draft ready-to-publish product listing copy for channels such as online stores and marketplaces from a product name and comma-separated feature list.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product names, features, and prompts are sent to x.ai using the user's API key.

Mitigation: Avoid unreleased, confidential, regulated, or customer-sensitive product data unless organizational policy permits that sharing.

Risk: The skill depends on a user-supplied XAI_API_KEY for API access.

Mitigation: Store the key securely, avoid committing it to files or logs, and rotate it if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/loutai0307-prog/skills/ai-product-description-writer)
- [BytesAgain homepage](https://bytesagain.com)
- [xAI Console](https://console.x.ai)
- [xAI Chat Completions API endpoint](https://api.x.ai/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style terminal text with section headings for each requested description style]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires XAI_API_KEY and sends product names, features, and prompts to the x.ai API.]

## Skill Version(s):

2.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
