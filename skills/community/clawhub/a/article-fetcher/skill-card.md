## Description: <br>
Fetches articles from WeChat Official Accounts, Xiaohongshu, Douban, and Zhihu, uploads images to OSS, extracts keywords with an LLM or local fallback, and archives the result to Notion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ajayhao](https://clawhub.ai/user/ajayhao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and content operators use this skill to fetch supported article URLs, preserve images in Aliyun OSS, extract tags, and create structured Notion archive entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Aliyun OSS and Notion credentials. <br>
Mitigation: Use least-privilege OSS and Notion tokens, store them outside prompts and source-controlled files, and rotate them if exposed. <br>
Risk: Optional LLM keyword extraction can send article text to the configured LLM provider. <br>
Mitigation: Configure an approved provider and avoid processing private, sensitive, or restricted content unless sharing it with that provider is allowed. <br>
Risk: Cookie files may contain active logged-in sessions for supported platforms. <br>
Mitigation: Protect cookie files with local file permissions, refresh them intentionally, and avoid sharing them with agents or users that do not need access. <br>
Risk: Archived articles and uploaded images may include copyrighted, private, or sensitive material. <br>
Mitigation: Archive only content the user is permitted to store, and review Notion database access and OSS bucket visibility before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ajayhao/article-fetcher) <br>
- [Publisher Profile](https://clawhub.ai/user/ajayhao) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and Python usage patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python dependencies plus Aliyun OSS, Notion, and optional LLM credentials.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata, OpenClaw metadata, changelog released 2026-05-10) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
