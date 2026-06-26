## Description: <br>
Deploy multilingual static websites on Cloudflare with Astro using markdown sources, supporting i18n, free hosting, and Git-based or direct deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bezkom](https://clawhub.ai/user/bezkom) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and site maintainers use this skill to scaffold, configure, internationalize, and deploy Astro static websites to Cloudflare Pages. It also supports multilingual blog workflows through helper scripts for creating localized posts and checking translation coverage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deployment commands may target the wrong Cloudflare account or Pages project if run without review. <br>
Mitigation: Review the active Cloudflare account, project, and deployment target before running Wrangler deployment commands. <br>
Risk: Helper scripts create or inspect local content paths based on user-provided titles, language codes, and directory values. <br>
Mitigation: Run the skill only in trusted Astro workspaces and review title, language, and directory inputs before execution. <br>


## Reference(s): <br>
- [Astro Docs](https://docs.astro.build) <br>
- [Cloudflare Pages Docs](https://developers.cloudflare.com/pages) <br>
- [Astro i18n Guide](https://docs.astro.build/en/guides/i18n/) <br>
- [Astro Cloudflare Adapter](https://docs.astro.build/en/guides/deploy/cloudflare/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with code snippets, shell commands, configuration examples, and optional JSON reports from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Helper scripts use local filesystem inputs and Python standard library only.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
