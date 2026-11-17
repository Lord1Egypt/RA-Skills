## Description: <br>
Bilibili All In One Free helps agents monitor Bilibili trends, download standard-resolution videos, track video statistics, and fetch playback or danmaku data through public APIs without login credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, media analysts, and content operators use this skill to query public Bilibili rankings and video metadata, compare engagement metrics, retrieve danmaku, and download 360p-1080p MP4 videos for offline review or content research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary marks the release suspicious because credential guidance and broad read/execute/write scope do not fully match the stated no-login public-API purpose. <br>
Mitigation: Review the skill before installing, do not provide API keys or session cookies unless the publisher clearly justifies them, and run it only in a workspace where command execution and file writes are acceptable. <br>
Risk: Video download actions can write files and fetch content from Bilibili public APIs. <br>
Mitigation: Confirm destination paths before allowing downloads and verify that downloaded content is appropriate for the intended workspace and use case. <br>
Risk: Frequent public API calls may be rate-limited or blocked. <br>
Mitigation: Use conservative request rates and reduce frequency after rate-limit or anti-abuse responses. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/bilibili-all-in-one-free) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell and Python examples plus JSON execution results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can include Bilibili ranking data, video metadata, download status, playback URLs, danmaku data, execution logs, and error details.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release evidence; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
