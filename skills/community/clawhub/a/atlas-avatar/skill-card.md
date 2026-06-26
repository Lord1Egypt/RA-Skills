## Description: <br>
Create realtime passthrough AI avatar sessions with LiveKit WebRTC, view-only viewer tokens for multi-viewer watch, and offline lip-sync avatar videos using the Atlas API by North Model Labs, with optional Discord delivery of offline MP4 renders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eric-prog](https://clawhub.ai/user/eric-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create Atlas realtime avatar sessions, issue viewer tokens, manage session lifecycle actions, and generate offline lip-sync videos from image and audio inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires API credentials and may write them into local viewer configuration. <br>
Mitigation: Use scoped, revocable keys, keep generated .env.local files out of source control, and avoid optional viewer setup on shared machines. <br>
Risk: Face images, audio, prompts, and rendered videos may be sent to Atlas or optional third-party services. <br>
Mitigation: Upload only media and prompts that are approved for those services, and review the data flow before enabling Discord, ElevenLabs, Anthropic/LLM, or S3 integrations. <br>


## Reference(s): <br>
- [Atlas API reference](references/api-reference.md) <br>
- [North Model Labs API documentation](https://www.northmodellabs.com/api) <br>
- [North Model Labs examples](https://www.northmodellabs.com/examples) <br>
- [Atlas realtime example app](https://github.com/NorthModelLabs/atlas-realtime-example) <br>
- [ClawHub release page](https://clawhub.ai/eric-prog/atlas-avatar) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON API responses and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create Atlas API requests, LiveKit viewer tokens, local viewer setup files, and presigned offline render result links.] <br>

## Skill Version(s): <br>
1.0.9 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
