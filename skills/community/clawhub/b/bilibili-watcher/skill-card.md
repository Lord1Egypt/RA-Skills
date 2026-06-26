## Description: <br>
Fetch and read transcripts from Bilibili videos so an agent can summarize, answer questions about, or extract information from video content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiashuoji838-afk](https://clawhub.ai/user/jiashuoji838-afk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to retrieve Bilibili video transcripts for downstream summarization, question answering, keyword search, and information extraction. It is intended for Bilibili videos that provide closed captions or auto-generated subtitles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local Python helper that invokes yt-dlp against user-provided Bilibili URLs. <br>
Mitigation: Install and review yt-dlp separately in sensitive environments, and use the skill only for Bilibili links the user intends to process. <br>
Risk: Videos without closed captions or auto-generated subtitles may fail or produce no transcript. <br>
Mitigation: Confirm subtitle availability before relying on the transcript for summarization, Q&A, or extraction. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jiashuoji838-afk/bilibili-watcher) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text transcript with supporting Markdown guidance and bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires yt-dlp on PATH; transcript availability depends on Bilibili subtitle availability.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
