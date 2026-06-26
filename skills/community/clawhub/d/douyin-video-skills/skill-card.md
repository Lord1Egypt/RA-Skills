## Description: <br>
Search Douyin videos, filter and validate a selected result, extract its spoken transcript, and produce cleaned transcript files with correction notes. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[poca233](https://clawhub.ai/user/poca233) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and content researchers use this skill to collect candidate Douyin videos, confirm that the opened video matches the intended search result, and create transcript materials for research, competitive analysis, or creator workflow preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A logged-in Douyin browser profile can expose account session data or local profile paths. <br>
Mitigation: Use a dedicated browser profile for this workflow and keep the profile directory private. <br>
Risk: Extracted audio is sent to SiliconFlow for transcription and requires an API key. <br>
Mitigation: Use a scoped API key where possible, store it outside shared files, and avoid processing audio that should not leave the local environment. <br>
Risk: Output folders can contain source links, transcripts, metadata, and downloaded media derived from third-party content. <br>
Mitigation: Keep generated outputs private and review copyright, platform, and privacy obligations before reuse or distribution. <br>
Risk: Search results or opened video modals may not match the intended target video. <br>
Mitigation: Use the built-in title and modal validation workflow before extracting transcripts, and manually review results when confidence is low. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/poca233/douyin-video-skills) <br>
- [Filter Rules for Douyin Video Selection](references/filter-rules.md) <br>
- [douyin-video-skills publish copy](references/publish-copy.md) <br>
- [SiliconFlow API key page](https://cloud.siliconflow.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash examples, JSON metadata, local transcript files, and correction notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a local output directory containing meta.json, source-link.txt, transcript.md, transcript-raw.md, transcript-clean.md, and transcript-fixes.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
