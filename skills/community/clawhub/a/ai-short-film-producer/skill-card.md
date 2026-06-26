## Description: <br>
AI短剧制作助手 | AI Short Film Producer helps agents plan and produce low-cost AI short films by creating scripts and shot plans, generating video and TTS assets through third-party APIs, and assembling local outputs with FFmpeg and Python. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hitjcl](https://clawhub.ai/user/hitjcl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, developers, and production-oriented agent users can use this skill to turn a theme, script, or short-form video idea into a structured short-film production workflow. The skill guides storyboarding, prompt preparation, TTS generation, local FFmpeg/Python assembly, subtitle creation, asset export, cost estimation, and review iterations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may send prompts, scripts, voice text, and media to third-party generation services. <br>
Mitigation: Review the content before submission, avoid sensitive or confidential material, and use temporary or access-limited public links when an API requires reachable media. <br>
Risk: The workflow requires API credentials and may incur usage-based costs during retries or batch jobs. <br>
Mitigation: Use a scoped or low-balance API key, confirm pricing and retry limits before running batches, and monitor API usage during generation. <br>
Risk: The workflow writes generated media, subtitles, matrices, and final videos to local export folders. <br>
Mitigation: Choose the export folder deliberately, inspect generated files before sharing, and avoid overwriting unrelated project assets. <br>
Risk: Generated video, voice, subtitles, or timing may be inaccurate or unsuitable for release without review. <br>
Mitigation: Use the documented production review loop to check audio-video sync, subtitle accuracy, visual repetition, quality issues, and timing before publishing. <br>


## Reference(s): <br>
- [AI Short Film Production Workflow](references/production_workflow.md) <br>
- [Sucuang API Interface Notes](references/sucuang_api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and shell/Python command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local media file structures, API request payloads, FFmpeg commands, Python snippets, and review checklists.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
