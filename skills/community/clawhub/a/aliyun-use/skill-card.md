## Description: <br>
Aliyun Bailian(百炼) for LLM chat, and language translation. Use when you need to generate code, generate text with LLMs, or translate between languages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cnlangzi](https://clawhub.ai/user/cnlangzi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to call Alibaba Cloud Bailian/DashScope LLMs for chat, code generation, and translation after configuring an Aliyun Bailian API key. <br>

### Deployment Geography for Use: <br>
Global, subject to Alibaba Cloud service availability and the user's selected regional endpoint. <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, code snippets, and translation text are sent to Alibaba Cloud Bailian or the endpoint configured by ALIYUN_BAILIAN_API_HOST. <br>
Mitigation: Use only approved endpoints, use a dedicated API key, and avoid submitting secrets, regulated data, or confidential source code unless that provider is approved for the data. <br>
Risk: Region-bound API keys or an unintended API host can route requests to the wrong service endpoint. <br>
Mitigation: Set ALIYUN_BAILIAN_API_HOST deliberately and match it to the API key's region before using the skill. <br>


## Reference(s): <br>
- [AliYun Bailian API Reference](references/API.md) <br>
- [Available models](assets/models.json) <br>
- [Alibaba Cloud Bailian Console](https://bailian.console.aliyun.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON success/error objects and plain-text or streaming CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ALIYUN_BAILIAN_API_KEY; ALIYUN_BAILIAN_API_HOST can select a compatible endpoint.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
