## Description: <br>
Generate AI-powered presentations, documents, and social posts using the Gamma.app API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucassynnott](https://clawhub.ai/user/lucassynnott) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to generate Gamma presentations, documents, and social posts from provided topics or document text through the Gamma.app API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and document text supplied to the skill are sent to Gamma.app using the configured Gamma API key. <br>
Mitigation: Use only approved content for Gamma, and do not submit secrets, credentials, private keys, regulated data, or confidential business documents unless that use is approved. <br>
Risk: The shell script can upload content chosen by the agent or user to the Gamma API. <br>
Mitigation: Prefer explicit file paths or direct content that the user intended to send, and review generated commands before execution. <br>


## Reference(s): <br>
- [Gamma ClawHub skill page](https://clawhub.ai/lucassynnott/gamma) <br>
- [Gamma API generations endpoint](https://public-api.gamma.app/v1.0/generations) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and API status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated Gamma URLs and credit usage may be returned after asynchronous API polling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
