## Description: <br>
Generate reference-based videos with Alibaba Cloud Model Studio Wan R2V models (wan2.6-r2v-flash, wan2.6-r2v). Use when creating multi-shot videos from reference video/image material, preserving character style, or documenting reference-to-video request/response flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content engineers use this skill to prepare Alibaba Cloud Wan reference-to-video requests, validate response shape, and document request and polling evidence for generated videos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and reference media are sent to Alibaba Cloud for video generation. <br>
Mitigation: Confirm the data is appropriate for Alibaba Cloud processing before use, and avoid submitting sensitive media unless the deployment has approved terms and controls. <br>
Risk: DashScope API keys or Alibaba Cloud credentials are required. <br>
Mitigation: Use a limited-purpose credential, keep it out of committed files, and rotate it if local output or logs may have exposed it. <br>
Risk: The helper installs an unpinned SDK dependency and writes request/output evidence locally. <br>
Mitigation: Install dependencies in a virtual environment, review dependency versions before production use, and inspect or clean the output directory after each run. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cinience/alicloud-ai-video-wan-r2v) <br>
- [Alibaba Cloud Wan video-to-video API reference](https://help.aliyun.com/zh/model-studio/wan-video-to-video-api-reference) <br>
- [Alibaba Cloud Model Studio newly released models](https://help.aliyun.com/zh/model-studio/newly-released-models) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration, JSON files] <br>
**Output Format:** [Markdown guidance with shell commands and generated JSON request files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes request payloads and response-validation evidence under the configured output directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter version is 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
