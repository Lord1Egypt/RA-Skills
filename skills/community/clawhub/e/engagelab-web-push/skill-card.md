## Description:

Helps agents use EngageLab Web Push REST APIs for browser notifications, in-app messages, tags, aliases, schedules, user deletion, statistics, and callback configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devengagelab](https://clawhub.ai/user/devengagelab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to generate API calls, client code, and configuration guidance for sending EngageLab Web Push messages and managing web push devices, schedules, statistics, and callbacks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can help send broad web push broadcasts and create or change scheduled sends.

Mitigation: Require explicit user confirmation before broadcasts or schedule changes, including message content, target scope, send time, and data center.

Risk: The skill covers user deletion by registration_id, which the artifact describes as irreversible.

Mitigation: Verify registration_id values and require explicit confirmation before generating or executing any deletion request.

Risk: EngageLab AppKey, Master Secret, GroupKey, and group master secret are sensitive credentials.

Mitigation: Use placeholders in generated examples unless credentials are intentionally supplied, and keep real secrets out of prompts, logs, and committed files.

Risk: Callback endpoints can be spoofed or replayed if signature checks are skipped.

Mitigation: Treat HMAC-SHA256 callback verification with timestamp and nonce replay checks as mandatory for production callbacks.

Risk: Changing the API base URL can route authenticated requests away from intended EngageLab hosts.

Mitigation: Restrict clients and generated commands to official HTTPS EngageLab Web Push hosts unless the user explicitly validates another endpoint.

## Reference(s):

- [Callback API](references/callback-api.md)
- [Web Push API Error Codes](references/error-codes.md)
- [HTTP Status Code](references/http-status-code.md)
- [ClawHub Skill Page](https://clawhub.ai/devengagelab/skills/engagelab-web-push)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with inline JSON, code snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request bodies, endpoint paths, authentication placeholders, and error-handling guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
