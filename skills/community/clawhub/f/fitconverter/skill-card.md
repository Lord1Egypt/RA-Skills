## Description: <br>
fitconverter helps agents submit fitness activity exports to the FitConverter service for conversion between supported source platforms and FIT, TCX, GPX, KML, or connected destination platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daozhao](https://clawhub.ai/user/daozhao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to configure a FitConverter MCP connection, upload workout export ZIPs, submit conversion jobs, and check conversion or payment status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workout exports and email addresses may be sent to FitConverter during conversion. <br>
Mitigation: Use the service only when comfortable sharing those data, confirm the selected files before upload, and avoid including unrelated files in ZIP archives. <br>
Risk: Some sync modes may require API keys or platform account passwords. <br>
Mitigation: Prefer manual secure API-key configuration, avoid pasting secrets in chat when possible, and use credentials that can be rotated or revoked. <br>
Risk: Conversion flows may return payment QR codes or payment links. <br>
Mitigation: Confirm the destination, amount, order details, and payment recipient before paying. <br>


## Reference(s): <br>
- [ClawHub fitconverter listing](https://clawhub.ai/daozhao/fitconverter) <br>
- [FitConverter homepage](https://www.fitconverter.com) <br>
- [FitConverter MCP API](https://api.fitconverter.com/mcp) <br>
- [OpenClaw integration guide](openclaw-integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JSON, bash, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include MCP calls, HTTP multipart upload examples, status handling, and payment QR-code handling guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
