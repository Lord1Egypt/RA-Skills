## Description: <br>
Deploys simple web pages and HTML apps to Deno Deploy using the REST API and a standalone Python helper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hosainnet](https://clawhub.ai/user/hosainnet) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and engineers use this skill to prepare Deno-compatible single-file web apps, deploy them to Deno Deploy, verify the deployment, and share the resulting public URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish code publicly and create Deno resources using stored credentials. <br>
Mitigation: Confirm the exact code, project name, Deno organization, and public URL before each deployment. <br>
Risk: Stored Deno access tokens and organization identifiers can be misused if exposed. <br>
Mitigation: Use a dedicated limited token when possible, protect the credential files, and rotate credentials if exposure is suspected. <br>
Risk: Application source or environment values could unintentionally expose private information in a public deployment. <br>
Mitigation: Review the code before deployment and avoid deploying secrets, private source, or sensitive data. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/hosainnet/deno-subhosting-deploy-skill) <br>
- [Deno Subhosting Setup](https://dash.deno.com/subhosting/new_auto) <br>
- [Deno Deploy API Endpoint](https://api.deno.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown guidance with TypeScript examples and shell commands; the deploy helper prints JSON API responses and a deployment URL.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Deployment output can include a public Deno URL, deployment ID, status, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact metadata reports 0.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
