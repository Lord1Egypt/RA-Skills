## Description: <br>
Helps agents plan, build, review, and validate a stateless Bash CLI wrapper for the publicly documented EODHD API with OpenClaw secret handling and logging hygiene. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oscraters](https://clawhub.ai/user/oscraters) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to design, implement, review, or validate an OpenClaw-safe EODHD API CLI, including command structure, credential handling, packaging checks, and redaction rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release advertises a runnable EODHD CLI, but the package evidence is missing scripts/eodhd. <br>
Mitigation: Review before installing or publishing; either include scripts/eodhd or update the metadata to describe an instruction-only planning skill. <br>
Risk: Using a real EODHD token can make raw API calls that may consume account quota. <br>
Mitigation: Inject EODHD_API_KEY through OpenClaw secrets and approve raw API calls deliberately. <br>
Risk: API tokens may be exposed through examples, verbose output, dry-run output, or copied request URLs if redaction is not preserved. <br>
Mitigation: Keep EODHD_API_KEY out of repo files and redact api_token values in logs, dry runs, tests, traces, and diagnostics. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/oscraters/eodhd) <br>
- [Implementation Plan](references/implementation-plan.md) <br>
- [OpenClaw Secrets and Logging Notes](references/openclaw-secrets.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or modify Bash CLI files; expected runtime output from the CLI is JSON with diagnostics on stderr.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
