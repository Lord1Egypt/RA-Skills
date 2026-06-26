## Description: <br>
Route Alibaba Cloud Model Studio requests to the right local skill for Qwen Image, Qwen Image Edit, Wan Video, Wan R2V, Qwen TTS, Qwen ASR, advanced TTS variants, and related Model Studio capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill as an entry router when they need Alibaba Cloud Model Studio help but have not yet selected a specific text, image, audio, video, multimodal, retrieval, or document-understanding capability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can route work to Alibaba Cloud Model Studio services that require DashScope credentials and may incur API usage. <br>
Mitigation: Install it only when Model Studio services are intended, use a limited DASHSCOPE_API_KEY, and verify the downstream skill before execution. <br>
Risk: Generated artifacts or saved API response summaries may contain sensitive request or response content. <br>
Mitigation: Review and clear files under output/alicloud-ai-entry-modelstudio/ when they contain sensitive content. <br>
Risk: Unpinned SDK installation can change behavior as the dashscope package evolves. <br>
Mitigation: Consider pinning the dashscope package version in controlled environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cinience/alicloud-ai-entry-modelstudio) <br>
- [Official source list](references/sources.md) <br>
- [DashScope async task API](https://dashscope.aliyuncs.com/api/v1/tasks/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with routing tables, clarifying questions, API polling examples, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to downstream local skills and may save artifacts, command outputs, or API response summaries under output/alicloud-ai-entry-modelstudio/.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
