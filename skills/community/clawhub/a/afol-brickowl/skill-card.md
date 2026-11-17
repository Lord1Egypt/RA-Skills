## Description:

Use the BrickOwl API through the included CLI for catalog lookup, inventory, orders, wishlists, and safe marketplace writes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[musketyr](https://clawhub.ai/user/musketyr)

### License/Terms of Use:

MIT-0

## Use Case:

External BrickOwl sellers and agents use this skill to look up BrickOwl catalog data, inspect the authenticated store inventory and orders, create wishlists, and prepare marketplace inventory changes through the included CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send BRICKOWL_API_KEY to a caller-selected API URL through BRICKOWL_BASE_URL or --base-url.

Mitigation: Use the default BrickOwl API endpoint unless the alternate destination is fully trusted.

Risk: Marketplace writes can create, update, or delete inventory and wishlists, and the evidence notes conflicting approval guidance.

Mitigation: Confirm every create, update, delete, wishlist, and mutating bulk request with exact identifiers and values before passing --yes; use --dry-run first.

Risk: Order addresses, buyer email, inventory costs, and personal notes may be private.

Mitigation: Summarize only the data needed for the user's task and avoid exposing sensitive order or inventory details.

## Reference(s):

- [BrickOwl OpenAPI Reference](references/openapi/brickowl.yaml)
- [BrickOwl Tool Guidance](references/prompts/brickowl-tools.txt)
- [BrickOwl API Documentation](https://www.brickowl.com/api_docs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API or CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses BRICKOWL_API_KEY for authentication; mutating commands support dry-run and require explicit --yes execution.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
