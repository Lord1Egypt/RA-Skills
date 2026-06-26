## Description: <br>
Multi-step deployment agent for full-stack apps, covering build, test, GitHub publishing, and Cloudflare Pages deployment with human approval at each stage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sherajdev](https://clawhub.ai/user/sherajdev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to guide full-stack app deployment through local build and test checks, GitHub publishing, and Cloudflare Pages release steps. It is especially relevant for Next.js and Cloudflare D1 deployment preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing steps may affect the wrong repository, files, account, visibility setting, or Cloudflare project if run from the wrong workspace or account context. <br>
Mitigation: Before push or deploy stages, confirm the working directory, git status, files to commit, GitHub account, repository visibility, Cloudflare account, and target project. <br>
Risk: The documented default deployment domain uses sheraj.org, which may be unintended for other users or organizations. <br>
Mitigation: Use an explicitly controlled custom domain and avoid the default sheraj.org domain unless ownership and intent are confirmed. <br>


## Reference(s): <br>
- [C.R.A.B Deploy Agent on ClawHub](https://clawhub.ai/sherajdev/deploy-agent) <br>
- [Cloudflare Pages Next.js Framework Guide](https://developers.cloudflare.com/pages/framework-guides/nextjs/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires gh, wrangler, git, and jq for the documented workflow.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
