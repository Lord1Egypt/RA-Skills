## Description: <br>
AlphaClaw is a SkillHub CLI tool for searching, installing, publishing, and managing Claude Code skills with AK/SK login, skill search, install and publish workflows, favorites, and comments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688AiInfra](https://clawhub.ai/user/1688AiInfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use AlphaClaw to authenticate to SkillHub, discover Claude Code skills, install them into local projects, and publish skill packages for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs users to install and trust the third-party 1688alphaclaw npm package. <br>
Mitigation: Verify the npm package and AlphaShop or SkillHub domains before installation. <br>
Risk: The CLI handles AK/SK credentials and stores authentication data under ~/.alphaclaw/auth.json. <br>
Mitigation: Use revocable or least-privilege credentials and protect the local authentication file. <br>
Risk: Commands such as --force and --yes can overwrite local skills or publish content with reduced review. <br>
Mitigation: Review commands carefully before executing overwrite or non-interactive publish operations. <br>


## Reference(s): <br>
- [AlphaClaw on ClawHub](https://clawhub.ai/1688AiInfra/alphaclaw) <br>
- [SkillHub website](https://skill.alphashop.cn/) <br>
- [AlphaShop API key management](https://www.alphashop.cn/seller-center/apikey-management) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and CLI configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to run npm and alphaclaw CLI commands that install, overwrite, authenticate, or publish skills.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill frontmatter metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
