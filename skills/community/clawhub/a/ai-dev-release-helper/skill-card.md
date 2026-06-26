## Description: <br>
AI开发者发布助手 automates release-content work for GitHub projects by researching comparable projects, generating project visuals, and preparing a WeChat article. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, open-source maintainers, and developer-relations teams use this skill to prepare release announcements, project introductions, cover images, competitor analysis, and WeChat-ready technical articles from a public GitHub project. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may send project information and generated publishing assets to external services. <br>
Mitigation: Use the skill only with public or non-sensitive projects and review workflow.json before installing or running it. <br>
Risk: The workflow includes Feishu notifications that may disclose run status or publishing context if left enabled unintentionally. <br>
Mitigation: Disable Feishu notifications unless the target channel is intended and authorized. <br>
Risk: Generated release articles and images may be inaccurate or unsuitable for publication. <br>
Mitigation: Manually review generated articles and images before uploading or publishing to WeChat. <br>
Risk: Brave and WeChat credentials are needed for parts of the workflow. <br>
Mitigation: Use least-privilege credentials and avoid running the workflow with accounts or tokens that have broader access than required. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/zlszhonglongshen/ai-dev-release-helper) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/zlszhonglongshen) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, images] <br>
**Output Format:** [Markdown, JSON metadata, shell command examples, and generated image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces competitor_analysis.md, cover image, feature image, and article.md outputs in the configured output directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
