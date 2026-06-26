## Description: <br>
深度内容搜索工具，整合微信公众号、知乎、豆瓣、今日头条、百家号、微博、B站专栏等多平台内容抓取，支持获取微信公众号完整正文、知乎日报完整正文、豆瓣电影信息，并支持直接解析微信链接获取全文。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lyl340321](https://clawhub.ai/user/lyl340321) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to search across Chinese content platforms, retrieve full text where supported, parse WeChat article links, and return sourced text or JSON results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms and article URLs are sent to third-party services, and retrieved content may be stored locally when --output is used. <br>
Mitigation: Use non-sensitive queries and URLs, avoid storing confidential results, and review saved output paths before running the command. <br>
Risk: The skill depends on unpinned Python packages and live third-party platform behavior. <br>
Mitigation: Install in a controlled Python environment, keep result limits modest, and re-run validation when dependencies or platform responses change. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lyl340321/deep-content-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, files, shell commands, guidance] <br>
**Output Format:** [Plain text, Markdown-style summaries, JSON, or saved output files from command-line execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Searches default to three results per platform, can write retrieved content locally with --output, and require python3 plus requests, beautifulsoup4, lxml, and fake-useragent.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
