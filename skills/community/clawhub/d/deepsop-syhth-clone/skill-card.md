## Description: <br>
声音复刻技能，使用 AI Artist API 进行音色克隆和语音合成，支持查询已有音色、上传音频创建新音色、使用指定音色合成语音。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kukuoai](https://clawhub.ai/user/kukuoai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to list available voice profiles, create new cloned voices from authorized audio samples, and synthesize speech from text through the AI Artist API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice samples, synthesis text, and generated audio links are sent to the AI Artist/OSS service. <br>
Mitigation: Use the skill only with audio and text the user is permitted to process, and avoid sending sensitive or confidential voice content unless that external processing is acceptable. <br>
Risk: Voice cloning can enable impersonation or misleading speech if used without consent. <br>
Mitigation: Create cloned voices only from speakers who own the voice sample or have explicitly authorized the cloning use case, and label generated audio appropriately when context could be misleading. <br>
Risk: The skill requires an API key and documentation contains an exposed example key that could be mistaken for a usable secret. <br>
Mitigation: Store AI_ARTIST_TOKEN in a private environment or uncommitted .env file, rotate any exposed key that could ever have been valid, and avoid sharing logs or files containing credentials. <br>
Risk: Downloaded or generated MP3 files may contain sensitive voice content. <br>
Mitigation: Protect generated audio files like the source voice data and review output locations before sharing or publishing them. <br>


## Reference(s): <br>
- [Voice Clone API documentation](references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/kukuoai/deepsop-syhth-clone) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, API calls, files, guidance] <br>
**Output Format:** [Console text with shell command examples, API responses, generated audio URLs, and optional downloaded MP3 files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AI_ARTIST_TOKEN and user-provided text, voice IDs or names, and optional audio files or audio URLs; generated audio may be saved under ~/.openclaw/workspace/audio or a user-specified output directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
