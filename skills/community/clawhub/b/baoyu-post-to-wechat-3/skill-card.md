## Description: <br>
Posts content to WeChat Official Account via API or Chrome CDP, supporting article posting from HTML, markdown, or plain text and image-text posting with multiple images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tonight-su](https://clawhub.ai/user/tonight-su) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to prepare and post WeChat Official Account drafts from markdown, HTML, plain text, or image collections. The current release evidence says runtime posting scripts are not included, so users should treat the artifact as documentation unless implementation files are restored. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence says the documentation references posting, conversion, and environment-check scripts that are not included in the artifact. <br>
Mitigation: Before relying on the skill for posting, verify the required scripts are present in the installed artifact or treat the release as documentation-only. <br>
Risk: The skill asks agents to handle WeChat account credentials and persistent configuration. <br>
Mitigation: Use a dedicated WeChat account or isolated Chrome profile, avoid storing AppSecret in project files, and exclude .baoyu-skills and secret-bearing .env files from source control. <br>
Risk: Automated posting could target the wrong account or publish unintended content, images, or draft actions. <br>
Mitigation: Require a manual check of the selected account, content, images, and draft action before allowing API or browser posting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tonight-su/baoyu-post-to-wechat-3) <br>
- [Publisher profile](https://clawhub.ai/user/tonight-su) <br>
- [Project homepage](https://github.com/JimLiu/baoyu-skills#baoyu-post-to-wechat) <br>
- [Article Posting](references/article-posting.md) <br>
- [Image-Text Posting](references/image-text-posting.md) <br>
- [First-Time Setup](references/config/first-time-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell command examples and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May instruct agents to create local preference files and WeChat draft content; this release does not include the referenced runtime scripts.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata; artifact frontmatter says 1.56.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
