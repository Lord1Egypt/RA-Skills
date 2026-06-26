## Description: <br>
Authenticate AI agents with the DeepRead OCR API using OAuth device flow so the user can approve access in a browser and the agent can receive a DEEPREAD_API_KEY. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uday390](https://clawhub.ai/user/uday390) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to authorize headless agents with a DeepRead account, complete browser approval themselves, and set DEEPREAD_API_KEY for DeepRead OCR workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill produces a live DeepRead API key that could grant account access if exposed. <br>
Mitigation: Keep DEEPREAD_API_KEY out of logs and source control, and use a secrets manager for persistent storage. <br>
Risk: An agent could be authorized unintentionally if the browser approval step is not reviewed. <br>
Mitigation: Complete the DeepRead browser approval yourself and install the skill only when you intend to authorize the agent. <br>
Risk: Test documents sent during key verification may contain sensitive content. <br>
Mitigation: Use a disposable, non-confidential PDF when testing the key. <br>


## Reference(s): <br>
- [DeepRead Homepage](https://www.deepread.tech) <br>
- [DeepRead Skill Page](https://clawhub.ai/uday390/deepread-agent-setup) <br>
- [OAuth 2.0 Device Authorization Flow](https://datatracker.ietf.org/doc/html/rfc8628) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with bash commands, JSON examples, and optional Python or shell helper scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces DEEPREAD_API_KEY for the current agent session; persistence is user-controlled.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
