## Description: <br>
Creates and publishes Chinese metaphysics, guoxue, and I Ching short videos for Douyin using Volcengine image and video generation, Edge TTS dubbing, ffmpeg assembly, Douyin publishing, and backend verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinhuadeng](https://clawhub.ai/user/jinhuadeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and content creators use this skill to guide an agent through a reusable pipeline for generating, assembling, publishing, and verifying vertical Douyin guoxue short videos. It is intended for workflows that need multi-shot visual generation, Chinese voiceover, subtitles, AI-content declaration handling, and final backend verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can publish public Douyin posts using local account credentials before a person has reviewed the exact video, title, account, and AI-content declaration. <br>
Mitigation: Require manual final approval before any publish command runs, and verify the published item in the Douyin creator backend after publishing. <br>
Risk: Companion scripts and local credentials for Volcengine and Douyin are outside this skill card's bundled files. <br>
Mitigation: Review the referenced companion scripts before use and run with dedicated or least-privilege Volcengine keys and Douyin accounts where possible. <br>
Risk: AI-generated content declaration may be incomplete if automation cannot confirm the required Douyin UI clicks. <br>
Mitigation: Treat declaration status as unverified unless logs or manual review confirm the AI-content declaration was applied. <br>


## Reference(s): <br>
- [Prompt Patterns](references/prompt-patterns.md) <br>
- [Publish Notes](references/publish-notes.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jinhuadeng/douyin-guoxue-volcengine-pipeline) <br>
- [Publisher Profile](https://clawhub.ai/user/jinhuadeng) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline PowerShell, Python, ffmpeg, and CLI command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing workflow steps, prompt structure, publish checks, and final reporting fields; generated media and public posts are created by companion tools outside the skill itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
