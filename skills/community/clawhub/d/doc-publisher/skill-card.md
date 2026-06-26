## Description: <br>
Doc Publisher converts local Markdown document series into WeChat Official Account draft articles and publishes them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[403914291](https://clawhub.ai/user/403914291) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, editors, and content teams use this skill to convert local Markdown documentation into WeChat Official Account HTML drafts, publish ordered article series, and record publication results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires WeChat Official Account API credentials and the examples show credential-shaped values. <br>
Mitigation: Keep .env private and out of version control, rotate any copied example values, and prefer a test WeChat account before using production credentials. <br>
Risk: Draft-clearing scripts can delete WeChat drafts and rewrite publication records. <br>
Mitigation: Run draft-clearing scripts only after manual code review and only when intentionally deleting drafts from the configured account. <br>
Risk: Publishing sends local document content and selected image material to WeChat APIs. <br>
Mitigation: Review source documents and media for sensitive or unreleased information before publishing. <br>


## Reference(s): <br>
- [Doc Publisher ClawHub Page](https://clawhub.ai/403914291/doc-publisher) <br>
- [Project Homepage](https://docs.esupagent.com) <br>
- [WeChat Official Account Platform](https://mp.weixin.qq.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API Calls, Files] <br>
**Output Format:** [Markdown guidance with Node.js commands, configuration values, WeChat HTML draft content, and JSON publication records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WeChat Official Account credentials in a local .env file and can create or delete WeChat drafts through API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release.version and skill.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
