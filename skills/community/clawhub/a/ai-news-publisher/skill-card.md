## Description: <br>
Fetches AI news from 36Kr or Huxiu, helps rewrite it as a WeChat-ready article, and publishes the Markdown article to a WeChat Official Account draft box. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anydebug](https://clawhub.ai/user/anydebug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators and developers use this skill to collect current AI industry news, transform selected stories into WeChat-style Markdown articles, and create WeChat Official Account drafts for review before publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses WeChat Official Account credentials to create drafts. <br>
Mitigation: Store credentials outside shared documentation, restrict account access, and review every generated draft before publication. <br>
Risk: The publish script can install an unpinned global Node.js CLI. <br>
Mitigation: Preinstall and pin @wenyan-md/cli in a controlled environment before running the skill. <br>
Risk: The scraper can fetch arbitrary article URLs and supports stealth-style fetching. <br>
Mitigation: Use only authorized news sources, avoid stealth scraping unless permitted, and do not pass private or unrelated local content to the scripts. <br>
Risk: The publish script can modify supplied Markdown files by adding cover metadata. <br>
Mitigation: Run it on generated article copies and inspect the final Markdown before submitting it to WeChat. <br>


## Reference(s): <br>
- [Writing Guide](artifact/references/writing-guide.md) <br>
- [Scrapling Fetching Guide](artifact/references/scrapling-fetching.md) <br>
- [Scrapling Parsing API Guide](artifact/references/scrapling-parsing.md) <br>
- [36Kr AI Channel](https://www.36kr.com/information/AI/) <br>
- [Huxiu AI Channel](https://www.huxiu.com/channel/106.html) <br>
- [WeChat Official Account Platform](https://mp.weixin.qq.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown articles, JSON news lists, shell commands, and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated WeChat drafts should be reviewed before publication.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
