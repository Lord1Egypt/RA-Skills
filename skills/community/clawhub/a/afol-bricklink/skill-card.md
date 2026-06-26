## Description: <br>
Use the self-contained BrickLink API CLI for OAuth1-signed catalog, pricing, order, inventory, feedback, coupon, shipping, notification, and member-note workflows with guarded marketplace writes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[musketyr](https://clawhub.ai/user/musketyr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, marketplace operators, and LEGO AFOL sellers use this skill to query BrickLink catalog, pricing, order, inventory, feedback, coupon, shipping, notification, and member-note data, and to prepare guarded marketplace write actions after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires BrickLink OAuth credentials and can access private order, buyer, inventory, feedback, coupon, shipping, notification, and member-note data. <br>
Mitigation: Use narrowly scoped BrickLink API credentials, pass them only through BRICKLINK_API_* environment variables, and summarize only the data needed for the user's task. <br>
Risk: Marketplace write actions can create, update, or delete live inventory, order state, feedback, coupons, or private member notes. <br>
Mitigation: Run dry-run commands first, restate the exact endpoint, target, payload summary, and destructive impact, then wait for explicit confirmation before using --yes. <br>
Risk: Large set price breakdowns may consume substantial BrickLink API quota and take several minutes. <br>
Mitigation: Ask for approval before fan-out pricing workflows and begin with the approval-warning path when the pricing tool requires it. <br>


## Reference(s): <br>
- [AFOL BrickLink ClawHub Release](https://clawhub.ai/musketyr/afol-bricklink) <br>
- [BrickLink API Reference](https://www.bricklink.com/v3/api.page) <br>
- [BrickLink OpenAPI Reference](references/openapi/bricklink.yaml) <br>
- [BrickLink Tool Guidance](references/prompts/bricklink-tools.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, environment-variable configuration, and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Marketplace write workflows should use dry runs first, require explicit user confirmation, and avoid exposing OAuth credentials or private account data.] <br>

## Skill Version(s): <br>
1.0.0 (source: artifact frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
