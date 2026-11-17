## Description:

Reads product links, specifications, and quantities from Feishu Bitable records and uses browser automation to add matching Taobao/Tmall items to a shopping cart.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lorpha](https://clawhub.ai/user/lorpha)

### License/Terms of Use:


## Use Case:

External procurement and operations users can use this skill to bulk add purchasing-table items from Feishu Bitable into an authenticated Taobao or Tmall shopping cart.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make live cart changes in an authenticated shopping session.

Mitigation: Use a dedicated shopping browser profile and require explicit confirmation before adding items to the cart.

Risk: Untrusted Bitable records could direct the browser to unsafe or unintended product URLs.

Mitigation: Use trusted Bitable records only and validate that product links are legitimate Taobao or Tmall URLs before opening them.

Risk: Procurement results may be sent to a fixed Telegram recipient.

Mitigation: Remove the fixed Telegram notification or make the destination user-controlled before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lorpha/skills/addtocartfrombitable)
- [Default Feishu Bitable](https://somo-tech.feishu.cn/base/UIdIbPe2RaOQ1tsNIhlcB5ilngc)
- [Example Tmall item URL](https://detail.tmall.com/item.htm?id=701699369447)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Code, Guidance]

**Output Format:** [Markdown guidance with JavaScript and tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform live browser actions against an authenticated shopping profile and send a completion notification.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
