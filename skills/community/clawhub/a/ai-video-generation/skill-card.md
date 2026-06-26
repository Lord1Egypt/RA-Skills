## Description: <br>
Generates AI videos from prompts, images, audio, and media URLs using inference.sh CLI access to Google Veo, Seedance, Wan, Grok, OmniHuman, Fabric, HunyuanVideo, and related video models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okaris](https://clawhub.ai/user/okaris) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, creators, and marketing teams use this skill to generate or transform video content for social media, marketing, explainers, product demos, avatars, lipsync, upscaling, foley sound, and media assembly workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The quick start uses a remote CLI installer. <br>
Mitigation: Install only when inference.sh is trusted, and prefer the documented manual checksum-verification path when possible. <br>
Risk: Prompts, private images, internal URLs, audio, or video may be processed by inference.sh and its model providers. <br>
Mitigation: Avoid submitting confidential media or sensitive prompts unless the account, provider processing, and data handling terms are acceptable for the use case. <br>


## Reference(s): <br>
- [Ai Video Generation Skill on ClawHub](https://clawhub.ai/okaris/ai-video-generation) <br>
- [inference.sh](https://inference.sh) <br>
- [inference.sh CLI Installer](https://cli.inference.sh) <br>
- [inference.sh CLI Checksums](https://dist.inference.sh/cli/checksums.txt) <br>
- [Running Apps](https://inference.sh/docs/apps/running) <br>
- [Streaming Results](https://inference.sh/docs/api/sdk/streaming) <br>
- [Content Pipeline Example](https://inference.sh/docs/examples/content-pipeline) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON CLI inputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May involve prompts, image URLs, audio URLs, video URLs, and model-specific options passed to inference.sh apps.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
