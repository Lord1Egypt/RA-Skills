## Description:

Provides an OpenClaw agent tool interface intended for DeepSeek-assisted code generation, problem solving, planning, and analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[barisoezcan1905](https://clawhub.ai/user/barisoezcan1905)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators can use this skill to expose a DeepSeek-oriented prompt tool for code generation, problem solving, planning, and analysis workflows. The current release behaves as a stub and should be validated before relying on it for external API-backed results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake the current stub behavior for a working DeepSeek API integration.

Mitigation: Test the tool in the target agent environment and confirm it performs real API calls before depending on generated responses.

Risk: A future API-backed version could send prompts, code, secrets, credentials, or regulated data to an external service.

Mitigation: Avoid submitting sensitive or regulated data unless organizational policy permits it and the implementation's external data flow has been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/barisoezcan1905/skills/deepseek)

## Skill Output:

**Output Type(s):** [text, code, configuration, guidance]

**Output Format:** [JSON tool result with success, message, and optional data fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DEEPSEEK_API_KEY for future API-backed use; this release returns stub responses rather than calling DeepSeek.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
