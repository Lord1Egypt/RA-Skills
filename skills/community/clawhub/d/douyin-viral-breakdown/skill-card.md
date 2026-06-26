## Description: <br>
Analyzes Douyin short-video links to explain why a video may be popular, who it reaches, and what viewer behaviors it may trigger. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[csak47mu](https://clawhub.ai/user/csak47mu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content analysts use this skill to turn a Douyin video link into a structured breakdown of metadata, engagement signals, visual framing, audience fit, behavioral psychology, and reusable content patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch Douyin pages and download referenced videos, which may expose public URLs or media content to the local analysis environment. <br>
Mitigation: Use public links only, avoid sensitive content, and review fetched content before retaining or sharing results. <br>
Risk: The analysis workflow can create local video and frame files that may remain after the report is generated. <br>
Mitigation: Delete generated media files after analysis when retention is not needed. <br>
Risk: Some optional analysis paths may send image data or URLs to third-party services. <br>
Mitigation: Prefer first-party parsing and only use third-party services when the user accepts that data-sharing behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/csak47mu/douyin-viral-breakdown) <br>
- [Publisher profile](https://clawhub.ai/user/csak47mu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown analysis report with tables, calculated engagement metrics, and optional command or helper-code snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local video or frame files when the media-analysis workflow is used.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
