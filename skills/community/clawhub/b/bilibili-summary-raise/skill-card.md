## Description: <br>
通过内置脚本获取B站视频信息并总结 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raise7727](https://clawhub.ai/user/raise7727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to fetch basic metadata for a Bilibili video from a URL or BV identifier and produce a short content summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends Bilibili BV identifiers to Bilibili's public API. <br>
Mitigation: Use it only when sharing the video identifier with Bilibili is acceptable. <br>
Risk: The artifact references scripts/fetch.js, but the included file is scripts/fecth.js, which may prevent reliable execution. <br>
Mitigation: Fix the script filename or the skill reference before relying on the skill in production. <br>


## Reference(s): <br>
- [Bilibili API 文档](references/api.md) <br>
- [Bilibili video info API](https://api.bilibili.com/x/web-interface/view?bvid=) <br>
- [ClawHub skill page](https://clawhub.ai/raise7727/bilibili-summary-raise) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API Calls, guidance] <br>
**Output Format:** [Markdown summary with video metadata fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes title, uploader, play count, likes, and a content summary when video data is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
