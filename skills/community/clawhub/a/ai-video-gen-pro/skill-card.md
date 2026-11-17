## Description:

Ai Video Gen Pro helps agents generate videos with Google Veo, Seedance, Wan, Grok, and other inference.sh CLI models for text-to-video, image-to-video, lipsync, avatar animation, upscaling, and foley workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bingze00000](https://clawhub.ai/user/bingze00000)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for inference.sh commands and configuration guidance for generating social media videos, marketing content, explainer videos, product demos, AI avatars, lipsync videos, upscaled videos, and foley sound.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, image URLs, audio URLs, and video URLs may be sent to inference.sh or downstream external model services.

Mitigation: Avoid sensitive media and review the relevant service terms, privacy expectations, and data handling requirements before use.

Risk: Related npx skills add examples can install mutable third-party skills that may change future agent behavior.

Mitigation: Verify the source and pin or otherwise trust the exact skill version before installing related skills.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bingze00000/skills/ai-video-gen-pro)
- [inference.sh](https://inference.sh)
- [inference.sh CLI Install Instructions](https://raw.githubusercontent.com/inference-sh/skills/refs/heads/main/cli-install.md)
- [Running Apps](https://inference.sh/docs/apps/running)
- [Streaming Results](https://inference.sh/docs/api/sdk/streaming)
- [Content Pipeline Example](https://inference.sh/docs/examples/content-pipeline)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing CLI examples and model/app ID guidance; generated media is produced by external inference.sh services.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
