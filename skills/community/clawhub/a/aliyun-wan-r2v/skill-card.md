## Description: <br>
Use when generating reference-based videos with Alibaba Cloud Model Studio Wan R2V models (wan2.6-r2v-flash, wan2.6-r2v). Use when creating multi-shot videos from reference video/image material, preserving character style, or documenting reference-to-video request/response flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to prepare and operate Alibaba Cloud Model Studio Wan R2V reference-to-video workflows, including request payloads, async polling, and output evidence handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Alibaba Cloud Model Studio requests may process user prompts and reference media with an external provider and may incur usage costs. <br>
Mitigation: Use this skill only when Alibaba Cloud Model Studio processing is intended, confirm region and operation scope before execution, and run a minimal read-only connectivity check first. <br>
Risk: API credentials can be exposed if copied into prompts, logs, or shared files. <br>
Mitigation: Use DASHSCOPE_API_KEY or Alibaba Cloud credentials from a scoped environment or credentials file, and avoid storing secrets in generated artifacts. <br>
Risk: Saved request payloads, task IDs, prompts, media URLs, polling snapshots, or generated videos may contain private information. <br>
Mitigation: Review, restrict, or delete saved output files before sharing or publishing evidence directories. <br>


## Reference(s): <br>
- [Aliyun Wan video-to-video API reference](https://help.aliyun.com/zh/model-studio/wan-video-to-video-api-reference) <br>
- [Aliyun Model Studio newly released models](https://help.aliyun.com/zh/model-studio/newly-released-models) <br>
- [Aliyun Model Studio reference-to-video](https://help.aliyun.com/zh/model-studio/reference-to-video) <br>
- [Aliyun Model Studio models](https://help.aliyun.com/zh/model-studio/models) <br>
- [Skill reference sources](references/sources.md) <br>
- [ClawHub skill page](https://clawhub.ai/cinience/aliyun-wan-r2v) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON files] <br>
**Output Format:** [Markdown guidance with shell commands and JSON request payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save request payloads, polling snapshots, task identifiers, and generated video output paths under output/aliyun-wan-r2v/.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
