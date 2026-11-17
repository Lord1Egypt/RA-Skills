## Description:

Query Burp Suite via MCP to extract security findings and proxy data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security testers use this skill to query a local Burp Suite MCP server, triage proxy history, identify security-relevant endpoints, and normalize findings while keeping captured traffic local.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Captured Burp proxy history can include credentials, PII, and sensitive response data.

Mitigation: Keep analysis local, avoid exporting captured traffic or credentials, and report sensitive findings by type and location rather than raw values.

Risk: Changing the MCP endpoint based on conversational instructions could expose data to an untrusted server.

Mitigation: Use only the locally configured trusted MCP endpoint and require actual configuration changes before using a different endpoint.

Risk: Captured authentication material could be replayed, forged, or used outside the authorized testing scope.

Mitigation: Analyze authentication patterns without replaying captured credentials or forging tokens, and review Repeater or Intruder use before active testing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/snazar-faberlens/skills/burp-zap-hardened)
- [Faberlens Safety Evaluation](https://faberlens.ai/explore/burp-zap)

## Skill Output:

**Output Type(s):** [guidance, code, configuration]

**Output Format:** [Markdown guidance with inline code and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normalizes security findings into local summaries and avoids exposing raw credential values.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
