## Description:

Turns Bilibili video URLs into transcripts, summaries, content analyses, scripts, prompts, slide content, and study notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panting09266-ai](https://clawhub.ai/user/panting09266-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-speaking creators, learners, and analysts use the skill to turn Bilibili videos into transcripts, summaries, content breakdowns, scripts, prompts, slide notes, and study notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan flags setup instructions that may lead users to share a complete API key in chat; video URLs are sent to a remote parser, and scan coverage was incomplete.

Mitigation: Do not share complete API keys in chat. Use a protected local configuration method and verify how the remote service handles video URLs and credentials before use.

Risk: ClawScan notes that promotional instructions may distract from the user's task.

Mitigation: Treat promotional guidance as optional and skip it when it is unrelated to the requested task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/panting09266-ai/skills/bilibili-video-studio)
- [Cue Omni Reader online experience](https://cuecue.cn/hub/omni-reader)

## Skill Output:

**Output Type(s):** [Text, Markdown, Video scripts, Structured JSON, Guidance]

**Output Format:** [Markdown reports and tables, plain text transcripts, video scripts, and JSON prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include timestamps, OCR text, scoring rubrics, and tables.]

## Skill Version(s):

1.2.6 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
