## Description: <br>
Use the BrickOwl API through the included CLI for catalog lookup, inventory, orders, wishlists, and safe marketplace writes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[musketyr](https://clawhub.ai/user/musketyr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketplace operators, and AFOL sellers use this skill to work with their authenticated BrickOwl account: searching catalog records, validating IDs, viewing inventory and orders, creating wishlists, and preparing guarded inventory changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a BrickOwl API key that can access private store, order, buyer, address, cost, inventory, and note data. <br>
Mitigation: Install only when the operator is comfortable granting that account access, keep the API key out of transcripts and logs, and summarize private data only to the extent needed for the user's task. <br>
Risk: Evidence security guidance reports a conflicting included prompt that says seller inventory changes can run without approval. <br>
Mitigation: Treat that no-approval prompt as unsafe; require a dry run and explicit user confirmation before any create, update, delete, wishlist, or bulk write. <br>
Risk: BrickOwl writes can create, update, or delete marketplace inventory and wishlist data. <br>
Mitigation: Restate the exact action, identifiers, quantity, price, condition, wishlist name, or bulk request list before executing with --yes. <br>


## Reference(s): <br>
- [AFOL BrickOwl ClawHub Page](https://clawhub.ai/musketyr/afol-brickowl) <br>
- [BrickOwl OpenAPI Reference](references/openapi/brickowl.yaml) <br>
- [BrickOwl Tool Guidance](references/prompts/brickowl-tools.txt) <br>
- [BrickOwl API Documentation](https://www.brickowl.com/api_docs) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, json] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses BRICKOWL_API_KEY from the environment and supports dry-run output for mutating commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
