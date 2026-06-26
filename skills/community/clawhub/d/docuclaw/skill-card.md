## Description: <br>
Sovereign document intelligence & archival system. Extracts structured data from invoices, receipts, and contracts 100% locally using AI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[astonysh](https://clawhub.ai/user/astonysh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use DocuClaw to extract structured information from invoices, receipts, contracts, scans, photos, and email documents into a local Markdown archive for search, accounting, calendaring, and archival workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill's local-only privacy claim conflicts with optional OpenAI Vision use for confidential documents. <br>
Mitigation: Review configuration before use and disable cloud vision providers unless the user intentionally permits document data to leave local hardware. <br>
Risk: Calendar or accounting sync may share extracted sensitive document data with third-party services. <br>
Mitigation: Enable sync integrations only after confirming the target service, data scope, and retention requirements for the document set. <br>


## Reference(s): <br>
- [DocuClaw ClawHub Listing](https://clawhub.ai/astonysh/docuclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration, Shell commands] <br>
**Output Format:** [Markdown guidance with command examples and structured archival conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Describes local document processing workflows that may optionally connect to cloud vision, calendar, or accounting services.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
