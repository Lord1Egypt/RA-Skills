## Description:

Helps creators turn Douyin video links into transcripts, summaries, structural analyses, scripts, and generation prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panting09266-ai](https://clawhub.ai/user/panting09266-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and social media teams use this skill to understand Douyin videos and create transcripts, summaries, video breakdowns, scripts, and prompts based on them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance asks users to share a reusable API key in chat, which could expose the credential.

Mitigation: Use the local configuration option, restrict the credential file to the account owner, and rotate any key already shared in a conversation.

Risk: Video links are sent to Cue for remote parsing, parsing consumes credits, and the server retention promise has not been independently verified.

Mitigation: Avoid sending sensitive links, review the service's data handling terms, and check available credits before processing videos.

## Reference(s):

- [Cue Omni Reader online experience](https://cuecue.cn/hub/omni-reader)
- [ClawHub skill release](https://clawhub.ai/panting09266-ai/skills/douyin-video-studio)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance, Structured JSON]

**Output Format:** [Markdown text with headings and tables; structured JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content varies by the selected video task and may include transcripts, summaries, breakdowns, scripts, or prompts.]

## Skill Version(s):

1.1.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
