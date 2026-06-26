## Description: <br>
多平台内容分发器 v1.0。一次输入，自动适配小红书/知乎/公众号/抖音四种平台格式，直接输出可发布内容。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hyjaixiao](https://clawhub.ai/user/hyjaixiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketing teams, and social media operators use this skill to turn one Chinese content topic into platform-specific drafts for Xiaohongshu, Zhihu, WeChat public accounts, and Douyin. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Topics, points, and draft context are sent to the configured OpenAI-compatible API provider. <br>
Mitigation: Use a trusted OPENAI_BASE and avoid confidential or regulated inputs unless that provider and use case are approved. <br>
Risk: The skill requires an API key that can authorize model usage and cost. <br>
Mitigation: Use a limited-quota API key and rotate or revoke it if it is exposed. <br>
Risk: Generated drafts may contain inaccurate or unsuitable claims for public posting. <br>
Mitigation: Review and edit generated claims before publishing on social platforms. <br>
Risk: Generated drafts are saved locally and may contain sensitive campaign or topic details. <br>
Mitigation: Set CONTENT_OUTPUT_DIR to an appropriate location and delete or redirect output when drafts are sensitive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hyjaixiao/content-producer) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [OpenAI-compatible API endpoint](https://api.openai.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files] <br>
**Output Format:** [Markdown files with YAML front matter, plus terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes dated draft files under CONTENT_OUTPUT_DIR and can generate one selected platform or all supported platforms.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
