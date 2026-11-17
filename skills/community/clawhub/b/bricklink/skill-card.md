## Description:

BrickLink Store API helper/CLI (OAuth 1.0 request signing). Covers orders, store inventory (read + write), catalog, categories, colors, feedback, and push notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[odrobnik](https://clawhub.ai/user/odrobnik)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, store operators, and agents use this skill to query BrickLink store orders, inventory, catalog data, feedback, and notifications, and to prepare or run authenticated BrickLink API CLI commands. It also supports store mutations such as order updates, feedback replies, and inventory create/update/delete operations when the user provides suitable credentials and approves the action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands can immediately change live BrickLink store data, including orders, feedback, and inventory.

Mitigation: Use least-privilege or read-only credentials when possible and manually review every mutating command before execution.

Risk: Order detail and invoice HTML exports may contain customer personal information and default to predictable /tmp file paths.

Mitigation: Choose an appropriate workspace output path for sensitive exports, protect generated files, and remove temporary copies when no longer needed.

Risk: BrickLink OAuth credentials grant access according to the account and token permissions used.

Mitigation: Store credentials securely, avoid sharing them with untrusted agents, and rotate tokens if exposure is suspected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/odrobnik/skills/bricklink)
- [Setup Instructions](SETUP.md)
- [BrickLink Catalog Item API](references/catalog-api.md)
- [BrickLink Store Inventory API](references/inventory-api.md)
- [BrickLink Orders API](references/orders-api.md)
- [BrickLink Catalog Resource Representations](https://www.bricklink.com/v3/api.page?page=resource-representations-catalog)
- [BrickLink Inventory Resource Representations](https://www.bricklink.com/v3/api.page?page=resource-representations-inventory)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline shell commands; CLI commands can return JSON or text and can write local HTML files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and BrickLink OAuth 1.0 credentials via config file or environment variables.]

## Skill Version(s):

1.4.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
