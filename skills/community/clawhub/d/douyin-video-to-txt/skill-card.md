## Description: <br>
抖音视频转文本知识库 — Download Douyin videos, transcribe to text via faster-whisper, save to Obsidian knowledge base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[afeicn](https://clawhub.ai/user/afeicn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge-base users use this skill to download a Douyin video, transcribe its speech locally with faster-whisper, and save the transcript and AI summary into an Obsidian note. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates local media, audio, transcript, and Markdown files, which may overwrite or clutter an existing notes location. <br>
Mitigation: Set OBSIDIAN_VAULT_PATH before use and review generated destination filenames before writing notes. <br>
Risk: Downloaded videos and generated transcripts may contain sensitive or copyrighted third-party content. <br>
Mitigation: Use only content the user is permitted to process and keep generated files in an appropriate local vault or temporary directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/afeicn/douyin-video-to-txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with bash and Python snippets, plus generated transcript text and Obsidian Markdown notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local video, audio, transcript, and Markdown note files; the Obsidian destination can be controlled with OBSIDIAN_VAULT_PATH.] <br>

## Skill Version(s): <br>
2.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
