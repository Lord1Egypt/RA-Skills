## Description: <br>
Write and publish SEO-optimized blog posts to canmarket.ai, including topic research, article drafting with original data, Nuxt page creation, commit and push workflow, auto-deployment, and optional DEV.to cross-posting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing operators, site owners, and developers who administer CanMarket use this skill to draft, publish, and deploy SEO-focused blog posts for canmarket.ai. It is intended for users who can review generated content, changed files, commits, and deployment targets before publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can push generated blog content directly to a live CanMarket site from broad trigger phrases. <br>
Mitigation: Require manual approval after reviewing the article, changed files, git diff, commit message, target branch, deployment target, and any DEV.to destination before publishing. <br>
Risk: Direct commits to the production branch can cause accidental production changes. <br>
Mitigation: Use a branch or pull request workflow where practical, and deploy only after build verification and reviewer approval. <br>
Risk: The skill is site-specific and assumes access to CanMarket publishing infrastructure. <br>
Mitigation: Install and run it only if you own or administer the CanMarket site and are authorized to publish there. <br>


## Reference(s): <br>
- [Canlah AI homepage](https://canlah.ai) <br>
- [CanMarket website](https://canmarket.ai) <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/canmarket-blog) <br>
- [Publisher profile](https://clawhub.ai/user/PHY041) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Nuxt/Vue code, SEO metadata, JSON-LD snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify blog source files, propose commit messages, and provide deployment or cross-posting steps.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
