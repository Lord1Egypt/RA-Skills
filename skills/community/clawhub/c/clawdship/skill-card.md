## Description: <br>
Deploy websites and apps to clawdship.dev with zero signup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicodlz](https://clawhub.ai/user/nicodlz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to publish static sites, Dockerfile-based apps, and web projects to Clawdship hosting, including initial deploys, redeploys, site management, custom-domain updates, and credit checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload selected local project files to clawdship.dev and create public hosted resources. <br>
Mitigation: Deploy from a clean build directory, exclude .env files and secrets, and require explicit confirmation before deploys or redeploys. <br>
Risk: The skill exposes deletion, custom-domain, and payment-related operations. <br>
Mitigation: Require explicit human confirmation before deletions, custom-domain changes, or credit top-ups, and share billing details clearly with the user. <br>
Risk: A configured CLAWDSHIP_API override can redirect API calls away from the default service. <br>
Mitigation: Verify CLAWDSHIP_API is not set unexpectedly before running deployment commands. <br>
Risk: Generated API keys are credentials that cannot be recovered if lost. <br>
Mitigation: Keep returned API keys private and store them in a password manager or encrypted secret store. <br>


## Reference(s): <br>
- [Clawdship](https://clawdship.dev) <br>
- [Clawdship API](https://api.clawdship.dev/v1) <br>
- [Clawdship Skill on ClawHub](https://clawhub.ai/nicodlz/clawdship) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands, URLs, API keys, billing links, and deployment guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include hosted site URLs, generated API keys, billing URLs, curl commands, and required environment variable names.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
