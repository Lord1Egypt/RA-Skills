## Description: <br>
Provides Speech-to-Text for Amharic audio and text translation between languages using the Addis Assistant API, with authentication through an x-api-key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dagmawibabi](https://clawhub.ai/user/dagmawibabi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to transcribe Amharic audio and translate text through the Addis Assistant API. It is useful when a workflow needs scripted STT or language translation with an x-api-key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio, text, and API keys are sent to an external service. <br>
Mitigation: Use the skill only with audio or text that is appropriate to send to Addis Assistant and review the service handling requirements before use. <br>
Risk: The scripts ask users to pass real API keys directly on the command line. <br>
Mitigation: Prefer a safer secret source such as an environment variable or secret manager before using the scripts with production keys. <br>
Risk: The artifact endpoints do not explicitly enforce https://. <br>
Mitigation: Edit the scripts to use explicit https:// Addis Assistant endpoints before installation or deployment. <br>


## Reference(s): <br>
- [Addis Assistant API Specifications](references/api_spec.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and curl command examples; scripts print API responses as text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an x-api-key and sends audio or text to api.addisassistant.com.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
