## Description: <br>
Use when live speech translation is needed with Alibaba Cloud Model Studio Qwen LiveTranslate models, including bilingual meetings, realtime interpretation, and speech-to-speech or speech-to-text translation flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare Alibaba Cloud Qwen LiveTranslate request payloads for bilingual meetings, live subtitles, realtime interpretation, and translated call-center captions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved outputs may contain private meeting, call, subtitle, or business transcript content. <br>
Mitigation: Confirm that audio may be processed by Alibaba Cloud, redact sensitive content when possible, and delete or protect saved payloads and summaries. <br>


## Reference(s): <br>
- [Alibaba Cloud Qwen LiveTranslate documentation](https://help.aliyun.com/document_detail/2976526.html) <br>
- [Alibaba Cloud Model Studio newly released models](https://help.aliyun.com/zh/model-studio/newly-released-models) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON request payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save request payloads and response summaries under output/alicloud-ai-audio-livetranslate/.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
