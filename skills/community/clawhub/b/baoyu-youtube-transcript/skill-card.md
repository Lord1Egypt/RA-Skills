## Description: <br>
Downloads YouTube video transcripts, subtitles, metadata, and cover images by URL or video ID, with support for multiple languages, translation, chapters, speaker identification, and cached re-formatting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimliu](https://clawhub.ai/user/jimliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to fetch YouTube captions, transcripts, thumbnails, and metadata from a URL or video ID, then save or reformat them as Markdown or SRT. It is useful for transcript capture, subtitle generation, language selection, translation, chapter organization, and speaker-labeled transcript workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may run yt-dlp or related local tools when direct YouTube transcript access is blocked. <br>
Mitigation: Install and use the skill only in environments where local tool execution for transcript retrieval is acceptable, and review tool availability before running fallback paths. <br>
Risk: Setting YOUTUBE_TRANSCRIPT_COOKIES_FROM_BROWSER can allow fallback transcript retrieval to use browser login state for YouTube. <br>
Mitigation: Leave YOUTUBE_TRANSCRIPT_COOKIES_FROM_BROWSER unset unless authenticated YouTube access is explicitly intended and approved. <br>
Risk: Speaker identification post-processing overwrites the Markdown transcript generated for that run. <br>
Mitigation: Keep raw transcript and cache outputs separately when preserving the unprocessed transcript is important. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/jimliu/baoyu-youtube-transcript) <br>
- [Source Homepage](https://github.com/JimLiu/baoyu-skills#baoyu-youtube-transcript) <br>
- [Speaker Transcript Prompt](prompts/speaker-transcript.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown transcript files, SRT subtitle files, JSON cache files, cover images, and stdout status or transcript-list output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can cache raw transcript data, metadata, sentence segmentation, and cover images under youtube-transcript/ for later re-formatting.] <br>

## Skill Version(s): <br>
1.117.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
