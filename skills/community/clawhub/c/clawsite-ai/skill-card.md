## Description: <br>
Static website hosting for AI agents that deploy HTML, CSS, JavaScript, images, and other static files to a dedicated HTTPS Clawsite URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dannylai999](https://clawhub.ai/user/dannylai999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to publish generated static websites, portfolios, link hubs, landing pages, and similar static content to a public URL. It guides deployment, cache purge, site listing, quota handling, and destructive delete workflows for Clawsite-hosted sites. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish generated files to a public Clawsite URL. <br>
Mitigation: Keep secrets, private drafts, and unpublished material out of the deployment directory before creating the zip. <br>
Risk: A deploy is an atomic full-site replacement and can remove files from the previous public site. <br>
Mitigation: Confirm the intended site contents before deployment and verify quota or rate-limit errors without attempting destructive resets. <br>
Risk: The configured API key can deploy, purge cache, list sites, and delete a site. <br>
Mitigation: Protect CLAWSITE_API_KEY and require explicit user confirmation before deleting or fully replacing a site. <br>


## Reference(s): <br>
- [Clawsite homepage](https://clawsite.ai) <br>
- [ClawHub skill page](https://clawhub.ai/dannylai999/clawsite-ai) <br>
- [Publisher profile](https://clawhub.ai/user/dannylai999) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with shell commands, HTTP request examples, and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLAWSITE_API_KEY and CLAWSITE_SITE_ID for authenticated site management.] <br>

## Skill Version(s): <br>
1.0.5 (source: SKILL.md frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
