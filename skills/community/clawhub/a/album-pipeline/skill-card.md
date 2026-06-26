## Description: <br>
Album Pipeline automates an AI music album workflow from concept design through songwriting, lyrics formatting, MiniMax-based music and visual generation, audio transcoding, and release packaging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raylanlin](https://clawhub.ai/user/raylanlin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and music creators use this skill to coordinate a structured, multi-agent album production pipeline that creates songs, prompts, audio files, cover assets, promotional copy, compliance checks, and packaged release materials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can create many project files and packaged release artifacts. <br>
Mitigation: Run the skill in a dedicated project folder and review generated outputs before publication. <br>
Risk: The workflow calls external generation and media tooling, including MiniMax CLI, ffmpeg, ffprobe, and zip. <br>
Mitigation: Use trusted, configured tool installations and review commands before execution. <br>
Risk: Prompts and lyrics may contain confidential creative material before provider generation. <br>
Mitigation: Review generated prompts and lyrics before sending them to generation providers when confidentiality matters. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/raylanlin/album-pipeline) <br>
- [Publisher profile](https://clawhub.ai/user/raylanlin) <br>
- [MiniMax CLI](https://github.com/MiniMax-AI/cli) <br>
- [File Contracts](artifact/FILE_CONTRACTS.md) <br>
- [Production Pipeline Review](artifact/docs/production-pipeline-review.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documents, structured project files, shell command templates, media-generation prompts, audio artifacts, image/video assets, and zip packaging instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces many files across a dedicated album project workspace and relies on MiniMax CLI, ffmpeg, ffprobe, and zip for generation, transcoding, verification, and packaging.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
