## Description: <br>
DeepRead BYOK guides users through connecting an OpenAI, Google, or OpenRouter API key to DeepRead so document processing uses the user's provider account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uday390](https://clawhub.ai/user/uday390) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and DeepRead users use this skill to set up Bring Your Own Key document processing, understand provider billing changes, and continue using the same DeepRead API endpoints after configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users provide provider API keys to DeepRead through its dashboard. <br>
Mitigation: Confirm trust in DeepRead before setup, use scoped or limited provider keys where possible, and monitor provider billing. <br>
Risk: Sensitive API keys may be exposed through chats, logs, screenshots, committed files, or local plaintext storage. <br>
Mitigation: Avoid pasting production keys into shared contexts, keep DEEPREAD_API_KEY in an environment variable or secrets manager, and rotate keys regularly. <br>


## Reference(s): <br>
- [DeepRead homepage](https://www.deepread.tech) <br>
- [DeepRead BYOK dashboard](https://www.deepread.tech/dashboard/byok) <br>
- [ClawHub skill page](https://clawhub.ai/uday390/deepread-byok) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline shell, Python, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a DeepRead account and DEEPREAD_API_KEY; provider API keys are entered by the user in the DeepRead dashboard.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
