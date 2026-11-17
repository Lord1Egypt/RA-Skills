## Description:

Calls the coze-js-api Douyin transcription endpoint to return transcript-ready results from Douyin URLs or copied share text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyriswu](https://clawhub.ai/user/kyriswu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to transcribe or extract subtitles from Douyin/TikTok China videos by passing a share link or copied share text through a configured transcription API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Douyin share text and the service API key to the external devtool.uk transcription service.

Mitigation: Use it only where sharing that data with the service is approved, store the key in DOUYIN_TRANSCRIBE_API_KEY, and redact secrets from logs or shared output.

Risk: Missing or invalid API keys can stop execution and surface purchase or renewal messaging.

Mitigation: Confirm a valid key is configured before running the skill and present the purchase or renewal link only when key handling requires it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kyriswu/skills/douyin-transcribe-api)
- [Publisher profile](https://clawhub.ai/user/kyriswu)
- [Douyin transcription API endpoint](https://coze-js-api.devtool.uk/transcribe-douyin)
- [API key purchase or renewal page](https://devtool.uk/plugin)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands and concise API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include success or failure status, selected response fields, and a practical next step.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
