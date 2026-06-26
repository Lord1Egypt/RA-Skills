## Description: <br>
Helps an agent retrieve Bilibili video subtitles, generate summaries, and locate keyword timestamps using local helper scripts and cached subtitle files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BAIKEMARK](https://clawhub.ai/user/BAIKEMARK) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill when they want an agent to analyze Bilibili video content from a BVID or full video link. It supports subtitle extraction, structured video summaries, and timestamp lookup for specific topics mentioned in subtitles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a live Bilibili login session and stores cookies in plaintext. <br>
Mitigation: Use it only in a private workspace, do not paste cookies into chat, do not commit or share cookie.txt, and delete the cookie file when finished. <br>
Risk: Subtitle retrieval sends requests to Bilibili using the available login session. <br>
Mitigation: Invoke the skill only for Bilibili videos you explicitly intend to retrieve or analyze, and review generated files before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BAIKEMARK/bilibili-summary) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated subtitle files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local cookie.txt and subtitles_output files for cached subtitles and timestamp search.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
