## Description: <br>
Use when live speech translation is needed with Alibaba Cloud Model Studio Qwen LiveTranslate models, including bilingual meetings, realtime interpretation, and speech-to-speech or speech-to-text translation flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to prepare Qwen LiveTranslate request payloads for bilingual meetings, realtime interpretation, live subtitles, and translated call-center captions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved request payloads, transcripts, translations, or response summaries may contain sensitive meeting or call content. <br>
Mitigation: Store generated artifacts only in appropriate locations, redact or delete them when no longer needed, and manage Alibaba Cloud credentials outside the skill with normal secret-management controls. <br>


## Reference(s): <br>
- [Sources](references/sources.md) <br>
- [Alibaba Cloud Model Studio Qwen LiveTranslate documentation](https://help.aliyun.com/document_detail/2976526.html) <br>
- [Alibaba Cloud Model Studio newly released models](https://help.aliyun.com/zh/model-studio/newly-released-models) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and JSON request payload files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save translation session payloads and response summaries under output/aliyun-qwen-livetranslate/.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
