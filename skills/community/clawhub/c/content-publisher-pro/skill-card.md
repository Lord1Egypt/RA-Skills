## Description: <br>
Publishes Markdown articles to GitHub Pages blogs and Dev.to, with content variants, SEO optimization, and pre-publish duplicate checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wdsega](https://clawhub.ai/user/wdsega) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Technical bloggers and content operators use this skill to prepare, preview, and publish Markdown articles to GitHub Pages and Dev.to from a local workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing credentials for GitHub and Dev.to are sensitive and can grant write access to external services. <br>
Mitigation: Keep config files private, use least-privilege tokens, and install in a virtual environment with pinned or audited dependencies. <br>
Risk: A live run can publish unintended or duplicate content to public channels. <br>
Mitigation: Run with --dry-run first and review the selected Markdown article, destination platforms, and generated output before publishing. <br>
Risk: Article content is sent to third-party publishing services during normal use. <br>
Mitigation: Only publish content that is approved for those services and appropriate for public release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wdsega/content-publisher-pro) <br>
- [GitHub REST API](https://api.github.com) <br>
- [Dev.to API](https://dev.to/api) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May publish user-selected Markdown content to GitHub Pages and Dev.to when run outside dry-run mode.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
