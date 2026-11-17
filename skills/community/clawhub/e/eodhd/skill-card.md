## Description:

Plan, build, review, or extend a stateless Bash CLI wrapper for the publicly documented EODHD API, intended for OpenClaw agents and Clawhub.ai distribution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oscraters](https://clawhub.ai/user/oscraters)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to plan, build, review, and validate a stateless Bash CLI wrapper for EODHD API access with OpenClaw-managed credentials and secret-safe logging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The published package metadata declares scripts/eodhd as the CLI entrypoint, but that file is not present in the artifact.

Mitigation: Ask the publisher to include scripts/eodhd and rerun package validation before relying on runtime behavior.

Risk: The skill requires EODHD_API_KEY for runtime API access.

Mitigation: Inject the credential through OpenClaw-managed environment handling and review dry-run, verbose, and test output for token redaction before deployment.

## Reference(s):

- [EODHD CLI ClawHub Skill Page](https://clawhub.ai/oscraters/skills/eodhd)
- [EODHD Bash CLI Implementation Plan](references/implementation-plan.md)
- [OpenClaw Secrets and Logging Notes](references/openclaw-secrets.md)
- [EODHD Calendar API Documentation](https://eodhd.com/financial-apis/calendar-upcoming-earnings-ipos-and-splits)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with code, shell command, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce CLI design guidance, Bash implementation details, validation commands, packaging metadata, and redaction recommendations.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
