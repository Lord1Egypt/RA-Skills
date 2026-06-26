## Description: <br>
Automate Facebook Page posting and token management using Graph API with retry-safe, rate-limit-aware workflows for text and image content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YunneeToiChoi](https://clawhub.ai/user/YunneeToiChoi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to plan Facebook Page publishing workflows, exchange and manage Page tokens, configure required environment variables, and prepare text, image, or scheduled posts through the Graph API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Page access tokens and app secrets could be exposed if copied into chat logs, commits, or runtime output. <br>
Mitigation: Keep secrets in environment variables or a secret manager, never log tokens or app secrets, and revoke tokens when the workflow is no longer needed. <br>
Risk: Automated posting can publish unintended or noncompliant content to a live Facebook Page. <br>
Mitigation: Require human approval before publishing or scheduling posts, use least-privilege Meta permissions, and review generated requests before execution. <br>
Risk: Facebook Graph API rate limits or permission changes can cause failed or repeated posting attempts. <br>
Mitigation: Use retry logic with exponential backoff, monitor token validity, and keep posting frequency within operational limits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/YunneeToiChoi/ai-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code blocks, environment variable examples, and API endpoint examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Non-executable guidance; users must supply Meta app credentials, Page identifiers, and Page access tokens.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
