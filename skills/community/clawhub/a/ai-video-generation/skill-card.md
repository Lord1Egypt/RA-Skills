## Description:

Generate AI videos with Google Veo, Seedance, Wan, Grok, and 40+ other models through the inference.sh CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[okaris](https://clawhub.ai/user/okaris)

### License/Terms of Use:


## Use Case:

Developers, creators, and marketing teams use this skill to generate video content, animate source images, create avatar or lipsync clips, upscale videos, add foley sound, and assemble media workflows through inference.sh commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documentation includes a remote pipe-to-shell installer and unpinned package commands that could execute code that was not reviewed with this release.

Mitigation: Use a pinned, inspectable CLI installation path with published checksums or signatures, avoid privileged shells for installation, and review optional related-skill installs separately.

Risk: Prompts, media, private URLs, and account credentials may be processed by inference.sh or model providers when commands are run.

Mitigation: Do not submit sensitive prompts, media, private URLs, credentials, or regulated data unless the user accepts the relevant provider processing terms.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/okaris/skills/ai-video-generation)
- [inference.sh](https://inference.sh)
- [Running Apps](https://inference.sh/docs/apps/running)
- [Streaming Results](https://inference.sh/docs/api/sdk/streaming)
- [Content Pipeline Example](https://inference.sh/docs/examples/content-pipeline)
- [CLI Checksums](https://dist.inference.sh/cli/checksums.txt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON inputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may submit prompts, images, audio, video, and URLs to inference.sh-hosted apps or third-party model providers.]

## Skill Version(s):

0.1.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
