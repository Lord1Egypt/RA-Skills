## Description: <br>
Generates natural speech audio files from text through Crazyrouter's OpenAI-compatible TTS API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xujfcn](https://clawhub.ai/user/xujfcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill when they need an agent to convert supplied text or file contents into speech audio with selectable voice, model, speed, and output format. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for speech generation is sent to Crazyrouter and may contain sensitive, private, regulated, or credential material. <br>
Mitigation: Review input text before synthesis and avoid sending secrets, private documents, regulated data, or account credentials. <br>
Risk: Changing CRAZYROUTER_BASE_URL sends requests and the API key to a different endpoint. <br>
Mitigation: Leave CRAZYROUTER_BASE_URL unset unless the endpoint is intentionally trusted and approved for the data being synthesized. <br>


## Reference(s): <br>
- [Crazyrouter](https://crazyrouter.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Audio files (mp3, opus, aac, or flac) with terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CRAZYROUTER_API_KEY and can use CRAZYROUTER_BASE_URL to override the API endpoint.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
