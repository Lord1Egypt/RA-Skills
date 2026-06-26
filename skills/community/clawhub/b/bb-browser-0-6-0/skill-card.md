## Description: <br>
Turn any website into a CLI command. 36 platforms, 103 commands — Twitter, Reddit, GitHub, YouTube, Zhihu, Bilibili, Weibo, and more. Uses OpenClaw's browser directly, no extra extension needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gu-yunyu](https://clawhub.ai/user/gu-yunyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to run bb-browser site adapters through OpenClaw's browser and extract structured data from supported websites, including social, developer, finance, news, video, and knowledge platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands can read pages available in the user's current OpenClaw browser session, including logged-in website data. <br>
Mitigation: Use the skill only on accounts and browser profiles intended for extraction, and avoid running it against sensitive logged-in services. <br>
Risk: Extracted website data may include private or account-specific information. <br>
Mitigation: Review command output before sharing, storing, or using it in downstream workflows. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/gu-yunyu/bb-browser-0-6-0) <br>
- [Publisher profile](https://clawhub.ai/user/gu-yunyu) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration, Text, JSON] <br>
**Output Format:** [Markdown with inline bash code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands commonly produce structured website data and can be filtered with jq-style expressions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; artifact metadata version 0.6.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
