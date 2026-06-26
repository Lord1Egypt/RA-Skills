## Description: <br>
Extract and analyze Bilibili video content using yt-dlp, including video metadata, danmaku, subtitles, creator profile data, and series or collection information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuya227939](https://clawhub.ai/user/xuya227939) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, researchers, and content analysts use this skill to inspect Bilibili URLs, run local extraction commands, parse structured metadata or comment data, and present findings as readable Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser login cookies can expose authenticated Bilibili session data when passed to yt-dlp. <br>
Mitigation: Use cookies only when necessary, prefer a dedicated browser profile or limited account, and never share, upload, echo, or log exported cookies. <br>
Risk: The skill guides agents to run local shell commands and fetch third-party Bilibili data, so access limits, regional restrictions, or unavailable media can affect completeness. <br>
Mitigation: Review commands before execution, keep extraction local, and disclose access failures or restrictions in the final analysis. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xuya227939/bilibili-research-kit) <br>
- [Publisher profile](https://clawhub.ai/user/xuya227939) <br>
- [SnapVee homepage](https://snapvee.com) <br>
- [Support issue tracker](https://github.com/xuya227939/bilibili-research-kit/issues) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands, JSON parsing guidance, and tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local yt-dlp output files, subtitle files, or danmaku XML fetched with curl; no API key is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
