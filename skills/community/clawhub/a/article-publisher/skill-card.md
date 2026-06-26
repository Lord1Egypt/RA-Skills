## Description: <br>
Automates browser-based publishing of self-media articles to Zhihu, Bilibili, Baijiahao, Toutiao, and Xiaohongshu with QR login and local cookie persistence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phoenix1630](https://clawhub.ai/user/phoenix1630) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, operators, and publishing teams use this skill to log in to supported content platforms, check login status, and publish prepared articles to one or more logged-in accounts through browser automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish real content to logged-in public accounts. <br>
Mitigation: Use testMode first, name exact target platforms, avoid publish_to_all unless intended, and review generated content before live posting. <br>
Risk: The skill stores login cookies locally. <br>
Mitigation: Use dedicated accounts where practical, keep local cookie data private, and clear stored data when access is no longer needed. <br>
Risk: Browser automation depends on Playwright and downloaded Chromium binaries. <br>
Mitigation: Update and pin Playwright deliberately, and use trusted browser download sources before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/phoenix1630/article-publisher) <br>
- [Publisher Profile](https://clawhub.ai/user/phoenix1630) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Text status messages with optional structured data from tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May open browser sessions, save local cookies, and publish live posts when not run in test mode.] <br>

## Skill Version(s): <br>
1.5.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
