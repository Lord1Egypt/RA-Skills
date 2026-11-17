## Description: <br>
AI智能图表生成：根据用户提供的数据生成图表配置，并通过 aitubiao API 创建可视化项目。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aitubiao](https://clawhub.ai/user/aitubiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn provided tables or files into aitubiao chart projects after authentication, quota checking, and user cost confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a persistent aitubiao API key in ~/.aitubiao/credentials and the CLI loads that file as shell code. <br>
Mitigation: Use only a revocable API key from the legitimate aitubiao API-key page, inspect or delete ~/.aitubiao/credentials after use, and rotate the key if it may have been exposed or tampered with. <br>
Risk: The API key can query quota and create billable projects through the aitubiao service. <br>
Mitigation: Confirm quota and cost before creating projects, and install the skill only when the user trusts aitubiao with submitted data and billing actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aitubiao/aitubiao-ai-chart) <br>
- [aitubiao API key management](https://app.aitubiao.com/setting/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce chart project URLs, project identifiers, screenshot links, quota details, and downloaded export files through the aitubiao service.] <br>

## Skill Version(s): <br>
1.1.5 (source: ClawHub release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
