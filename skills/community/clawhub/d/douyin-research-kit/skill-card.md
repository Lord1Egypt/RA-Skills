## Description: <br>
A content research toolkit for Douyin (抖音) that helps agents extract video metadata, captions, engagement stats, creator profiles, music information, hashtag trends, and live stream data using yt-dlp. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuya227939](https://clawhub.ai/user/xuya227939) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers, analysts, and developers use this skill to inspect Douyin videos, profiles, music pages, hashtags, and live streams, then turn yt-dlp output into research-ready summaries and Markdown tables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using browser cookies for Douyin access can expose authenticated session data if cookie values, command output, or cookie files are mishandled. <br>
Mitigation: Use a dedicated browser profile or Douyin-scoped cookie file, avoid printing or saving cookie values, and install yt-dlp from a trusted source. <br>
Risk: Douyin results may be incomplete or unavailable when content is deleted, region restricted, or a live stream is offline. <br>
Mitigation: Treat extraction results as availability-dependent and clearly report unavailable or restricted content instead of filling gaps. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xuya227939/douyin-research-kit) <br>
- [Project Homepage](https://snapvee.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON-field guidance, and tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local yt-dlp JSON output, subtitles, and browser-cookie configuration; no bundled code or API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact version fields) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
