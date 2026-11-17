## Description:

Validate email addresses, URLs, and domains with live DNS, DNSBL, disposable-domain, HTTP reachability, redirect-chain, SSL, WHOIS, and heuristic checks, returning recommendations and confidence or risk details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vannelier](https://clawhub.ai/user/vannelier)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and workflow operators use this skill to check whether emails, URLs, domains, and uploaded contact lists are reachable, trustworthy, or need human review before follow-up actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Validation inputs may be sent to a third-party hosted service before the user has clearly approved that data sharing.

Mitigation: Use the free quote and consent flow before validation, and do not submit emails, URLs, domains, or uploaded contact files unless the user approves third-party processing.

Risk: Secrets in URLs, internal hostnames, regulated data, or bulk contact files could expose sensitive information to the hosted operator.

Mitigation: Avoid sending those inputs to the hosted endpoint; prefer self-hosting for sensitive datasets and strip secrets from URLs before validation.

Risk: Optional self-hosted or local MCP usage depends on operator-managed credentials and dependencies.

Mitigation: Protect payment and admin environment variables, avoid exposing admin bypass keys to agents or clients, and pin dependencies for local deployments.

## Reference(s):

- [Deep Validator ClawHub Page](https://clawhub.ai/vannelier/skills/deep-validator)
- [Hosted Deep Validator Endpoint](https://deep-validator-production.up.railway.app)
- [Deep Validator Source Code](https://github.com/nathanleclaire/Agent_Validator)

## Skill Output:

**Output Type(s):** [API calls, guidance, text, configuration]

**Output Format:** [JSON responses and concise Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include recommended_action, confidence scores, risk scores, redirect details, validation checks, cost quotes, payment challenges, and self-hosting configuration.]

## Skill Version(s):

2.5.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
