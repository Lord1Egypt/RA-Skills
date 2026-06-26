## Description: <br>
Automates KFC and McDonald's order flows by converting backend order links into browser actions that confirm orders and retrieve pickup codes and order information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wananbaby](https://clawhub.ai/user/wananbaby) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to query configured KFC and McDonald's product/order backends, create order links, run the matching browser flow, and return order status, pickup codes, screenshots, or order links to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place paid or account-linked food orders through configured KFC and McDonald's flows. <br>
Mitigation: Keep the default no-final-submit behavior unless live order submission is intentional, and test with controlled accounts and backends before use. <br>
Risk: The skill sends phone, API key, and order parameters to the configured backend. <br>
Mitigation: Install only when the configured backend is trusted, protect the .env/API key, and avoid exposing credentials in logs or shared files. <br>
Risk: Local order-state outputs can contain order links and order details. <br>
Mitigation: Delete local outputs and order-state files when no longer needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wananbaby/clawauto-shop) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [OPENCLAW_INSTALL_CHECKLIST.md](artifact/OPENCLAW_INSTALL_CHECKLIST.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Files] <br>
**Output Format:** [Markdown and terminal text with JSON status lines, local JSON state files, and screenshots from browser flows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include product lists, order IDs, order links, pickup codes, order status, balance/cost details, screenshots, and local order-state files.] <br>

## Skill Version(s): <br>
2.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
