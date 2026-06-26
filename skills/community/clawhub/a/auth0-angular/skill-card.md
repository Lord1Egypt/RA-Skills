## Description: <br>
Use when adding authentication to Angular applications with route guards and HTTP interceptors - integrates @auth0/auth0-angular SDK for SPAs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[auth0](https://clawhub.ai/user/auth0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add Auth0 authentication to Angular 13+ single-page applications, including login/logout UI, route guards, HTTP interceptors, and protected API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated setup downloads and executes an Auth0 CLI installer script. <br>
Mitigation: Review the setup guide and installer before execution, or install Auth0 CLI through a trusted package manager. <br>
Risk: Example code logs access tokens in API examples. <br>
Mitigation: Remove token logging and avoid exposing access tokens in application logs before using generated code. <br>
Risk: The skill requires Auth0 tenant credentials and OAuth configuration. <br>
Mitigation: Verify the tenant, application, callback URLs, logout URLs, and API audience before applying generated configuration. <br>


## Reference(s): <br>
- [Setup Guide](references/setup.md) <br>
- [Integration Guide](references/integration.md) <br>
- [API Reference](references/api.md) <br>
- [Auth0 Angular SDK Documentation](https://auth0.com/docs/libraries/auth0-angular) <br>
- [Auth0 Angular Quickstart](https://auth0.com/docs/quickstart/spa/angular) <br>
- [Auth0 Angular SDK GitHub Repository](https://github.com/auth0/auth0-angular) <br>
- [Auth0 Agent Skills Homepage](https://github.com/auth0/agent-skills) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with TypeScript, Bash, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Auth0 tenant, application, callback URL, logout URL, audience, and Angular environment configuration values.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
