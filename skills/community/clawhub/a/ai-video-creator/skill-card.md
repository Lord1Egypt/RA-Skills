## Description: <br>
AI Video Creator automates short-form healing atmosphere video production: topic selection, Jimeng AI clip generation, ffmpeg assembly with BGM, and optional Xiaohongshu publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jameswangchen](https://clawhub.ai/user/jameswangchen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, content operators, and developers use this skill to generate persona-driven vertical video prompts, assemble AI-generated clips with overlay text and BGM, and optionally publish the final short video to Xiaohongshu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Volcengine paid API quota and cloud credentials. <br>
Mitigation: Use dedicated or limited credentials where possible, monitor quota before runs, and avoid sharing terminal output that may expose key prefixes. <br>
Risk: The optional Xiaohongshu publishing path depends on a logged-in local publishing server and can post generated content to a social account. <br>
Mitigation: Keep the MCP server local and trusted, verify login status, and review the generated video, title, caption, tags, visibility, and schedule before publication. <br>
Risk: Generated video prompts and social copy may be inaccurate, unsuitable, or off-brand. <br>
Mitigation: Require human approval after content generation and again before publishing the final video. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jameswangchen/ai-video-creator) <br>
- [Environment setup guide](references/setup.md) <br>
- [Volcengine Jimeng API documentation](https://www.volcengine.com/docs/85621/1544715) <br>
- [Xiaohongshu MCP server](https://github.com/xpzouying/xiaohongshu) <br>
- [Pixabay Music](https://pixabay.com/music/) <br>
- [Free Music Archive](https://freemusicarchive.org/) <br>
- [Uppbeat](https://uppbeat.io/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with JSON content plans and shell commands; generated MP4 video and metadata files when executed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Volcengine credentials, ffmpeg, local BGM assets, and an optional local Xiaohongshu MCP publishing server.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
