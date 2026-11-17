## Description:

基于美剧笔记的英语学习技能，覆盖听说读写复习五个模块，使用百度语音 API 进行可选 TTS，并使用本地 faster-whisper 进行可选语音识别。

This skill is ready for commercial/non-commercial use.

## Publisher:

[nanfeiduliri](https://clawhub.ai/user/nanfeiduliri)

### License/Terms of Use:

MIT-0

## Use Case:

WorkBuddy users studying English from their own TV or movie notes use this skill to generate dictation, listening, speaking, reading-comprehension, and spaced-review exercises. The skill is aimed at individual learners who want guided practice and feedback inside an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to store Baidu API credentials in a skill reference file.

Mitigation: Use quota-limited or throwaway Baidu credentials, keep the skill directory out of shared or synced folders, and rotate credentials if the directory is exposed.

Risk: The speaking practice flow records microphone audio and sends it to a localhost speech server.

Mitigation: Run the speaking server only while actively practicing, review the generated local page before use, and stop the server when finished.

Risk: Imported study notes may contain personal or copyrighted text that becomes part of generated exercises and review files.

Mitigation: Review notes before importing them, avoid sensitive material, and periodically clear generated temporary files and review-pool entries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nanfeiduliri/skills/english-coach-publish)
- [README](README.md)
- [Skill definition](SKILL.md)
- [Notes template](references/notes.md)
- [Baidu credentials guide](references/baidu_credentials.md)
- [Review pool template](references/review_pool.md)
- [Speaking practice HTML template](references/speak_template.html)
- [Baidu Speech Console](https://console.bce.baidu.com/ai/#/ai/speech/app/list)
- [Baidu TTS endpoint](https://tsn.baidu.com/text2audio)
- [Baidu OAuth token endpoint](https://openapi.baidu.com/oauth/2.0/token)
- [Hugging Face mirror used by setup instructions](https://hf-mirror.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions, learner exercises, correction feedback, shell commands, generated HTML pages, and local Python server code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create temporary local audio and HTML files, maintain a markdown review pool, and use optional user-provided Baidu credentials, microphone audio, and local Whisper model files.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
