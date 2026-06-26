## Description: <br>
Call EngageLab Web Push REST APIs to send web push notifications and in-app messages, manage tags and aliases, create scheduled tasks, delete users, query statistics, and configure callbacks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devengagelab](https://clawhub.ai/user/devengagelab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to prepare or run EngageLab Web Push API calls for browser push notifications, audience targeting, scheduled sends, callback verification, and delivery/statistics workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Web push sends, broadcasts, scheduled tasks, and registration_id deletion can affect real users or remove user data. <br>
Mitigation: Preview exact recipients, message bodies, schedules, and deletion targets before execution, and require explicit confirmation for broadcasts, schedule changes, and deletion actions. <br>
Risk: EngageLab AppKey, Master Secret, group credentials, and callback secrets are sensitive credentials. <br>
Mitigation: Keep credentials out of generated artifacts and logs, use placeholders when credentials are not provided, and treat callback secrets as production secrets. <br>
Risk: Unverified callback requests can lead to incorrect delivery or click analytics. <br>
Mitigation: Use callback signature verification with the X-CALLBACK-ID header and HMAC-SHA256 for production callback endpoints. <br>


## Reference(s): <br>
- [EngageLab Web Push Skill Page](https://clawhub.ai/devengagelab/engagelab-web-push) <br>
- [Callback API](references/callback-api.md) <br>
- [Web Push API Error Codes](references/error-codes.md) <br>
- [HTTP Status Code](references/http-status-code.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code, JSON request examples, curl commands, and language-specific API snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include EngageLab Web Push request payloads, endpoint choices, authentication placeholders, and callback verification guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
