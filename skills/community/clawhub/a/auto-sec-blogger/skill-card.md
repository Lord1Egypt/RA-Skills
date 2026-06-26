## Description: <br>
Auto Sec Blogger collects security news, selects relevant items, generates security blog drafts with an LLM, publishes drafts to Notion, and can deploy approved posts to a GitHub Pages blog. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rebugui](https://clawhub.ai/user/rebugui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security content teams use this skill to automate security-news collection, article drafting, Notion review workflows, and publishing of approved Markdown posts to a blog repository. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish Notion-approved content to a GitHub Pages repository through local git actions. <br>
Mitigation: Use a dedicated test or blog repository, inspect approvals and git diffs before enabling pushes, and grant only the minimum GitHub permissions needed. <br>
Risk: Notion and GitHub credentials can allow unintended writes if they are broad or reused. <br>
Mitigation: Use dedicated low-privilege Notion and GitHub credentials and rotate them if the workspace or logs may have exposed them. <br>
Risk: Background publishing can continuously deploy content without close review. <br>
Mitigation: Avoid the background publisher unless continuous publishing is required and keep a human approval gate in Notion. <br>
Risk: Runtime Mermaid rendering through npx can introduce dependency and execution risk. <br>
Mitigation: Pin the Mermaid renderer version or remove runtime npx rendering before production use. <br>


## Reference(s): <br>
- [Architecture Reference](references/architecture.md) <br>
- [GLM API Documentation](https://open.bigmodel.cn/dev/api) <br>
- [Notion API Documentation](https://developers.notion.com/) <br>
- [Jekyll Documentation](https://jekyllrb.com/docs/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown articles, Notion draft content, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local blog post files and trigger git-based publication when configured.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
