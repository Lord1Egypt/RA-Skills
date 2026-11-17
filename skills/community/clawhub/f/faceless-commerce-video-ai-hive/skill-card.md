## Description:

This skill helps merchants, reviewers, and small teams turn faceless commerce video requests into a reviewable production plan, shot script, prompts, runnable AI-HIVE video-generation commands, task records, and acceptance checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, merchants, marketing teams, and agent developers use this skill to plan and generate faceless product-promotion videos without relying on a visible presenter. It supports scripts, prompts, AI-HIVE media uploads and asynchronous video jobs, local ffmpeg checks, and delivery review for platform-ready short video assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can store an AI-HIVE API key and send it to a configurable API server.

Mitigation: Use only the official AI-HIVE base URL, review AI_HIVE_BASE_URL and ~/.ai-hive/config.json before execution, and use a limited or low-balance API key.

Risk: Selected images, video, or audio can be uploaded to AI-HIVE or object storage as part of generation jobs.

Mitigation: Upload only media the user is authorized to share and review final parameters before submitting any generation task.

Risk: Generation jobs may incur cost and create asynchronous outputs that need review.

Mitigation: Confirm prompt, mode, routing, price snapshot, and task parameters before paid generation; use a small sample before batch work.

Risk: Local video editing commands invoke ffmpeg or ffprobe on user-selected files.

Mitigation: Run the tools in a dedicated environment and keep original media files separate from edited outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/faceless-commerce-video-ai-hive)
- [Publisher profile](https://clawhub.ai/user/wubin1836)
- [AI-HIVE chat and API key page](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with bash commands, JSON task records, generated media file paths, and checklist-style review notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JSON briefs and downloaded video or image files; AI-HIVE generation can submit paid asynchronous jobs after user review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
