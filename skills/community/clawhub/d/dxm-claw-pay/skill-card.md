## Description: <br>
度小满支付技能处理 SP 服务余额不足或未购买场景，根据结构化商品数据生成支付链接和二维码，并支持通过 installSkill 流程下载已购买的 Skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[duxiaoman](https://clawhub.ai/user/duxiaoman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Skill authors use this skill to route unpaid SP-service responses into a payment QR-code flow and to install paid ClawHub skills after payment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installSkill flow can place remote ZIP contents into the local skills workspace and stores a local signing key. <br>
Mitigation: Use the installer only when the publisher, distribution service, and requested skill ID are trusted; prefer a contained environment and review or scan installed skill content before use. <br>
Risk: The payment flow depends on external payment and short-link services and writes QR-code image files locally. <br>
Mitigation: Confirm payment links are expected HTTPS payment URLs before QR generation, and delete temporary QR-code files manually when stricter cleanup is required. <br>


## Reference(s): <br>
- [ClawHub skill listing: dxm-claw-pay](https://clawhub.ai/duxiaoman/dxm-claw-pay) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, files, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON script responses; QR codes are written as PNG files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js. Payment QR output includes a local file path; user-facing guidance should not display the QR base64 payload.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
