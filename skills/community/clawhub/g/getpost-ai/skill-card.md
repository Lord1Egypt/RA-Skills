## Description: <br>
Access 24+ LLM chat models and 16+ image/video generation models via one API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dommholland](https://clawhub.ai/user/dommholland) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call a single AI gateway for chat completions, image generation, and video generation examples. It provides API authentication guidance and curl-based request patterns for integrating supported model providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The referenced service domain may not serve the claimed API or may not be controlled by the intended provider. <br>
Mitigation: Confirm the getpost.dev service identity and documentation before sending prompts, private data, or bearer keys. <br>
Risk: Example requests send prompts and credentials to an external AI gateway. <br>
Mitigation: Start with test prompts and limited-scope credentials, and avoid sensitive data until the provider and API behavior are independently verified. <br>


## Reference(s): <br>
- [GetPost AI API documentation](https://getpost.dev/docs/api-reference#ai) <br>
- [ClawHub skill page](https://clawhub.ai/dommholland/getpost-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with curl commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes bearer-token authentication examples and polling guidance for long-running video jobs.] <br>

## Skill Version(s): <br>
1.0.0 (source: skill frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
