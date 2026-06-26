## Description: <br>
Configures, exports, and invokes AICADE Galaxy dynamic services for AI use, including AICADE_GALAXY environment variables, X-API-Key authentication, service discovery, and responsePaths selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shifenghu](https://clawhub.ai/user/shifenghu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure AICADE Galaxy access, export available gateway services into an artifact, and invoke exported tools with validated JSON arguments. It is useful when an agent needs reusable command guidance for API-key authenticated dynamic services and partial JSON response selection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Environment setup can overwrite an existing .env file. <br>
Mitigation: Back up any existing .env file and review AICADE_GALAXY_* values before running setup scripts. <br>
Risk: Debug logging can expose API keys or request data. <br>
Mitigation: Keep AICADE_GALAXY_DEBUG disabled when using real credentials or sensitive payloads. <br>
Risk: Generated artifacts may invoke the wrong host or unexpected dynamic services if configuration is incorrect. <br>
Mitigation: Set AICADE_GALAXY_BASE_URL explicitly to the intended host and inspect generated artifacts before invoking tools. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shifenghu/aicade-galaxy-skill) <br>
- [AICADE Galaxy Base URL](https://aicadegalaxy.com/agent) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON, code] <br>
**Output Format:** [Markdown guidance with shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update a local .env file, export a JSON artifact, and return normalized JSON results from invoked tools.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
