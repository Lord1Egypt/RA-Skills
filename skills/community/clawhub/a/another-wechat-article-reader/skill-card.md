## Description: <br>
Reads public WeChat article URLs and returns structured article metadata and plain-text content using a dedicated fetching script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pangahn](https://clawhub.ai/user/pangahn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill when a user provides a public mp.weixin.qq.com article URL and needs the article title, author, publication time, source URL, logs, and body text returned as structured data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs network retrieval for WeChat article URLs, while security evidence notes a documentation gap around explicit network-permission metadata. <br>
Mitigation: Confirm the agent only fetches user-provided mp.weixin.qq.com article URLs and ask the publisher to add explicit allowed-destination metadata. <br>
Risk: WeChat anti-crawling behavior or page changes can lead to blocked, empty, or incomplete article extraction. <br>
Mitigation: Review returned errors, status logs, and extracted content before relying on the result. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pangahn/another-wechat-article-reader) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [JSON object with article fields or an error object; skill guidance is Markdown with shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes source URL, fetch strategy, and execution logs for troubleshooting.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
