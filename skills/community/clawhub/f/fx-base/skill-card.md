## Description: <br>
Fx Base provides shared feima-lab API helper functions for dependent skills, including FX_AI_API_KEY validation, authenticated POST requests, and common JSON error handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fangshan101-coder](https://clawhub.ai/user/fangshan101-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this helper as a shared dependency for domain skills that need to call Feima's authenticated backend API and return consistent JSON error responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependent skills can send request data to Feima's API service using the configured FX_AI_API_KEY. <br>
Mitigation: Install only if you trust Feima's API service and send only data appropriate for that service. <br>
Risk: FX_AI_API_KEY is a sensitive credential used for authenticated requests. <br>
Mitigation: Keep the key private and revoke or rotate it when the integration is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Fx Base skill page](https://clawhub.ai/fangshan101-coder/fx-base) <br>
- [Feima platform](https://platform.feima.ai/) <br>
- [Feima API service endpoint](https://api-ai-brain.fenxianglife.com) <br>


## Skill Output: <br>
**Output Type(s):** [Code, API Calls, Configuration, Guidance] <br>
**Output Format:** [JavaScript module functions and JSON error output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FX_AI_API_KEY; dependent skills may send request data to Feima's API service.] <br>

## Skill Version(s): <br>
1.1.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
