## Description: <br>
Queries package tracking information from Chinese and international carriers through the Kuaidi100 API, with optional carrier auto-detection from the tracking number. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charles-lpf](https://clawhub.ai/user/charles-lpf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to check delivery status and present a package tracking timeline when a tracking number is provided. It supports carrier auto-detection for common Chinese and international carriers, with manual carrier code override when detection fails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Package lookups send tracking numbers, carrier codes, and Kuaidi100 customer identifier/signature data to Kuaidi100. <br>
Mitigation: Use the skill only when the user is comfortable sharing those lookup details with Kuaidi100, and avoid querying sensitive shipments without consent. <br>
Risk: Kuaidi100 credentials can expose quota or billing if reused broadly or stored on shared machines. <br>
Mitigation: Use a dedicated API key when possible, monitor quota and billing, and avoid storing credentials in shell startup files on shared systems. <br>
Risk: Carrier auto-detection may choose the wrong carrier or fail for unsupported tracking number formats. <br>
Mitigation: Confirm the carrier with the user or provide a manual carrier code when auto-detection is uncertain. <br>


## Reference(s): <br>
- [Kuaidi100 Open Platform](https://api.kuaidi100.com/register/enterprise) <br>
- [Kuaidi100 Dashboard](https://api.kuaidi100.com/home) <br>
- [Kuaidi100 Carrier Codes](https://api.kuaidi100.com/manager/openapi/download/kdbm.do) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text tracking status and timeline, typically summarized for the user as Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided Kuaidi100 API key and customer ID; sends tracking number and carrier code to Kuaidi100.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
