## Description: <br>
One-stop AI video production from script to final cut, with intelligent engine routing, lip-sync digital avatars, and automated marketing strategy integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, and automation teams use this skill to plan and generate short-form AI videos, lip-sync digital avatar videos, captions, voiceover fallback paths, and platform-ready delivery metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may write media files and run command-line media tools. <br>
Mitigation: Run it in a sandboxed workspace, keep command execution scoped to expected media operations, and review generated file paths before writing. <br>
Risk: The workflow can call external AI, TTS, and video-generation APIs. <br>
Mitigation: Keep API keys in environment variables, restrict API scopes and quotas, and avoid sending sensitive or unlicensed source material. <br>
Risk: The artifact describes optional publishing of generated videos. <br>
Mitigation: Require explicit human confirmation and review the video, subtitles, rights, and platform metadata before any posting step. <br>
Risk: The security summary flags insufficient scoping and confirmation guidance. <br>
Mitigation: Treat deployment as higher risk until local policy adds confirmation gates for publication and non-media command execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/ai-video-studio-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance and JSON-style status objects, with optional file paths or URLs for generated media.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or produce video, subtitle, audio, and metadata outputs through external AI, TTS, video-generation, and media tooling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; artifact frontmatter reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
