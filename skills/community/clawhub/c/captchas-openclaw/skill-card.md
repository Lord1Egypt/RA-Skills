## Description: <br>
OpenClaw integration guidance for CAPTCHAS Agent API, including OpenResponses tool schemas and plugin tool registration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CAPTCHASCO](https://clawhub.ai/user/CAPTCHASCO) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to connect OpenClaw agents to CAPTCHAS verification flows through OpenResponses tool schemas or OpenClaw plugin tool registration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CAPTCHAS_API_KEY is required for integration and could be exposed if stored in source, logs, or shared configuration. <br>
Mitigation: Store the API key in a secret manager or protected environment variable and avoid printing it in logs or generated examples. <br>
Risk: CAPTCHA verification data may include personal, secret, regulated, or site-specific information in signals, media_url, answers, tokens, or domain metadata. <br>
Mitigation: Send only the minimum verification data needed and avoid sensitive data unless explicitly approved for the deployment. <br>
Risk: A misconfigured CAPTCHAS endpoint or domain setting could route verification traffic incorrectly. <br>
Mitigation: Verify CAPTCHAS_ENDPOINT and optional domain settings before enabling the integration in production. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/CAPTCHASCO/captchas-openclaw) <br>
- [CAPTCHAS Publisher Profile](https://clawhub.ai/user/CAPTCHASCO) <br>
- [CAPTCHAS Homepage](https://captchas.co) <br>
- [CAPTCHAS Agent API Endpoint](https://agent.captchas.co) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Code, API Calls] <br>
**Output Format:** [Markdown with JSON and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes environment variable names, API headers, and OpenResponses/OpenClaw tool schemas.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
