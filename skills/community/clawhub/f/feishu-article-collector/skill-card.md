## Description: <br>
Collects Toutiao and WeChat public account articles, extracts article text, uses AI to summarize and categorize them, and stores deduplicated records in Feishu Bitable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[budingsoft](https://clawhub.ai/user/budingsoft) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and workspace operators use this skill to save shared Toutiao or WeChat article links into a Feishu Bitable with an AI-generated summary, category, source label, and duplicate check. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automates article retrieval, AI analysis, and writes to a Feishu workspace, which can expose article content and derived metadata to Feishu and DeepSeek. <br>
Mitigation: Use a controlled Feishu workspace, a dedicated low-privilege app, and avoid confidential, internal, subscription-only, or personal links unless this data flow is acceptable. <br>
Risk: Weak scoping around link handling and redirects can increase the impact of high-automation behavior. <br>
Mitigation: Tighten hostname validation, re-check or disable redirects, and add an explicit command or authorization gate before production use. <br>
Risk: The setup helper includes full-access permission behavior. <br>
Mitigation: Remove or gate the full-access helper and document the intended data handling and permission model before deploying broadly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/budingsoft/feishu-article-collector) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/budingsoft) <br>
- [Feishu Open APIs](https://open.feishu.cn/open-apis) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [Text replies based on JSON script results, with shell command invocation and environment-variable configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3, requests, FEISHU_APP_ID, FEISHU_APP_SECRET, and DEEPSEEK_API_KEY; writes article records to Feishu Bitable.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
