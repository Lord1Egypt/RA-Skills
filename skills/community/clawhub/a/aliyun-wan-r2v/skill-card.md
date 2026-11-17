## Description:

Use when generating reference-based videos with Alibaba Cloud Model Studio Wan R2V models (wan2.6-r2v-flash, wan2.6-r2v).

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare and validate Alibaba Cloud Wan reference-to-video requests, including multi-shot generation from reference video or image material while preserving character style.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials and generated payload files may contain Alibaba Cloud API keys, prompts, media URLs, task IDs, or other sensitive project details.

Mitigation: Use a scoped Alibaba Cloud API key, avoid committing credentials or generated request files, and review saved outputs before sharing.

Risk: The helper depends on local Python tooling and the DashScope SDK, so dependency or environment drift can affect request preparation.

Mitigation: Install and run the skill in a dedicated virtual environment and validate the helper script before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cinience/skills/aliyun-wan-r2v)
- [Alibaba Cloud Wan video-to-video API reference](https://help.aliyun.com/zh/model-studio/wan-video-to-video-api-reference)
- [Alibaba Cloud newly released models](https://help.aliyun.com/zh/model-studio/newly-released-models)
- [Alibaba Cloud reference-to-video documentation](https://help.aliyun.com/zh/model-studio/reference-to-video)
- [Alibaba Cloud Model Studio models](https://help.aliyun.com/zh/model-studio/models)
- [Bundled source references](references/sources.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Files, Guidance]

**Output Format:** [Markdown guidance with JSON request files and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save request payloads, task outputs, generated video artifacts, and polling snapshots under the configured output directory.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
