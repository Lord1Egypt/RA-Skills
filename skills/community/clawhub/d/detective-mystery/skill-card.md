## Description: <br>
Runs an immersive Chinese detective mystery game where an LLM generates a case, suspects, clues, and the culprit, while players investigate through text or ASR input, optional TTS narration, evidence review, accusation, scoring, save/load support, and difficulty settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Delong-liu-bupt](https://clawhub.ai/user/Delong-liu-bupt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to play or run a Chinese-language voice-enabled detective game that generates a mystery case, supports suspect interrogation, location examination, evidence collection, accusation, and final scoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Game prompts, typed responses, and selected audio files may be sent to configured model, ASR, and TTS providers. <br>
Mitigation: Use dedicated API keys, avoid sensitive personal information, and run with --no-asr or --no-tts when voice services are not needed. <br>
Risk: Saved game state, generated audio, and final reports may persist locally under the outputs directory. <br>
Mitigation: Review and delete the outputs directory when saved game data, reports, or generated audio are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Delong-liu-bupt/detective-mystery) <br>
- [Prompt templates reference](references/prompts_cn.md) <br>
- [State schema reference](references/state_schema_cn.md) <br>
- [LLM provider endpoint](https://models.audiozen.cn/v1) <br>
- [ASR provider endpoint](https://api.senseaudio.cn/v1/audio/transcriptions) <br>
- [TTS provider endpoint](https://api.senseaudio.cn/v1/t2a_v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, JSON, audio files, guidance] <br>
**Output Format:** [Interactive terminal text with generated JSON game state, JSON case reports, optional MP3 TTS files, and Markdown documentation references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes saved game state and final case reports under an outputs directory; can run without ASR or TTS for reduced provider exposure.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
