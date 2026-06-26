## Description: <br>
AI-optimized web search, image search and content extraction via BytePlus InfoQuest API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[infoquest-byteplus](https://clawhub.ai/user/infoquest-byteplus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search the web, find images, apply recency or site filters, and extract clean content from URLs through BytePlus InfoQuest. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, image queries, site filters, and URLs are sent to the BytePlus InfoQuest API. <br>
Mitigation: Do not use the skill for secrets, internal-only URLs, or confidential research topics unless third-party API use matches organizational policy. <br>
Risk: INFOQUEST_API_KEY is required for API access. <br>
Mitigation: Store the key in an environment variable or secret manager and avoid committing it to source control. <br>
Risk: Older Node.js runtimes require node-fetch support. <br>
Mitigation: Prefer Node.js 18+ or use a pinned node-fetch version when older Node.js support is needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/infoquest-byteplus/byted-infoquest-search) <br>
- [BytePlus InfoQuest Documentation](https://docs.byteplus.com/en/docs/InfoQuest/What_is_Info_Quest) <br>
- [BytePlus InfoQuest API Console](https://console.byteplus.com/infoquest/infoquests) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON search results for web and image search; Markdown-formatted extracted page content for URL extraction.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and INFOQUEST_API_KEY; sends search queries, image queries, site filters, and URLs to BytePlus InfoQuest.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
