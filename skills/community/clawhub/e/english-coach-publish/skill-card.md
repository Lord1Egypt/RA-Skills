## Description: <br>
基于美剧笔记的英语学习技能，覆盖听说读写复习五个模块。触发词：练英语、英语练习、默写、听力、口语、阅读。TTS 使用百度语音API，ASR 使用本地 faster-whisper。首次使用需配置百度 TTS 凭证和 Whisper 模型。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nanfeiduliri](https://clawhub.ai/user/nanfeiduliri) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External learners use this skill in WorkBuddy to turn their own English notes into writing, listening, speaking, reading, and spaced-review practice tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Baidu API keys and learning records are kept in local markdown files. <br>
Mitigation: Keep the skill directory private, do not commit the credentials file to a repository, and rotate any exposed keys. <br>
Risk: Speaking practice uses a localhost speech-recognition server and microphone recording page. <br>
Mitigation: Use it only for intended practice sessions, open the localhost page knowingly, and close the speech server when the exercise is finished. <br>
Risk: User notes may contain personal learning history or excerpts from watched media. <br>
Mitigation: Review note content before sharing the skill directory and avoid storing sensitive material in study files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nanfeiduliri/english-coach-publish) <br>
- [Baidu Speech Console](https://console.bce.baidu.com/ai/#/ai/speech/app/list) <br>
- [Baidu TTS Endpoint](https://tsn.baidu.com/text2audio) <br>
- [Baidu OAuth Token Endpoint](https://openapi.baidu.com/oauth/2.0/token) <br>
- [Hugging Face Mirror](https://hf-mirror.com) <br>
- [Baidu Credentials Reference](references/baidu_credentials.md) <br>
- [Notes Template](references/notes.md) <br>
- [Review Pool Reference](references/review_pool.md) <br>
- [Speaking Practice Template](references/speak_template.html) <br>
- [Notes Path Reference](references/notes_path.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with generated local files, shell commands, HTML practice pages, and three-part correction text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate temporary local audio and speech-practice files under .workbuddy/tmp_audio/ and maintain local markdown study records.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
