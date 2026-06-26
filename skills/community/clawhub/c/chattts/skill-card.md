## Description: <br>
High-quality, conversational Text-to-Speech (TTS) generation via local ChatTTS API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Djttt](https://clawhub.ai/user/Djttt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use Chattts to convert input text into conversational speech through a configured local ChatTTS API. The skill is suited for agent workflows that need a generated WAV audio result from text plus optional seed, temperature, and top_p controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input text is sent to the configured TTS backend, which may expose secrets or sensitive personal data. <br>
Mitigation: Check CHATTTS_API_URL or the default endpoint before use, avoid sending sensitive text, and prefer a backend you operate or explicitly trust. <br>
Risk: If CHATTTS_API_URL is unset, the script falls back to a fixed private-network API endpoint. <br>
Mitigation: Set CHATTTS_API_URL explicitly for the intended trusted backend before generating speech. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Djttt/chattts) <br>
- [Publisher Profile](https://clawhub.ai/user/Djttt) <br>
- [Configured ChatTTS API Endpoint](http://172.23.252.114:8020) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, audio files, configuration] <br>
**Output Format:** [Plain text path to a generated WAV audio file, with shell command usage examples in the skill guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts text plus optional seed, temperature, and top_p values; sends them to CHATTTS_API_URL or the default ChatTTS endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
