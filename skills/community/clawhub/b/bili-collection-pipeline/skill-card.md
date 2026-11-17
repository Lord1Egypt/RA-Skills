## Description:

Bili Collection Pipeline helps agents fetch Bilibili collections or YouTube playlists, download media, transcribe audio with Whisper, semantically segment transcripts, and write Markdown knowledge-base files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaozishan](https://clawhub.ai/user/xiaozishan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content-operations users can use this skill to turn Bilibili collections or YouTube playlists into resumable batches of Markdown transcripts with semantic paragraph segmentation. It is suited for building searchable personal or team knowledge bases from permitted media sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted collection JSON could abuse unsafe video ID handling during transcription.

Mitigation: Only process collection JSON files you generated or inspected, and validate video IDs before running transcription.

Risk: Temporary and output path handling could delete or overwrite files outside the intended workspace.

Mitigation: Run the pipeline in a dedicated temp/output directory and confine cleanup to exact files created by the workflow.

Risk: Optional LLM post-processing may send transcript content to a remote API.

Mitigation: Do not send sensitive transcripts to remote LLM services unless the data handling terms are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaozishan/skills/bili-collection-pipeline)
- [Publisher profile](https://clawhub.ai/user/xiaozishan)
- [you-get](https://github.com/soimort/you-get)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg](https://ffmpeg.org/)
- [Bilibili API endpoint](https://api.bilibili.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with command examples; generated artifacts are JSON collection manifests, progress JSON, and Markdown transcript files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow may download media, create temporary audio/video files, use local Whisper models, optionally call remote LLM APIs for post-processing, and resume from progress files.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
