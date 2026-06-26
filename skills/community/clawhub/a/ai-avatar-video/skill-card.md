## Description: <br>
Create AI avatar and talking head videos with OmniHuman, Fabric, PixVerse via inference.sh CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okaris](https://clawhub.ai/user/okaris) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, creators, marketers, educators, and localization teams use this skill to generate AI presenter, talking-head, lipsync, dubbing, and virtual-influencer video workflows through inference.sh CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installer commands may encourage piping a remote script directly to a shell. <br>
Mitigation: Prefer manual download and SHA-256 checksum verification for the inference.sh CLI before running it. <br>
Risk: Avatar, voice, audio, or video inputs may contain sensitive biometric or personal media. <br>
Mitigation: Submit only media that the user owns or is authorized to process, and avoid sensitive portraits, voices, or videos without consent. <br>
Risk: Media URLs are processed by external cloud services. <br>
Mitigation: Use a trusted inference.sh account and review data-handling expectations before sending private or regulated content. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/okaris/ai-avatar-video) <br>
- [inference.sh](https://inference.sh) <br>
- [inference.sh CLI Installer](https://cli.inference.sh) <br>
- [CLI Checksums](https://dist.inference.sh/cli/checksums.txt) <br>
- [Running Apps](https://inference.sh/docs/apps/running) <br>
- [Content Pipeline Example](https://inference.sh/docs/examples/content-pipeline) <br>
- [Streaming Results](https://inference.sh/docs/api/sdk/streaming) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces CLI-oriented instructions for external cloud avatar-video generation services.] <br>

## Skill Version(s): <br>
0.1.5 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
