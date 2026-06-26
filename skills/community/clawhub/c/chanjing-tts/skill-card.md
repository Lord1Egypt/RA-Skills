## Description: <br>
Chanjing TTS converts text to speech through the Chanjing Open API, including voice listing, task creation, polling, and generated audio URL retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iamzn1018](https://clawhub.ai/user/iamzn1018) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate speech audio from supplied text with Chanjing voices, including selecting a voice, creating a synthesis task, and polling for the completed audio URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chanjing app credentials and refreshed access tokens are stored in a local credentials.json file. <br>
Mitigation: Keep credentials.json private, do not commit or paste keys, and use CHANJING_CONFIG_DIR when credentials need to be isolated. <br>
Risk: Text is sent to the Chanjing API and completed audio is retrieved from URLs returned by the API. <br>
Mitigation: Send only text acceptable for Chanjing processing and use the skill only when the Chanjing API host and returned URLs are trusted. <br>
Risk: Changing CHANJING_API_BASE can redirect credential and text requests to another endpoint. <br>
Mitigation: Leave CHANJING_API_BASE unset unless intentionally using a trusted endpoint. <br>


## Reference(s): <br>
- [Chanjing documentation](https://doc.chanjing.cc) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples; scripts print plain text, tabular text, or JSON when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Chanjing credentials, calls the Chanjing API, and returns task IDs or generated audio URLs.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
