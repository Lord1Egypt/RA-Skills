## Description:

Helps merchants and brand teams turn authorized customer posts, buyer-show media, and UGC clips into reviewable Chinese ad-production workflows, scripts, prompts, shell commands, and AI-HIVE generation tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants, brand teams, and marketing operators use this skill to transform authorized buyer-show or UGC materials into ad briefs, shot plans, prompts, editing commands, AI-HIVE generation tasks, and acceptance checklists for ecommerce and social advertising.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles AI-HIVE API keys and may read credentials from environment variables or a local config file.

Mitigation: Use only an API key approved for this machine, avoid pasting real keys into prompts or logs, and keep local credential files permission-restricted.

Risk: The workflow can upload customer images, videos, or audio to AI-HIVE before generation.

Mitigation: Upload only media that is authorized for reuse, keep the API base URL at the official endpoint, and review source assets for privacy, trademark, and consent issues before submission.

Risk: Generation tasks may be billable and can be submitted asynchronously.

Mitigation: Confirm model, routing mode, parameters, pricing snapshot, and expected output count before submitting generation jobs; use small samples before batch runs.

Risk: Local editing commands can transform or write media files.

Mitigation: Inspect generated commands before running them, preserve original files, and write outputs to separate paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/customer-post-to-ad-ai-hive)
- [AI-HIVE chat and API access](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API base endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON artifacts, Python command examples, shell commands, task records, and checklist items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AI-HIVE task IDs, pricing snapshots, model/routing choices, generated media download locations, and local ffmpeg processing commands when the workflow is executed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
