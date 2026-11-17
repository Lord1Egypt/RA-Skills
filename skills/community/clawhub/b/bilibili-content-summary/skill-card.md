## Description:

Extracts and summarizes Bilibili video and image-text content using audio download, ASR transcription or image OCR, LLM summarization, and Feishu delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zify9000](https://clawhub.ai/user/zify9000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to summarize Bilibili videos or image-text posts and deliver the resulting abstract, key points, and chapter breakdowns to a configured Feishu chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can send summaries and related metadata to an external Feishu chat automatically.

Mitigation: Verify the Feishu chat target and only enable automatic push when external delivery is acceptable.

Risk: The skill requires Bilibili, model-provider, OCR/ASR, and Feishu credentials.

Mitigation: Use dedicated low-privilege credentials and review the exact repository revision and scripts before installation.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/zify9000/bilibili-content-summary)
- [ClawHub skill page](https://clawhub.ai/zify9000/skills/bilibili-content-summary)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated summary content delivered through Feishu]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries are described as a short abstract, three to five key points, and chapter or structure breakdowns when available.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
