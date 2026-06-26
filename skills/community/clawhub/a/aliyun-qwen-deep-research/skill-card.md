## Description: <br>
Use when a task needs Alibaba Cloud Model Studio Qwen Deep Research models to plan multi-step investigation, run iterative web research, and produce structured reports with citations or evidence summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and research agents use this skill to prepare Alibaba Cloud Qwen Deep Research requests, keep run settings organized, and capture structured research outputs with citations or evidence summaries. <br>

### Deployment Geography for Use: <br>
China mainland (Beijing region) <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Alibaba Cloud DashScope credentials. <br>
Mitigation: Protect DASHSCOPE_API_KEY or configured Alibaba Cloud credentials and run the helper from an isolated virtual environment. <br>
Risk: Research goals, request payloads, run settings, and report snapshots may be saved locally. <br>
Mitigation: Review saved files under output/aliyun-qwen-deep-research/ and delete sensitive or unneeded artifacts after use. <br>
Risk: The release evidence notes that this is a request-preparation/support skill rather than a complete research executor. <br>
Mitigation: Confirm generated request payloads and model responses before relying on reports or sharing results. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cinience/aliyun-qwen-deep-research) <br>
- [Qwen Deep Research documentation](https://help.aliyun.com/zh/model-studio/qwen-deep-research) <br>
- [Qwen Deep Research model updates](https://help.aliyun.com/zh/model-studio/newly-released-models) <br>
- [Alibaba Cloud Model Studio model list](https://help.aliyun.com/zh/model-studio/models) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON request payload files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores request payloads, run settings, and report snapshots under output/aliyun-qwen-deep-research/ unless OUTPUT_DIR is overridden.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
