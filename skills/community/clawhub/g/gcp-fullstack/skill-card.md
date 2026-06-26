## Description: <br>
Complete development lifecycle super agent for GCP: scaffolding, compute, database, auth, feature generation, testing, pre-production QA gate with go/no-go reports, deploy, Cloudflare CDN/security, and monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guifav](https://clawhub.ai/user/guifav) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build and operate full-stack web applications on Google Cloud Platform, including scaffolding, service selection, feature implementation, testing, deployment, Cloudflare configuration, and monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan flags broad GCP, Cloudflare, repository, filesystem, network, and credential authority with incomplete scoping and warnings. <br>
Mitigation: Use a staging project first, issue least-privilege GCP/Firebase/Cloudflare credentials, and require explicit human approval before deploys, DNS or security changes, IAM changes, public exposure, database changes, and CI/CD triggers. <br>
Risk: The skill can generate QA flows that send prompts or outputs to OpenRouter for LLM-as-judge evaluation. <br>
Mitigation: Avoid production data and secrets in QA prompts, keep OPENROUTER_API_KEY optional, and review generated validation scripts before running them. <br>
Risk: Generated deployment and infrastructure commands can alter live cloud services, DNS records, databases, or source control state. <br>
Mitigation: Run read-only checks and dry runs where possible, verify the active GCP project and Cloudflare zone, back up data before database changes, and review all generated commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guifav/gcp-fullstack) <br>
- [Project scaffolding module](artifact/docs/01-scaffolding.md) <br>
- [Compute service selection module](artifact/docs/02-compute.md) <br>
- [Database setup module](artifact/docs/03-database.md) <br>
- [Authentication module](artifact/docs/04-auth.md) <br>
- [Feature generation module](artifact/docs/05-features.md) <br>
- [Testing and quality module](artifact/docs/06-testing.md) <br>
- [Deployment and monitoring module](artifact/docs/07-deploy.md) <br>
- [Cloudflare DNS, CDN, and security module](artifact/docs/08-cloudflare.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code blocks, shell commands, configuration snippets, generated project files, tests, and go/no-go reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or execute cloud, repository, filesystem, DNS, deployment, and QA workflows depending on user approval and available credentials.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
