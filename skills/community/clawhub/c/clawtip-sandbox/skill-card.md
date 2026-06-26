## Description: <br>
为第三方技能执行 clawtip 沙箱支付交易，仅在第三方服务发起有效的 clawtip 支付请求时触发，并在沙箱环境中完成支付验证。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawtip](https://clawhub.ai/user/clawtip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to test third-party ClawHub payment integrations against the clawtip sandbox flow without using real funds. The skill accepts order identifiers from a calling workflow, runs the sandbox payment CLI, and returns diagnostic payment validation output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can forward raw sandbox payment stdout that may include token URLs, plaintext credential material, decrypted payloads, or order parameters. <br>
Mitigation: Use only in a controlled developer sandbox, redact sensitive stdout before forwarding, and require explicit consent before sharing payment debug output. <br>
Risk: The skill persists a local sandbox token in configs/config.json. <br>
Mitigation: Restrict configs/config.json to owner read/write permissions, restrict the configs directory, and avoid reusable credentials or real funds. <br>
Risk: The skill installs and executes an npm CLI package as part of the sandbox payment flow. <br>
Mitigation: Verify the npm package provenance separately and keep execution limited to controlled sandbox environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clawtip/clawtip-sandbox) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with CLI stdout excerpts and diagnostic guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include sandbox payment status, order parameter diagnostics, credential-related debug fields, and remediation guidance.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
