## Description: <br>
Create presentations, documents, social posts, and websites using Gamma's AI API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MrGoodB](https://clawhub.ai/user/MrGoodB) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content creators use this skill to have an agent create Gamma presentations, documents, social posts, or webpages through Gamma's API and return the generated Gamma URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Gamma API key and the artifact mentions storing it in TOOLS.md, which can expose plaintext credentials. <br>
Mitigation: Provide the API key through an environment variable or secret manager, avoid version-controlled files, and do not submit confidential content unless sending it to Gamma is acceptable. <br>


## Reference(s): <br>
- [Gamma developer documentation](https://developers.gamma.app) <br>
- [Gamma public API base URL](https://public-api.gamma.app/v1.0) <br>
- [ClawHub skill page](https://clawhub.ai/MrGoodB/gamma-presentations) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns or guides retrieval of a Gamma URL after polling the generation endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
