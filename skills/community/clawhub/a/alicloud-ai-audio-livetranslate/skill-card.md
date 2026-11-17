## Description:

Use when live speech translation is needed with Alibaba Cloud Model Studio Qwen LiveTranslate models, including bilingual meetings, realtime interpretation, and speech-to-speech or speech-to-text translation flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare Alibaba Cloud Qwen LiveTranslate requests for bilingual meetings, live subtitles, realtime interpretation, and translated call-center captions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved translation payloads and response summaries may contain private speech or business content.

Mitigation: Keep output files in a controlled location, review them before sharing, and delete them when they are no longer needed.

## Reference(s):

- [Sources](references/sources.md)
- [Alibaba Cloud Model Studio LiveTranslate documentation](https://help.aliyun.com/document_detail/2976526.html)
- [Alibaba Cloud Model Studio newly released models](https://help.aliyun.com/zh/model-studio/newly-released-models)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON request payload files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes scoped request payloads and response summaries under output/alicloud-ai-audio-livetranslate/.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
