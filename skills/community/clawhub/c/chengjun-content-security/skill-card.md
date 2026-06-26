## Description: <br>
Calls the Chengjun content-security HTTP API to check text for sensitive content, protected-title wording, banned terms, grammar issues, and punctuation issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chengjunai](https://clawhub.ai/user/chengjunai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content reviewers, compliance teams, and developers use this skill to submit text to Chengjun's API before publication and receive structured checks for sensitive wording, banned terms, grammar, and punctuation issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided text is sent to api.vsbclub.com for analysis. <br>
Mitigation: Use only when that provider is approved for the environment, and avoid submitting secrets, regulated data, or confidential business content unless approved. <br>
Risk: The skill requires a Chengjun API key. <br>
Mitigation: Provide the key through CHENGJUN_API_KEY or a secret manager and avoid placing credentials in prompts, logs, or checked-in files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chengjunai/chengjun-content-security) <br>
- [Publisher profile](https://clawhub.ai/user/chengjunai) <br>
- [Chengjun platform](https://platform.vsbclub.com/) <br>
- [Chengjun content API host](https://api.vsbclub.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, API calls, configuration guidance] <br>
**Output Format:** [JSON response with status code, message, and precheck result arrays] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CHENGJUN_API_KEY; text input is limited to 5000 characters per request.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
