## Description: <br>
APM 인증 센터 API documents 19 APM authentication endpoints for account, email, phone, admin, supplier, user, token refresh, verification-code, and token-validation flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[apmzoom](https://clawhub.ai/user/apmzoom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to look up APM authentication API endpoints and prepare signed requests for login, token refresh, verification-code delivery, and token validation. It is intended for agents helping with API integration work where the user already has authorization to access the APM platform. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill covers login, token refresh, and token validation flows that may expose passwords, SMS or email codes, access tokens, and refresh tokens. <br>
Mitigation: Use least-privilege accounts, keep credentials and tokens out of logs and shared prompts, and rotate any value that may have been exposed. <br>
Risk: Some flows send verification codes or may create accounts during login or registration-style authentication. <br>
Mitigation: Ask for explicit user confirmation before sending verification codes or using login flows that could create accounts. <br>
Risk: Administrator authentication endpoints can grant elevated access when used with admin credentials. <br>
Mitigation: Avoid admin credentials unless the task requires them and the user confirms the intended scope. <br>


## Reference(s): <br>
- [APM skills homepage](https://github.com/apmzoom-ai/apm-skills) <br>
- [APM authentication API base URL](https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com) <br>
- [ClawHub skill page](https://clawhub.ai/apmzoom/apmzoom-ids) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Code, Shell commands] <br>
**Output Format:** [Markdown with endpoint details, request parameters, and optional code or shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference APM_USER_TOKEN and sensitive authentication values supplied by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: artifact/SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
