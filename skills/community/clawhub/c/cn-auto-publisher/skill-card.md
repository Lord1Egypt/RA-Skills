## Description: <br>
多平台内容自动发布，支持将内容发布为知乎回答、知乎文章或小红书图文笔记。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and operators use this skill to automate publishing prepared Chinese-language content to Zhihu questions, Zhihu articles, and Xiaohongshu notes. It is intended for users who can review the content and target destination before allowing the agent to publish. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically publish to real Zhihu and Xiaohongshu accounts. <br>
Mitigation: Review the content and target URL manually before execution, and prefer adding a confirmation or draft-only step before publishing. <br>
Risk: Reusable login cookies are stored on disk under ~/.qclaw. <br>
Mitigation: Use only accounts you are willing to automate, protect the cookie files, and delete them after use when persistence is not needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-auto-publisher) <br>
- [Publisher profile](https://clawhub.ai/user/freedompixels) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Guidance, Text] <br>
**Output Format:** [Markdown guidance with shell commands and JSON status output from publishing scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May launch browser automation, request manual login, publish to live platform accounts, and store reusable cookies under ~/.qclaw.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
