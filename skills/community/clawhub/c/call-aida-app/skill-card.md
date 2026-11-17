## Description:

Invokes the AIDA chat-messages API with a user-provided appid, query, and JSON inputs, then returns the application response.

This skill is ready for commercial/non-commercial use.

## Publisher:

[summerloveqq](https://clawhub.ai/user/summerloveqq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to call internal AIDA applications from shell, stdin JSON, environment variables, or OpenClaw tool integrations. It is intended for workflows such as report generation, document analysis, and other AIDA-backed request processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the provided appid bearer token, inputs, query, and user identifier to the AIDA service.

Mitigation: Install and run it only when that data is intended for AIDA; prefer stdin or a managed secret store and avoid placing real tokens in shell history, exported environment variables, or logs.

Risk: Bundled tests and sample calls can make live requests when real credentials or sensitive fixtures are supplied.

Mitigation: Use dummy credentials for validation, and run tests with real data only when live production requests are explicitly intended.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/summerloveqq/skills/call-aida-app)
- [AIDA API documentation](https://aida.vip.sankuai.com)
- [OpenClaw documentation](https://openclaw.io)
- [README.zh.md](artifact/README.zh.md)
- [EXAMPLES.md](artifact/EXAMPLES.md)
- [INTEGRATION.md](artifact/INTEGRATION.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON response data plus Markdown or text usage guidance with shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The runtime response includes success, message, data, and, when available, raw_answer fields.]

## Skill Version(s):

1.0.0 (source: server release metadata, target metadata, and artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
