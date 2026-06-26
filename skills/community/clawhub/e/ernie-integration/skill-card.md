## Description: <br>
Step-by-step guide for integrating Baidu ERNIE 5.0 (Qianfan) models into Clawdbot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mattheliu](https://clawhub.ai/user/mattheliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure Baidu ERNIE 5.0 through Qianfan as a Clawdbot model provider, including API-key setup, provider configuration, verification commands, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using this integration sends Clawdbot model requests to Baidu Qianfan under the user's API account. <br>
Mitigation: Install only when that data flow is intended and approved; avoid sending secrets or regulated data unless approved for the Baidu Qianfan account and deployment context. <br>
Risk: The integration requires an ERNIE_API_KEY credential that could expose the user's Qianfan account if mishandled. <br>
Mitigation: Treat ERNIE_API_KEY like a password, keep it out of version control and shared logs, and rotate keys regularly. <br>
Risk: The artifact mentions a test script that is not included in the submitted files. <br>
Mitigation: Ignore that missing test-script instruction unless the script is supplied by a trusted source and reviewed before execution. <br>


## Reference(s): <br>
- [Configuration Examples](references/config-examples.md) <br>
- [Baidu Qianfan Documentation](https://cloud.baidu.com/doc/WENXINWORKSHOP/index.html) <br>
- [Qianfan API Reference](https://cloud.baidu.com/doc/WENXINWORKSHOP/s/Fm2vrveyu) <br>
- [Clawdbot Model Providers](https://docs.openclaw.ai/concepts/model-providers) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration, shell commands] <br>
**Output Format:** [Markdown with JSON configuration snippets and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Clawdbot provider configuration, environment variable setup, model selection commands, and API test examples.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
