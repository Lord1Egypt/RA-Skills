## Description: <br>
Downloads Bilibili video subtitles, chunks them for LLM processing, and supports summarization workflows for BV videos and SS/EP course episodes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DavinciEvans](https://clawhub.ai/user/DavinciEvans) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to retrieve Bilibili subtitles, split long subtitle text into manageable chunks, and prepare those chunks for structured LLM summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores reusable Bilibili login cookies or session data in local plaintext files. <br>
Mitigation: Use the QR login only in trusted workspaces and delete ~/.openclaw/workspace/bilibili_cookie.txt and bilibili_cheese_session.json after use when credentials no longer need to persist. <br>
Risk: Untrusted or malformed Bilibili video, season, or episode IDs may cause unexpected API requests or failures. <br>
Mitigation: Validate BV, SS, and EP identifiers before running the downloader scripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DavinciEvans/bilibili-subtitle-download-skill) <br>
- [Bilibili](https://www.bilibili.com/) <br>
- [Bilibili web-interface view API](https://api.bilibili.com/x/web-interface/view) <br>
- [Bilibili player API](https://api.bilibili.com/x/player/v2) <br>
- [Bilibili course episode API](https://api.bilibili.com/pugv/view/web/episode) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands plus RESULT_JSON metadata and chunked subtitle text files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes subtitle chunks under bili_temp and reports chunk paths in RESULT_JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
