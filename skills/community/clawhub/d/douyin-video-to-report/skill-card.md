## Description: <br>
Converts Douyin video links into HTML reports by fetching video, extracting audio and frames, transcribing Chinese speech, analyzing visuals, and preparing report content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wahtungl](https://clawhub.ai/user/wahtungl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to summarize permitted Douyin videos into shareable HTML reports with transcript and visual-analysis inputs. It is suited to workflows where local media processing and external CLI services are acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow bypasses platform checks and processes media that may require permission. <br>
Mitigation: Use only with videos the user has permission to process and require explicit consent before fetching or downloading media. <br>
Risk: URL-influenced shell commands may be unsafe when inputs are not constrained. <br>
Mitigation: Validate Douyin URLs and prefer safe subprocess argument lists over shell command strings. <br>
Risk: Downloaded video, extracted audio, screenshots, transcripts, and reports may persist on disk or be handled by external CLI services. <br>
Mitigation: Run in an isolated environment with scoped permissions and cleanup controls, and review external service handling before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wahtungl/douyin-video-to-report) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Pipeline script](artifact/douyin_pipeline.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with Python and shell command snippets; runtime script produces text transcripts, frame analysis, and report-ready files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes a user-supplied Douyin URL and may leave downloaded media, extracted audio, screenshots, transcripts, and reports on disk or with external CLI services.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
