## Description:

Uses AI-HIVE to generate TVC advertising videos from text and optional image, video, or audio references, then submit, track, and download generation tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, e-commerce teams, brand marketers, advertising agencies, producers, and social media operators use this skill to create TVC ads, product videos, social commerce clips, short drama clips, and other AIGC video assets through AI-HIVE.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, media files, and API credentials can be sent to external AI-HIVE endpoints.

Mitigation: Use the skill only with prompts and media you are comfortable sending to AI-HIVE, protect the API key, and avoid including sensitive or unauthorized content.

Risk: A custom API base URL could redirect credentials, prompts, or media to an endpoint the user did not intend to trust.

Mitigation: Keep the base URL at https://ai-hive.iclip.cn/api unless you deliberately trust and have verified another endpoint.

Risk: Automatic invocation may run the video workflow for vague requests or before cost, rights, and output details are clear.

Mitigation: Avoid enabling automatic use for vague requests; review generated commands and confirm budget, asset rights, and output requirements before execution.

Risk: Downloaded results may overwrite or clutter local output locations.

Mitigation: Choose an output directory where accidental overwrites or unexpected downloaded files would not matter.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-tvc-video)
- [AI-HIVE homepage](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON task output from the helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script can upload media, return task IDs, poll generation tasks, and download generated video files to a local output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
