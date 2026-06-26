## Description: <br>
AI-driven social media management skill that helps generate content calendars, recommend posting times, draft engagement replies, and analyze performance across supported platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lvjunjie-byte](https://clawhub.ai/user/lvjunjie-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Social media operators, creators, brands, and marketing teams use this skill to plan posts, choose publishing times, draft replies, and review engagement analytics for platforms including Xiaohongshu, Weibo, Twitter/X, LinkedIn, Instagram, and WeChat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says the skill asks users to store powerful account credentials in a plaintext agent-readable file. <br>
Mitigation: Use scoped API tokens stored in a secret manager or environment variables, and avoid placing passwords, session cookies, or long-lived account secrets in TOOLS.md. <br>
Risk: The security guidance notes that public posting, auto-reply, and bulk engagement safeguards are under-specified. <br>
Mitigation: Require human review and approval before real posting, automated replies, or bulk engagement actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lvjunjie-byte/ai-social-media-manager-lvjunjie) <br>
- [README](artifact/README.md) <br>
- [API Documentation](artifact/src/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with command-line examples, JavaScript API examples, generated text replies, and JSON-like calendar or analytics objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include generated posting schedules, suggested reply text, engagement summaries, and configuration guidance for platform credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact package metadata references 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
