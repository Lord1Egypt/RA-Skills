## Description: <br>
fastfish 开源精简版，帮助代理整理微信公众号内容、执行本地敏感词检测、拉取每日热点并生成本地 HTML 预览；微信发布、授权和原创度检测需要商业版。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[superxs777](https://clawhub.ai/user/superxs777) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content operations teams use this skill to guide an agent through local fastfish-lite CLI workflows for WeChat article formatting, local compliance checks, HTML preview, and daily-hot-topic retrieval or push setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing or running fastfish-lite involves third-party code and Python dependencies. <br>
Mitigation: Review the linked repository and dependencies, use a pinned trusted release, and run in an isolated non-root environment before deployment. <br>
Risk: The skill uses API keys and webhook credentials for authenticated access and hot-topic push channels. <br>
Mitigation: Keep credentials in .env only, do not display or commit them, and enable push channels only where the operator controls the destination. <br>
Risk: Scheduled hot-topic tasks can push content repeatedly or to the wrong channel if misconfigured. <br>
Mitigation: Create, edit, or remove cron jobs only after explicit operator approval and verify the selected channel before enabling recurring pushes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/superxs777/fastfish-lite) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides CLI invocation and configuration; it does not itself publish to WeChat.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
