## Description: <br>
Routes Alibaba Cloud Model Studio requests to the appropriate local skill for Qwen text, coding, deep research, image, video, audio, search, and multimodal workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to route ambiguous Alibaba Cloud Model Studio requests to the right local capability-specific skill, clarify missing modality or operation details, and produce SDK, API, parameter, polling, or troubleshooting guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Provider API calls can consume Alibaba Cloud resources or incur costs. <br>
Mitigation: Confirm intent, region, identifiers, and operation scope before execution; start with a minimal read-only request when possible. <br>
Risk: DashScope API keys and saved outputs may expose credentials, prompts, task IDs, result URLs, or account details. <br>
Mitigation: Use scoped credentials, store the API key outside shared files, and review output artifacts before sharing them. <br>
Risk: Routing to a capability-specific sub-skill may lead to high-impact or mutating actions through provider APIs. <br>
Mitigation: Review the selected destination sub-skill and require explicit approval for high-impact or mutating operations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cinience/aliyun-modelstudio-entry) <br>
- [Alibaba Cloud Model Studio Models](https://help.aliyun.com/zh/model-studio/models) <br>
- [Alibaba Cloud Model Studio Newly Released Models](https://help.aliyun.com/zh/model-studio/newly-released-models) <br>
- [Alibaba Cloud Model Studio OpenAI-Compatible API](https://help.aliyun.com/zh/model-studio/openai-compatible) <br>
- [DashScope Async Tasks API](https://dashscope.aliyuncs.com/api/v1/tasks/) <br>
- [Artifact Source Links](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with routing tables, clarifying questions, API examples, and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference provider API calls, async task polling, local sub-skill paths, and saved evidence files.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
