## Description: <br>
Auto Video Analyzer extracts video key frames with FFmpeg and uses AI vision to produce structured video analysis reports on Windows, macOS, and Linux. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shishenbaiye](https://clawhub.ai/user/shishenbaiye) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to inspect local video files, extract representative frames, analyze visual content, and return a structured report. It also supports deeper sampling modes for detailed review and debugging of video behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: First use can automatically download and run unpinned GitHub shell scripts on the user's machine. <br>
Mitigation: Review the helper scripts before use, pin them to a specific commit with checksums when possible, and require explicit confirmation before first download or execution. <br>
Risk: Video frames and copied video files may contain sensitive content and can remain in workspace analysis directories. <br>
Mitigation: Avoid sensitive videos unless the analysis location is understood, and clean generated tool and analysis directories after use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shishenbaiye/auto-video-analyzer) <br>
- [Source Repository](https://github.com/shishenbaiye/auto-video-analyzer) <br>
- [Tool Scripts Directory](https://github.com/shishenbaiye/auto-video-analyzer/tree/main/tools) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with extracted-frame analysis and optional shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FFmpeg and may create temporary video-analysis files in the workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
