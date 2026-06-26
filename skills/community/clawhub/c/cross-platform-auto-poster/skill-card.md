## Description: <br>
Automates cross-platform social-media content generation and posting workflows for Xiaohongshu, TikTok, and YouTube, including generated posts, video composition, browser upload flows, and reposting workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiatian5](https://clawhub.ai/user/xiatian5) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, operators, and developers use this skill to generate, prepare, and publish social-media content across supported platforms. It is especially oriented toward Xiaohongshu image or video posts and TikTok/YouTube video reposting workflows that require account setup and supervised publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores logged-in social-media session state for real accounts. <br>
Mitigation: Use dedicated accounts, keep auth files out of version control, remove saved sessions when no longer needed, and supervise each publishing session. <br>
Risk: Automated posting can affect account reputation or trigger platform enforcement. <br>
Mitigation: Review generated content before publishing, limit posting frequency, and follow each platform's community and automation rules. <br>
Risk: Reposting or deduplicating third-party videos can create copyright or licensing exposure. <br>
Mitigation: Use reposting workflows only for content the operator owns or is licensed to redistribute, and retain records of permissions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xiatian5/cross-platform-auto-poster) <br>
- [Publisher Profile](https://clawhub.ai/user/xiatian5) <br>
- [xiaohongshu-content-automation](https://clawhub.ai/skills/xiaohongshu-content-automation) <br>
- [playwright-browser-automation](https://clawhub.ai/skills/playwright-browser-automation) <br>
- [remotion-video-toolkit](https://clawhub.ai/skills/remotion-video-toolkit) <br>
- [image_generate](https://clawhub.ai/skills/image-generate) <br>
- [FFmpeg Downloads](https://ffmpeg.org/download.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JavaScript examples, shell commands, and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of generated media paths, account configuration, browser-upload preparation, and JSONL publish logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
