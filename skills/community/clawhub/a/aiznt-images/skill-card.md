## Description: <br>
TS Images provides CLI commands for OpenAI-style image generation and Gemini generateContent image requests through configured AIZNT proxy URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangshengli0421](https://clawhub.ai/user/wangshengli0421) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to submit synchronous or asynchronous image-generation requests and query generated image tasks from configured service endpoints. It is suited for workflows that need OpenAI-style image APIs or Gemini generateContent image model calls from a command-line agent environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, request bodies, and --body-file content are sent to the configured image-generation service. <br>
Mitigation: Review payloads before submission and avoid sending sensitive data unless the configured service and use case are approved. <br>
Risk: The skill depends on TS_TOKEN and AIZNT_PROXY_URLS for authenticated requests to configured endpoints. <br>
Mitigation: Install only from a trusted publisher, keep credentials in managed environment secrets, and limit token exposure in logs or shell history. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wangshengli0421/aiznt-images) <br>
- [Publisher Profile](https://clawhub.ai/user/wangshengli0421) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands; command output is JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TS_TOKEN and AIZNT_PROXY_URLS environment variables; sends user-provided JSON bodies to configured image-generation endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
