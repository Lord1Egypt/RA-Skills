## Description: <br>
Creates and deploys web applications to Cloudflare Pages, with safety checks for file overwrites, GitHub pushes, and deployment changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samueli](https://clawhub.ai/user/samueli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create a web project, optionally push it to GitHub, and deploy it to Cloudflare Pages. It is suited for agent-assisted deployment workflows where project naming, file overwrite, repository, and Cloudflare account actions need explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify local project files, copy source directories, and overwrite existing paths. <br>
Mitigation: Confirm the project name, source directory, and whether in-place deployment or overwrite behavior is authorized before running deployment commands. <br>
Risk: The skill can use GitHub and Cloudflare accounts to create repositories, push code, or deploy pages. <br>
Mitigation: Confirm whether to skip GitHub or Cloudflare deployment, and use a least-privilege Cloudflare API token scoped to the intended account. <br>
Risk: Missing dependencies may lead to requests for global tool installation. <br>
Mitigation: Ask for explicit permission before installing system-level or global dependencies such as GitHub CLI or Wrangler. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samueli/dev-deploy) <br>
- [Cloudflare API token management](https://dash.cloudflare.com/profile/api-tokens) <br>
- [Cloudflare API token documentation](https://developers.cloudflare.com/fundamentals/api/get-started/create-token/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local project files and deployment instructions based on the requested workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
