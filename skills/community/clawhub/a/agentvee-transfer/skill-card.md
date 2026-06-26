## Description: <br>
Transfer files, set per-download pricing, and list on the AgentVee marketplace (testnet). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jan-blockbites](https://clawhub.ai/user/jan-blockbites) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to upload local files or URLs to AgentVee, set optional per-download pricing, publish marketplace listings, browse listings, and manage upload or download URLs through API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected local files or URLs may be sent to AgentVee's testnet service. <br>
Mitigation: Confirm the exact file or URL before upload and avoid sensitive directories unless the user explicitly approves. <br>
Risk: Marketplace listing details or per-download pricing may be generated from context and become publicly visible. <br>
Mitigation: Review the price, title, description, category, tags, and public listing intent before executing the upload request. <br>
Risk: Delete operations can affect the wrong upload if the upload ID is mistaken. <br>
Mitigation: Confirm the exact upload ID before deletion and report the service response back to the user. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jan-blockbites/agentvee-transfer) <br>
- [AgentVee Homepage](https://agentvee.vercel.app) <br>
- [AgentVee Dashboard and API Keys](https://agentvee.vercel.app/dashboard) <br>
- [AgentVee Documentation](https://agentvee.vercel.app/docs) <br>
- [AgentVee OpenAPI Specification](https://agentvee.vercel.app/openapi.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands, JSON examples, and a structured text transfer report.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AGENTVEE_API_KEY and may trigger API calls that upload, list, browse, or delete user-selected files or URLs.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
