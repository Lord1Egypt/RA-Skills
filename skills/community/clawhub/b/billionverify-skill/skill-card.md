## Description: <br>
Verify email addresses using the BillionVerify API. Use when user wants to verify single emails, batch verify email lists, upload files for bulk verification, check credit balance, or manage webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billionverifier](https://clawhub.ai/user/billionverifier) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to have an agent verify individual email addresses, process bulk email lists, check BillionVerify credit usage, and manage webhook notifications through the BillionVerify API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send individual addresses, large email lists, and downloaded verification results to or from a third-party service. <br>
Mitigation: Use it only for email data you are authorized to process with BillionVerify, strip unnecessary columns before upload, and avoid regulated or confidential lists unless third-party processing is approved. <br>
Risk: Webhook setup can expose destination URLs and file-completion events to the wrong endpoint. <br>
Mitigation: Review webhook URLs before creation, limit events to the needed scope, and store the returned webhook secret securely. <br>
Risk: Authenticated API commands rely on a BillionVerify API key. <br>
Mitigation: Provide the key through the BILLIONVERIFY_API_KEY environment variable and avoid embedding it in prompts, scripts, logs, or shared files. <br>


## Reference(s): <br>
- [BillionVerify API Documentation](https://billionverify.com/docs) <br>
- [BillionVerify Website](https://billionverify.com/) <br>
- [BillionVerify Node SDK](https://www.npmjs.com/package/billionverify-sdk) <br>
- [BillionVerify MCP Server](https://www.npmjs.com/package/billionverify-mcp) <br>
- [Billionverify Skill on ClawHub](https://clawhub.ai/billionverifier/billionverify-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline bash and curl commands; API result downloads may be CSV files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BILLIONVERIFY_API_KEY for authenticated BillionVerify endpoints.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
