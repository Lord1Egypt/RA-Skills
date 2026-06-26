## Description: <br>
Generate and deploy app Privacy Policy and Terms of Service static websites from an app feature document. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chentuan7963-afk](https://clawhub.ai/user/chentuan7963-afk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and app publishers use this skill to generate draft Privacy Policy and Terms of Service pages from explicit app feature inputs, run consistency checks, and deploy the approved static site to Cloudflare Pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated legal pages may not fully satisfy an app's legal or app-store requirements. <br>
Mitigation: Review the generated pages before deployment and seek human legal review before production app-store submission. <br>
Risk: Deployment uses Cloudflare credentials or an authenticated Wrangler session. <br>
Mitigation: Use least-privilege Cloudflare credentials and require explicit user approval before deployment. <br>
Risk: Heuristic feature and permission detection can miss or overstate app behavior. <br>
Mitigation: Collect explicit product inputs, run the consistency checker, and manually adjust disclosures when app behavior is more specific than the generated draft. <br>


## Reference(s): <br>
- [Cloudflare Pages + GitHub Deployment](references/cloudflare-github-deploy.md) <br>
- [App Legal Pages on ClawHub](https://clawhub.ai/chentuan7963-afk/app-legal-pages) <br>
- [Publisher Profile](https://clawhub.ai/user/chentuan7963-afk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with generated HTML/CSS files, JSON status output, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces static legal-site files, consistency-check results, deployment status, and public Cloudflare Pages URLs after user approval.] <br>

## Skill Version(s): <br>
0.1.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
