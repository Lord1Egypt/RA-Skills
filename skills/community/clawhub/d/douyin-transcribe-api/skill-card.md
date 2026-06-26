## Description: <br>
Call the coze-js-api Douyin transcription endpoint and return transcript-ready results from Douyin URLs or share text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kyriswu](https://clawhub.ai/user/kyriswu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to transcribe or extract subtitles from Douyin/TikTok China share links. It normalizes copied share text, runs the bundled shell wrapper, and reports transcript API results or practical troubleshooting guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill transmits Douyin link/share text and DOUYIN_TRANSCRIBE_API_KEY to the devtool.uk transcription service. <br>
Mitigation: Use it only when the user trusts that service with the provided link and credential, and keep the key in the DOUYIN_TRANSCRIBE_API_KEY environment variable. <br>
Risk: Command output or troubleshooting logs could expose sensitive API key material if copied verbatim. <br>
Mitigation: Redact API key values before sharing logs or command output, consistent with the skill's safety guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kyriswu/douyin-transcribe-api) <br>
- [Douyin transcription API endpoint](https://coze-js-api.devtool.uk/transcribe-douyin) <br>
- [API key purchase and renewal page](https://devtool.uk/plugin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DOUYIN_TRANSCRIBE_API_KEY; redact API key values when sharing command output.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
