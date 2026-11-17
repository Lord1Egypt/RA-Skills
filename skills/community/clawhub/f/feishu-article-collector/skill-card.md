## Description:

Collects Toutiao and WeChat article links, extracts article text, uses AI to summarize and classify the content, and stores the result in Feishu Bitable with duplicate detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[budingsoft](https://clawhub.ai/user/budingsoft)

### License/Terms of Use:


## Use Case:

External users and teams using OpenClaw can collect shared Toutiao or WeChat article links into a Feishu Bitable, with AI-generated summaries, categories, source labels, and duplicate checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weak URL validation can allow unintended sites to be fetched and processed.

Mitigation: Use the skill only in trusted chat contexts until strict hostname allowlisting and redirect checks are added.

Risk: Article content is sent to DeepSeek and stored in Feishu Bitable.

Mitigation: Deploy only where that third-party processing and storage of article content is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/budingsoft/skills/feishu-article-collector)
- [Feishu Open API Endpoint](https://open.feishu.cn/open-apis)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [JSON from the collection script and concise user-facing text replies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3, requests, Feishu app credentials, and a DeepSeek API key.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
