## Description:

Use the included Brickset CLI for LEGO set search/details, images, instructions, reviews, login/user hash, collection, wishlist, and notes with guarded account writes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[musketyr](https://clawhub.ai/user/musketyr)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve Brickset-backed LEGO set details, images, instructions, and community reviews, and to manage Brickset collection, wishlist, ratings, quantities, and notes after explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Brickset credentials could be sent to an unintended endpoint if the base URL is changed.

Mitigation: Use only the official Brickset API URL and avoid setting BRICKSET_BASE_URL or passing --base-url when real credentials are configured.

Risk: Account-changing collection or wishlist commands can modify private Brickset data.

Mitigation: Require explicit user confirmation for the exact account change and use dry-run output before running mutating commands with --yes.

Risk: Brickset API keys, user hashes, usernames, passwords, collection contents, wishlist entries, and notes may be sensitive.

Mitigation: Treat Brickset credentials and private account data as secrets, redact them from logs and summaries, and summarize only the information needed for the user's request.

## Reference(s):

- [Brickset OpenAPI reference](references/openapi/brickset.yaml)
- [Brickset public prompt guidance](references/prompts/brickset-tools.txt)
- [Brickset private prompt guidance](references/prompts/brickset-private-tools.txt)
- [Brickset API production endpoint](https://brickset.com/api/v3.asmx)
- [Brickset API key request](https://brickset.com/tools/webservices/requestkey)
- [Brickset API v3 documentation](https://brickset.com/article/52664/api-version-3-documentation)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise API-result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Brickset URLs, PDF instruction links, collection status summaries, and redacted dry-run request shapes.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
