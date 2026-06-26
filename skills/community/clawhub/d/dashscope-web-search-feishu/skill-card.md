## Description: <br>
Searches the web with DashScope Qwen and can send image-search results to Feishu chats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Oreo992](https://clawhub.ai/user/Oreo992) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and OpenClaw users use this skill to answer time-sensitive web queries, run deeper source-backed searches, and optionally deliver image results into Feishu conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image mode handles Feishu bot credentials and can post images into chats. <br>
Mitigation: Use a narrowly permissioned Feishu bot, restrict allowed recipients, and avoid sensitive chats until the deployment has been reviewed. <br>
Risk: Security evidence reports unsafe network and token handling in the image pipeline. <br>
Mitigation: Fix TLS verification, protect or disable the temporary token cache, and add URL, size, content-type, and private-network blocking before enabling automatic image sending. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Oreo992/dashscope-web-search-feishu) <br>
- [OpenClaw](https://github.com/nicepkg/openclaw) <br>
- [DashScope](https://dashscope.aliyuncs.com/) <br>
- [DashScope Console](https://dashscope.console.aliyun.com/) <br>
- [Feishu Open Platform](https://open.feishu.cn/app/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown text with citations and optional Feishu image-message delivery] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports turbo, deep, agent, thinking, freshness, site-filtered, and image-search modes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
