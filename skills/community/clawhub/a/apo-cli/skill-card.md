## Description: <br>
Search and order pharmacy products from apohealth.de via apo-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lars147](https://clawhub.ai/user/Lars147) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agent operators use this skill to search apohealth.de pharmacy products by name or PZN, inspect product details, browse categories, and manage a shopping cart. The user remains responsible for checkout and any medication decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change a live apohealth.de shopping cart. <br>
Mitigation: Review add, remove, and clear actions before execution; the user completes checkout separately in a browser. <br>
Risk: Local apo_cookies.json and apo_cart.json files may contain private session or cart data. <br>
Mitigation: Treat those files as private session data and avoid sharing them. <br>
Risk: Product search and cart workflows may involve medication-related products. <br>
Mitigation: Do not use the skill for medical advice; use it only for shopping workflow assistance. <br>


## Reference(s): <br>
- [Apo Cli ClawHub release](https://clawhub.ai/Lars147/apo-cli) <br>
- [Command Reference](references/commands.md) <br>
- [apohealth.de](https://www.apohealth.de) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and clickable cart URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include apohealth.de cart URLs and summaries of cart, product, price, and availability information.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata; pyproject.toml lists 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
