## Description: <br>
Automatically trims single-speaker videos by detecting and removing silence and filler to produce rough cuts with quality scoring and transcript-based deduplication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuchenggong19851114-design](https://clawhub.ai/user/zhuchenggong19851114-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to rough-cut single-speaker videos such as vlogs, tutorials, podcasts, and knowledge-sharing clips. It helps select candidate segments, remove repeated transcript content, produce edited MP4 clips, and generate processing reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Batch mode can recursively delete a user-specified work directory without containment checks. <br>
Mitigation: Run the skill only in a dedicated empty work directory, and do not pass home, project, downloads, or other valuable directories as the batch work directory. <br>
Risk: Generated reports and work files may contain transcripts from source videos. <br>
Mitigation: Treat reports, transcript files, and working directories as sensitive content and restrict or remove them after review. <br>
Risk: The Whisper dependency is unpinned, which can affect reproducibility and supply-chain review. <br>
Mitigation: Pin and review the openai-whisper dependency before controlled or repeatable deployments. <br>


## Reference(s): <br>
- [Auto Video Cut on ClawHub](https://clawhub.ai/zhuchenggong19851114-design/auto-video-cut) <br>
- [FFmpeg Downloads](https://ffmpeg.org/download.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and generated file descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled workflow can produce edited MP4 clips, Markdown reports, temporary transcript files, and batch concatenation outputs when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
