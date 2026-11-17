## Description:

Transcribe earnings call audio via Whisper, analyze stock price data, and generate structured Feishu documents summarizing financial results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and finance teams use this skill to turn earnings-call audio and stock history CSV data into local transcripts, financial indicators, and Feishu-ready Markdown for review and publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default shared temporary output folder can retain or expose full earnings-call transcripts, summaries, and Feishu-ready content, and may be vulnerable to local tampering.

Mitigation: Use a private, user-owned output directory, inspect generated Feishu content before publishing, and delete transcripts and summaries when no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/earnings-call-processor)
- [ClawHub publisher profile](https://clawhub.ai/user/terrycarter1985)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands]

**Output Format:** [Local text transcript, JSON indicators, and Feishu-ready Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes transcript.txt, financial_indicators.json, and feishu_content.md under the selected output directory.]

## Skill Version(s):

3.0.0 (source: frontmatter, server release evidence, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
