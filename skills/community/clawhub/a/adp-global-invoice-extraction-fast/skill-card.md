## Description: <br>
High-performance API for global invoice recognition. Each page is parsed in 5 seconds with reliable high-concurrency support. It extracts full invoice data and returns structured JSON directly, ideal for financial automation and cross-border document processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laiye-adp](https://clawhub.ai/user/laiye-adp) <br>

### License/Terms of Use: <br>
Commercial License Agreement <br>


## Use Case: <br>
Finance teams, system integrators, and developers use this skill to install and operate the Laiye ADP CLI for extracting structured invoice, receipt, and billing data from local files, URLs, Base64 inputs, folders, and asynchronous jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Invoices and receipts may contain confidential, regulated, or customer-sensitive data that is sent to the ADP/Laiye cloud service for processing. <br>
Mitigation: Use the skill only when the publisher and ADP/Laiye cloud service are approved for the documents being processed; avoid uploading confidential or regulated invoices without organizational approval. <br>
Risk: The skill requires an ADP API key, and exposed credentials could allow unauthorized service use. <br>
Mitigation: Store the API key in a protected local secret store or environment variable where possible, avoid sharing it in prompts or logs, and rotate it if exposure is suspected. <br>
Risk: The artifact documents pipe-to-shell and PowerShell installer options that execute remote scripts. <br>
Mitigation: Prefer the npm package or prebuilt release path when feasible; verify installer source and integrity before using remote script installers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/laiye-adp/adp-global-invoice-extraction-fast) <br>
- [ADP Global service](https://adp-global.laiye.com/) <br>
- [ADP China service](https://adp.laiye.com/) <br>
- [ADP CLI releases](https://github.com/laiye-ai/adp-cli/releases) <br>
- [ADP skill support issues](https://github.com/Laiye-ADP/adp-skills/issues) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with CLI commands and structured JSON extraction results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an ADP API key and an invoice extraction app ID; extraction may process local documents, remote URLs, Base64 data, folders, or asynchronous task IDs.] <br>

## Skill Version(s): <br>
1.0.1 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
