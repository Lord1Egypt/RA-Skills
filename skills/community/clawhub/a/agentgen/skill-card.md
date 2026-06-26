## Description: <br>
Generate PDFs and images from HTML using the AgentGen CLI and API, with a free tier and optional authenticated usage through AGENTGEN_API_KEY. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lyair1](https://clawhub.ai/user/lyair1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to generate screenshots, PDFs, reports, slides, invoices, and other rendered assets from HTML via AgentGen shell commands. It supports unauthenticated free-tier output and authenticated workflows for higher-volume or multi-page PDF generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HTML content and rendering inputs are sent to the AgentGen hosted service. <br>
Mitigation: Use the skill only for content approved for third-party processing, and do not include secrets, regulated data, confidential documents, or sensitive brand assets. <br>
Risk: Uploaded assets are publicly accessible temporary URLs for 24 hours. <br>
Mitigation: Upload only assets that can be public during the retention window, and remove or rotate any sensitive source material before rendering. <br>
Risk: The workflow depends on a third-party CLI and hosted rendering provider. <br>
Mitigation: Install the CLI from the documented source, keep credentials in AGENTGEN_API_KEY, and review generated files before using them in customer-facing workflows. <br>


## Reference(s): <br>
- [AgentGen homepage](https://www.agent-gen.com) <br>
- [ClawHub skill page](https://clawhub.ai/lyair1/agentgen) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands that produce PDF and image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated outputs may be PNG, JPEG, WebP, or PDF files; authenticated usage can remove watermarks and enable multi-page PDFs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
