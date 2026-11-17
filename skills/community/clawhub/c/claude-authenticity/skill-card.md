## Description:

Detect whether an API endpoint is backed by genuine Claude rather than a wrapper, proxy, or impersonator using nine weighted rule-based checks, and optionally extract injected system prompts from providers that override Claude's identity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[helloml0326](https://clawhub.ai/user/helloml0326)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to verify Claude API keys, endpoints, and third-party Claude services, audit whether providers are serving genuine Claude, and inspect optional evidence of provider-injected system prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional prompt-extraction mode may reveal hidden provider prompts, thinking output, or other sensitive operational text.

Mitigation: Use EXTRACT_PROMPT only with explicit authorization and treat any printed prompt or thinking output as sensitive data.

Risk: The copied script requires users to edit API endpoints, model IDs, and API keys directly before execution.

Mitigation: Use test-scoped API keys, avoid committing the edited script, and review configuration before running.

Risk: Endpoint auditing can affect services or providers outside the user's control if run without authorization.

Mitigation: Install and run the skill only for endpoints the user owns or is authorized to test.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/helloml0326/skills/claude-authenticity)
- [claude-verify project](https://github.com/molloryn/claude-verify)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces authenticity scores, verdict labels, per-check details, errors, and optional prompt-extraction output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
