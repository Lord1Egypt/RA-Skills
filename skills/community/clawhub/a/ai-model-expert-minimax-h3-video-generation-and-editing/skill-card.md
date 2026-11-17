## Description:

This skill helps creators and marketing teams use AI-HIVE to generate Minimax H3 videos from text and optional image, video, or audio references, then submit, poll, and download results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, video editors, ecommerce teams, and marketing teams use this skill to prepare prompts and media references for Minimax H3 video generation through AI-HIVE. The workflow supports task submission, progress checks, and downloading generated video results for advertising, product, social media, and short-form content production.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected media are uploaded to AI-HIVE for generation.

Mitigation: Install only if AI-HIVE is trusted, and avoid uploading sensitive, confidential, or unlicensed media.

Risk: The workflow downloads generated results to local storage and may create sizable media files.

Mitigation: Use a dedicated output directory, review downloaded files and disk usage, and use no-download mode for testing.

Risk: Changing the API base URL can redirect requests and uploaded media to another service.

Mitigation: Avoid overriding the base URL unless the replacement service is fully trusted.

Risk: The release security summary flags broad implicit activation.

Mitigation: Confirm user intent before invoking the workflow, especially when prompts include uploads, downloads, or paid generation tasks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-minimax-h3-video-generation-and-editing)
- [AI-HIVE entry point](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash commands; CLI runs can return JSON task data and downloaded video files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated media is saved to the configured output directory unless the user chooses no-download mode.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
