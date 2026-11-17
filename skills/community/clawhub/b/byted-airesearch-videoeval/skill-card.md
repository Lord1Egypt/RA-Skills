## Description:

Creates and checks long-running video material evaluation tasks, including submission, task listing, and detail/result retrieval for video evaluation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to submit local MP4 creative assets for video material evaluation, then check task lists or task details later for status and results. The skill is intended for evaluation-task workflows, not generic video upload.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An API-host override could redirect API keys, prompts, and uploaded videos away from the expected Volcengine host.

Mitigation: Run only in a controlled environment and ensure BYTED_AIRESEARCH_VIDEOEVAL_BASE_URL is unset or pinned to https://console.volcengine.com before submitting videos or prompts.

Risk: API keys passed on the command line may appear in shell history, process listings, or logs.

Mitigation: Prefer BYTED_AIRESEARCH_VIDEOEVAL_API_KEY for real credentials and rotate any key previously used in shell commands or logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/volcengine-skills/skills/byted-airesearch-videoeval)
- [Volcengine API key console](https://console.volcengine.com/datatester/ai-research/audience/list?tab=apikey)
- [Volcengine attachment upload endpoint](https://console.volcengine.com/datatester/compass/api/v3/survey/attachment)
- [Volcengine evaluation task endpoint](https://console.volcengine.com/datatester/compass/api/v3/survey/task)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls]

**Output Format:** [Natural-language Markdown summaries with JSON script envelopes for agent use]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Submissions are non-blocking; task list and detail queries return normalized status and result data for later human-readable summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
