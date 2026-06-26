## Description: <br>
REST API reference for 147 services, including authentication patterns, endpoints, rate limits, and common gotchas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mbrown4123](https://clawhub.ai/user/mbrown4123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill as a broad reference when integrating third-party APIs, looking up authentication patterns, endpoint examples, pagination, rate limits, webhooks, and common mistakes. It is documentation-only; users provide their own credentials and decide whether to run any commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Copy-ready examples can perform live actions against external services, including payments, trading, customer data changes, public posts, messages, or deletion. <br>
Mitigation: Review each command before execution, use test accounts or sandboxes, require explicit confirmation for mutating requests, and avoid running examples against production systems unless intended. <br>
Risk: The skill references sensitive credentials and OAuth tokens for many providers. <br>
Mitigation: Use least-privilege tokens, keep secrets in environment variables or approved secret storage, and avoid pasting real credentials into shared prompts, logs, or source files. <br>
Risk: The API reference may become stale as third-party endpoints, models, and rate limits change. <br>
Mitigation: Confirm critical endpoint behavior, pricing, permissions, and rate limits against the provider's current official documentation before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mbrown4123/api-tmp) <br>
- [Publisher profile](https://clawhub.ai/user/mbrown4123) <br>
- [Skill homepage](https://clawic.com/skills/api) <br>
- [API reference overview](artifact/SKILL.md) <br>
- [Setup guidelines](artifact/setup.md) <br>
- [Authentication patterns](artifact/auth.md) <br>
- [Credential naming](artifact/credentials.md) <br>
- [Pagination patterns](artifact/pagination.md) <br>
- [Resilience guidance](artifact/resilience.md) <br>
- [Webhook patterns](artifact/webhooks.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with endpoint tables, credential patterns, and curl-oriented code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only output; examples may reference live external APIs and user-supplied credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
