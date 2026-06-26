## Description: <br>
Reads product links, specifications, and quantities from a Feishu Bitable table and uses browser automation to add matching Taobao or Tmall items to a shopping cart. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lorpha](https://clawhub.ai/user/Lorpha) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users or purchasing operators use this skill to bulk process procurement rows from a Feishu Bitable and add matching Taobao or Tmall items to a cart through an OpenClaw browser profile. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can alter a live shopping cart. <br>
Mitigation: Use a dry-run preview and require explicit user approval before any add-to-cart action. <br>
Risk: Bitable rows can drive browser automation with product URLs and purchase quantities. <br>
Mitigation: Validate rows before use, restrict product URLs to expected Taobao and Tmall domains, and review item, specification, and quantity values before execution. <br>
Risk: Results may be sent to a fixed Telegram recipient. <br>
Mitigation: Make notifications opt-in and user-configurable, and confirm the recipient before sending. <br>
Risk: Browser automation uses a named browser profile that may contain active shopping sessions. <br>
Mitigation: Run with a dedicated least-privilege browser profile and avoid using profiles with unrelated authenticated accounts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Lorpha/addtocartfrombitable) <br>
- [Default Feishu Bitable](https://somo-tech.feishu.cn/base/UIdIbPe2RaOQ1tsNIhlcB5ilngc) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, browser automation actions, API calls] <br>
**Output Format:** [Text or Markdown guidance with browser and messaging tool calls.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Feishu Bitable rows, Taobao or Tmall product URLs, exact specification text, quantities, an OpenClaw browser profile, and Telegram notification status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
