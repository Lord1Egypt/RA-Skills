## Description:

Runs selected RunningHub-hosted ComfyUI workflows for generating multilingual video, short-form video, and advertising voiceover outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emwstudio](https://clawhub.ai/user/emwstudio)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to configure a RunningHub host and API key, select an emwstudio workflow, provide workflow inputs, launch the task, and receive the generated result URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: RunningHub API keys may be stored in local agent configuration, sent to the configured host, and exposed in output or process arguments.

Mitigation: Install only after review, use a dedicated RunningHub key with limited exposure, avoid sharing logs that may contain arguments or tool output, and rotate the key if it is exposed.

Risk: The skill runs shell and network helper scripts as part of normal workflow execution.

Mitigation: Run it in a least-privilege environment, review the scripts before enabling execution tools, and allow network access only to trusted RunningHub hosts.

Risk: A configurable host can redirect API-key-bearing requests if set to an untrusted value.

Mitigation: Validate the configured host before use and restrict it to www.runninghub.cn or www.runninghub.ai.

Risk: The artifact includes referral-oriented registration and credit guidance.

Mitigation: Review public-facing prompts and remove mandatory referral promotion before commercial deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/emwstudio/skills/emwstudio)
- [ClawHub publisher profile](https://clawhub.ai/user/emwstudio)
- [RunningHub China service](https://www.runninghub.cn/)
- [RunningHub international service](https://www.runninghub.ai/)
- [Workflow catalog](artifact/data/workflows.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown messages with JSON tool calls and generated media result URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a RunningHub API key for the configured RunningHub host.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
